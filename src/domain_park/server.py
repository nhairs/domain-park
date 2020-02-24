### IMPORTS
### ============================================================================
## Standard Library

## Installed
from nserver import NameServer, Response, A, TXT, NS

## Application


### CONSTANTS
### ============================================================================
PARKIT_SERVERS = {
    "ns1.parkit-beta.nicholashairs.com": "178.128.19.50",
    "ns2.parkit-beta.nicholashairs.com": "178.128.19.50",
    "ns3.parkit-beta.nicholashairs.com": "178.128.19.50",
    "ns4.parkit-beta.nicholashairs.com": "178.128.19.50",
}


### SERVER
### ============================================================================
server = NameServer("parkit", "n1.parkit-beta.nicholashairs.com")

@server.rule("{base_domain}", ["NS"])
def name_server_responder(query):
    response = Response()
    for server, ip in PARKIT_SERVERS.items():
        response.answers.append(NS(server, resource_name=query.name))
        response.additional.append(A(ip, resource_name=server))
    return response

@server.rule("_dmarc.{base_domain}", ["TXT"])
def dmarc_record_responder(query):
    return TXT("v=DMARC1; p=reject", resource_name=query.name)

@server.rule("{base_domain}", "TXT")
def spf_record_responder(query):
    return TXT("v=spf1 -all", resource_name=query.name)


### MAIN
### ============================================================================
if __name__ == "__main__":
    server.run()


