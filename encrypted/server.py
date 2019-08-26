#!/usr/bin/python3
import sys
import threading
import socketserver
from dnslib import *
import fnmatch

from Cryptodome.PublicKey import RSA
import rrsa, base64
pub_pem = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwGAKamKFesqyEfF3l3gS
H7VrkxAi62pLd+I4f/Atr/LhAcgQA1c9CIta2AQ1BJ3+rKHMHI1FJDDO2VwslKdV
qit1rCA41iAH0Nx4+T4KAQQLY/NxLbgFz9tTRM+kb53x1zVDUG/4IV8VIznMmSXG
j1YDhZUAaNnY6UfsBBKpPQ/9BP17ic8bjoyNFy7ryi7LUGhLtO3wfU2UbTYZrx9k
SsfT/r9OsK0B7Eoe4syY3/3nr/UplzWH4VMv57wfgy7j5mr1XKfmq8P2eqKH/8/p
GuCmJP6iXontxx7C3zjfBFBcFUbq+h/8TUgpFBbPV332kEaZ/du8wuo437CFrzSO
vQIDAQAB
-----END PUBLIC KEY-----
"""

records = {}
wildcard_records = []

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
 
        
        
def init(conf):
    global records
    for line in conf.split('\n'):
        record = _line_to_arr(line)
        if record == []:
            continue

        record_hostname = record[0]
        record_type = record[1]
        record_data = _record_type_construct_data(record_type, record[3])

        good_record = [record[0], record[1], int(record[2]), record_data]
        if '*' in record_hostname or '?' in record_hostname:
            # wildcard domain
            wildcard_records.append(good_record)
        else:
            # non-wildcard normal domain
            if record_hostname not in records:
                records[record_hostname] = []
            records[record_hostname].append(good_record)


def dns_response(data):
    request = DNSRecord.parse(data)

    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

    qname = request.q.qname
    query_domain = str(qname)
    qtype_code = request.q.qtype
    query_type = QTYPE[qtype_code]

    #print('QUERY>', query_domain, query_type)

    found = False
    if query_domain in records:
        for record in records[query_domain]:
            record_type, record_ttl, record_data = record[1:]
            ans = RR(rname=qname, ttl=record_ttl, rtype=_record_type_to_typecode(record_type), rdata=record_data)
            if query_type == record_type or query_type == 'ALL' or query_type == '*' or query_type == 'ANY' or record_type == 'CNAME':
                found = True
                reply.add_answer(ans)

    if not found:
        # Lookup wildcard domains.
        for record in wildcard_records:
            if not fnmatch.fnmatch(query_domain, record[0]):
                continue
            record_type, record_ttl, record_data = record[1:]
            ans = RR(rname=qname, ttl=record_ttl, rtype=_record_type_to_typecode(record_type), rdata=record_data)
            if query_type == record_type or query_type == 'ALL' or query_type == '*' or query_type == 'ANY' or record_type == 'CNAME':
                reply.add_answer(ans)
                break # Only add the first matched wildcard answer.

    return reply.pack()


class BaseRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            data = self.get_data()
            self.send_data(dns_response(data))
        except Exception as e:
            print('Exception:', e)

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
    if len(sys.argv) != 3:
        print('Usage: ./this.py <ListenAddr> <ConfigFile>')
        print('Example: ./this.py 0.0.0.0:53 /etc/dns.py.conf')
        exit(1)
    
    print('Reading config...')
    listen, configFile = sys.argv[1], sys.argv[2]
    ar = listen.split(':')
    if len(ar) != 2:
        raise RuntimeError("Invalid listen address " + listen)
    listen_addr, listen_port = ar[0], int(ar[1])

    with open(configFile, "r") as f:
        encrypted_encoded = ''
        for line in f.read().split('\n'):
            if line == '' or line[0] == '#':
                continue
            encrypted_encoded += line.replace('\t','').replace('\n','').replace(' ','').replace('\r','')
    
    encrypted = base64.b64decode(encrypted_encoded)
    pub = RSA.import_key(pub_pem.strip())
    conf = rrsa.encryptDecryptBytes(rrsa._encrypt, pub, encrypted).decode('utf-8')
    #print('conf:', conf)
    init(conf)

    print("Starting nameserver...")

    servers = [
        socketserver.ThreadingUDPServer((listen_addr, listen_port), UDPRequestHandler),
        socketserver.ThreadingTCPServer((listen_addr, listen_port), TCPRequestHandler),
    ]
    for s in servers:
        thread = threading.Thread(target=s.serve_forever)  # that thread will start one more thread for each request
        thread.daemon = True  # exit the server thread when the main thread terminates
        thread.start()
        print('Listening TCP & UDP ', s.server_address)

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