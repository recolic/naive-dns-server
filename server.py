#!/usr/bin/python3
import datetime
import sys
import time
import threading
import traceback
import socketserver
from dnslib import *


#class DomainName(str):
#    def __getattr__(self, item):
#        return DomainName(item + '.' + self)
#D = DomainName('example.com.')
#IP = '127.0.0.1'
#TTL = 60 * 5
PORT = 53

conf = [
    ('example.com.', 'A', '1.1.1.1', 60),
    ('example.com.', 'A', '1.0.0.1', 60),
    ('example.com.', 'AAAA', '::1', 60),
    ('example.com.', 'TXT', '"fuck you"', 120),
    ('example.com.', 'TXT', '"v=spf -all"', 120),
    ('example.com.', 'NS', 'l.example.com.', 120),
    ('b.example.com.', 'A', '2.2.2.2', 60),
    ('l.example.com.', 'A', '127.0.0.1', 60),
]

conf = """
# Note: Use SPACE character to split columns.
#       DO NOT use TAB character. It's not allowed.
# hostname        TYPE   TTL    VALUE
example.com.       A     60   1.1.1.1
example.com.       A     60   1.0.0.1
example.com.       AAAA  60   ::1
example.com.       TXT   120  "fuck you"
example.com.       TXT   120  "v=spf -all"
example.com.       NS    120  l.example.com.
b.example.com.     A     60   2.2.2.2
l.example.com.     A     60   127.0.0.1
mail.example.com.  MX    300  5 b.example.com
mail.example.com.  MX    300  10 l.example.com
f.example.com.     CNAME 30   b.example.com
"""



#soa_record = SOA(
#    mname=D.ns1,  # primary name server
#    rname=D.andrei,  # email of the domain administrator
#    times=(
#        201307231,  # serial number
#        60 * 60 * 1,  # refresh
#        60 * 60 * 3,  # retry
#        60 * 60 * 24,  # expire
#        60 * 60 * 1,  # minimum
#    )
#)
#ns_records = [NS(D.ns1), NS(D.ns2)]
#records = {
#    D: [A(IP), AAAA((0,) * 16), MX(D.mail), soa_record] + ns_records,
#    D.ns1: [A(IP)],  # MX and NS records must never point to a CNAME alias (RFC 2181 section 10.3)
#    D.ns2: [A(IP)],
#    D.mail: [A(IP)],
#    D.andrei: [CNAME(D)],
#}

records = {}

def init():
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
        
        
    for line in conf.split('\n'):
        record = _line_to_arr(line)
        if record == []:
            continue

        if record[0] not in records:
            records[record[0]] = []
        
        record_type = record[1]
        record_data = None
        if record_type == 'A':
            record_data = A(record[3])
        elif record_type == 'AAAA':
            record_data = AAAA(record[3])
        elif record_type == 'CNAME':
            record_data = CNAME(record[3])
        elif record_type == 'TXT':
            record_data = TXT(record[3])
        elif record_type == 'NS':
            record_data = NS(record[3])
        elif record_type == 'MX':
            record_data = MX(record[3])
        elif record_type == 'SPF':
            record_data = SPF(record[3])
        elif record_type == 'PTR':
            raise RuntimeError("PTR record not supported. Please add money if you want it.")
        elif record_type == 'SOA':
            raise RuntimeError("SOA record not supported. Please add money if you want it.")
        elif record_type == 'CERT':
            raise RuntimeError("CERT record not supported. Please add money if you want it.")
        else:
            raise RuntimeError("Unknown record type " + record_type)
        
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
            ans = RR(rname=qname, ttl=record_ttl, rdata=record_data)
            record_match = False
            if query_type == record_type or query_type == 'ALL' or query_type == '*' or query_type == 'ANY' or record_type == 'CNAME':
                reply.add_answer(ans)


    return reply.pack()


#    if queried_domain == D or queried_domain.endswith('.' + D):
#        for name, rrs in records.items():
#            print('iter', name)
#            if name == queried_domain:
#                print('hit')
#                for rdata in rrs:
#                    rqt = rdata.__class__.__name__
#                    if qt in ['*', rqt]:
#                        reply.add_answer(RR(rname=qname, rtype=QTYPE[rqt], rclass=1, ttl=TTL, rdata=rdata))
#
#        for rdata in ns_records:
#            reply.add_ns(RR(rname=D, rtype=QTYPE.NS, rclass=1, ttl=TTL, rdata=rdata))
#
#        reply.add_ns(RR(rname=D, rtype=QTYPE.SOA, rclass=1, ttl=TTL, rdata=soa_record))
#
#    print("---- Reply:\n", reply)
#
#    return reply.pack()


class BaseRequestHandler(socketserver.BaseRequestHandler):

    def get_data(self):
        raise NotImplementedError

    def send_data(self, data):
        raise NotImplementedError

    def handle(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("\n\n%s request %s (%s %s):" % (self.__class__.__name__[:3], now, self.client_address[0],
                                               self.client_address[1]))
        try:
            data = self.get_data()
            self.send_data(dns_response(data))
        except Exception:
            traceback.print_exc(file=sys.stderr)


class TCPRequestHandler(BaseRequestHandler):
    def get_data(self):
        data = self.request.recv(8192).strip()
        sz = int(data[:2].hex(), 16)
        if sz < len(data) - 2:
            raise Exception("Wrong size of TCP packet")
        elif sz > len(data) - 2:
            raise Exception("Too big TCP packet")
        return data[2:]

    def send_data(self, data):
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
        socketserver.ThreadingUDPServer(('', PORT), UDPRequestHandler),
        socketserver.ThreadingTCPServer(('', PORT), TCPRequestHandler),
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