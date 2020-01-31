### IMPORTS
### ============================================================================
## Standard Library
import socket
import socketserver
import struct
import sys
import time
from typing import Optional

## Installed
import dnslib
import tldextract

## Application


TTL = dnslib.secs["m"] * 5

### GENERAL SERVERS
### ============================================================================
## DNS Handler
## -----------------------------------------------------------------------------
class DNSHandler(socketserver.BaseRequestHandler):
    def process_dns_request(self, data) -> Optional[bytes]:
        request = dnslib.DNSRecord.parse(data)
        print()
        print("[ REQUEST ] =====================================================")
        print(request)

        response = request.reply()

        if request.header.opcode != dnslib.OPCODE.QUERY:
            response.header.set_rcode(dnslib.RCODE.REFUSED)
            return response.pack()

        for question in request.questions:
            print()
            print("[ QUESTION ] ============================================")
            print(question)
            question_domain = str(question.qname).rstrip(".")
            question_domain_parts = tldextract.extract(question_domain)

            if question.qtype == dnslib.QTYPE.NS and not question_domain_parts.subdomain:
                # NS lookup
                for i in range(1,5):
                    answer = dnslib.RR(
                        question_domain,
                        dnslib.QTYPE.NS,
                        rdata=dnslib.NS("ns{}.parkit-beta.nicholashairs.com".format(i)),
                        ttl=TTL
                    )
                    response.add_answer(answer)

            elif question.qtype == dnslib.QTYPE.TXT:
                # TXT lookup
                if question_domain_parts.subdomain == "_dmarc":
                    # DMARC record
                    answer = dnslib.RR(
                        question_domain,
                        dnslib.QTYPE.TXT,
                        rdata=dnslib.TXT("v=DMARC1; p=reject"),
                        ttl=TTL
                    )
                    response.add_answer(answer)

                elif not question_domain_parts.subdomain:
                    # raw domain - return SPF record
                    answer = dnslib.RR(
                        question_domain, dnslib.QTYPE.TXT, rdata=dnslib.TXT("v=spf1 -all"), ttl=TTL
                    )
                    response.add_answer(answer)
                # TODO: DKIM
                # If no match then no answer


        print()
        print("[ RESPONSE ] ====================================================")
        print(response)
        return response.pack()

## Transports
## -----------------------------------------------------------------------------
# TCP
# ..............................................................................
def receive_tcp_message(sock: socket.socket, length: int) -> bytes:
    message = b""
    remaining = length

    while remaining > 0:
        message += sock.recv(remaining)
        remaining = length - len(message)

    return message


class TCPHandler(DNSHandler):
    """

    References:
        - https://tools.ietf.org/html/rfc7766#section-8
    """
    def handle(self):
        data = receive_tcp_message(self.request, struct.unpack("!H", self.request.recv(2))[0])
        response = self.process_dns_request(data)
        if response:
            length = struct.pack("!H", len(response))
            self.request.sendall(length + response)
        return


# UDP
# ..............................................................................
class UDPHandler(DNSHandler):
    def handle(self):
        data, sock = self.request
        response = self.process_dns_request(data)
        if response:
            print()
            print("[ DATA ] ====================================================")
            print(response)
            sock.sendto(response, self.client_address)
        return


## DNS Server
## -----------------------------------------------------------------------------


### MAIN
### ============================================================================
if __name__ == "__main__":
    HOST, PORT = "localhost", 9953
    TIMEOUT = 60
    start_time = time.time()

    #server = socketserver.UDPServer((HOST, PORT), UDPHandler)

    print("Starting Server")

    while (time.time()) - start_time < TIMEOUT:
        try:
            server = socketserver.TCPServer((HOST, PORT), TCPHandler)
            break
        except OSError as e:
            if e.errno == 98:
                time.sleep(5)
                continue
            raise e
    else:
        print("Failed to start server after {}s".format(TIMEOUT))
        sys.exit(1)
    print("Server started")
    server.serve_forever()
