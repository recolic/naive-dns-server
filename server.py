#!/usr/bin/python3
import sys
import threading
import socketserver
from dnslib import *

listen_addr = '0.0.0.0'
listen_port = 53

conf = """
# Note: Use SPACE character to split columns.
#       DO NOT use TAB character. It's not allowed.
# hostname        TYPE   TTL    VALUE
example.com.       A     60   1.1.1.1
example.com.       A     60   1.0.0.1
example.com.       AAAA  60   2606:4700:30::681b:90e6
# TXT record: DO NOT add the double quote `""`.
example.com.       TXT   120  fuck you
example.com.       TXT   120  v=spf -all
example.com.       NS    120  l.example.com.
b.example.com.     A     60   2.2.2.2
l.example.com.     A     60   127.0.0.1
mail.example.com.  MX    300  5,b.example.com
mail.example.com.  MX    300  10,l.example.com
f.example.com.     CNAME 30   b.example.com
"""

records = {}

def _line_to_arr(line):
    line_backup = line
    line = line.strip(' \t\r\n')
    if line == '' or line[0] == '#':
        return []
    res = []
    for _ in range(3):
        pos = line.find(' ')
        if pos == -1:
            raise RuntimeError("Invalid configuration line:" + line_backup)
        res.append(line[:pos])
        line = line[pos:].strip()
    res.append(line)
    return res
def _record_type_construct_data(record_type, data_string):
    if record_type == 'A':
        return A(data_string)
    elif record_type == 'AAAA':
        return AAAA(data_string)
    elif record_type == 'CNAME':
        return CNAME(data_string)
    elif record_type == 'TXT':
        return TXT(data_string)
    elif record_type == 'NS':
        return NS(data_string)
    elif record_type == 'MX':
        pref, addr = data_string.split(',')
        return MX(addr, int(pref))
    elif record_type == 'SPF':
        return SPF(data_string)
    elif record_type == 'PTR':
        raise RuntimeError("PTR record not supported. Please add money if you want it.")
    elif record_type == 'SOA':
        raise RuntimeError("SOA record not supported. Please add money if you want it.")
    elif record_type == 'CERT':
        raise RuntimeError("CERT record not supported. Please add money if you want it.")
    else:
        raise RuntimeError("Unknown record type " + record_type)
def _record_type_to_typecode(record_type):
    _m = {
        'A': 1,
        'AAAA': 28,
        'CNAME': 5,
        'TXT': 16,
        'NS': 2,
        'MX': 15,
        'SPF': 99,
        'PTR': 12,
        'SOA': 6,
        'CERT': 37
    }
    if record_type in _m:
        return _m[record_type]
    else:
        raise RuntimeError("Unknown record type " + record_type)
 
        
        
def init():
    global records
    for line in conf.split('\n'):
        record = _line_to_arr(line)
        if record == []:
            continue

        if record[0] not in records:
            records[record[0]] = []
        
        record_type = record[1]
        record_data = _record_type_construct_data(record_type, record[3])
       
        records[record[0]].append([record[0], record[1], int(record[2]), record_data])


def dns_response(data):
    request = DNSRecord.parse(data)

    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

    qname = request.q.qname
    query_domain = str(qname)
    qtype_code = request.q.qtype
    query_type = QTYPE[qtype_code]

    print('QUERY>', query_domain, query_type)

    if query_domain in records:
        for record in records[query_domain]:
            record_type, record_ttl, record_data = record[1:]
            ans = RR(rname=qname, ttl=record_ttl, rtype=_record_type_to_typecode(record_type), rdata=record_data)
            record_match = False
            if query_type == record_type or query_type == 'ALL' or query_type == '*' or query_type == 'ANY' or record_type == 'CNAME':
                reply.add_answer(ans)

    return reply.pack()


class BaseRequestHandler(socketserver.BaseRequestHandler):

    def get_data(self):
        raise NotImplementedError

    def send_data(self, data):
        raise NotImplementedError

    def handle(self):
#        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
#        print("\n\n%s request %s (%s %s):" % (self.__class__.__name__[:3], now, self.client_address[0],
#                                               self.client_address[1]))
        try:
            data = self.get_data()
            self.send_data(dns_response(data))
        except Exception:
            traceback.print_exc(file=sys.stderr)


class TCPRequestHandler(BaseRequestHandler):
    def get_data(self):
        data = self.request.recv(8192).strip()
        #return data
        sz = int(data[:2].hex(), 16)
        if sz < len(data) - 2:
            raise Exception("Wrong size of TCP packet")
        elif sz > len(data) - 2:
            raise Exception("Too big TCP packet")
        return data[2:]

    def send_data(self, data):
        #return self.request.sendall(data)
        sz = bytes.fromhex(hex(len(data))[2:].zfill(4))
        return self.request.sendall(sz + data)


class UDPRequestHandler(BaseRequestHandler):

    def get_data(self):
        return self.request[0] # .strip()

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)


if __name__ == '__main__':
    print('Reading records...')
    init()
    print("Starting nameserver...")

    servers = [
        socketserver.ThreadingUDPServer((listen_addr, listen_port), UDPRequestHandler),
        socketserver.ThreadingTCPServer((listen_addr, listen_port), TCPRequestHandler),
    ]
    for s in servers:
        thread = threading.Thread(target=s.serve_forever)  # that thread will start one more thread for each request
        thread.daemon = True  # exit the server thread when the main thread terminates
        thread.start()
        print("%s server loop running in thread: %s" % (s.RequestHandlerClass.__name__[:3], thread.name))

    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        for s in servers:
            s.shutdown()
