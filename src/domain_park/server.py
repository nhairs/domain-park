# References:
#   - https://www.dmarcanalyzer.com/setup-parked-or-inactive-domains/
#   - https://www.cyber.gov.au/publications/how-to-combat-fake-emails
#   - https://www.m3aawg.org/sites/default/files/m3aawg_parked_domains_bp-2015-12.pdf

### IMPORTS
### ============================================================================
## Standard Library

## Installed
from nserver import NameServer, Response, A, TXT, NS, MX

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
server = NameServer("domain-park")  # pylint: disable=invalid-name


@server.rule("{base_domain}", ["NS"])
def name_server_responder(query):
    """Provide name servers.
    """
    response = Response()
    for ns_server, ip in PARKIT_SERVERS.items():  # pylint: disable=invalid-name
        response.answers.append(NS(query.name, ns_server))
        response.additional.append(A(ns_server, ip))
    return response


@server.rule("_dmarc.{base_domain}", ["TXT"])
def dmarc_record_responder(query):
    """Provide DMARC with reject policy.
    """
    return TXT(query.name, "v=DMARC1; p=reject")


@server.rule("**._domainkey.{base_domain}", ["TXT"])
@server.rule("**._domainkey.**.{base_domain}", ["TXT"])
def dkim_record_responder(query):
    """Provide empty DKIM key to all potential lookups.
    """
    return TXT(query.name, "v=DKIM1; p=")


@server.rule("{base_domain}", ["TXT"])
@server.rule("**.{base_domain}", ["TXT"])
def spf_record_responder(query):
    """Provide SPF that rejects all.
    """
    return TXT(query.name, "v=spf1 -all")


@server.rule("{base_domain}", ["MX"])
def mx_record_responder(query):
    """Provide empty MX record.
    """
    return MX(query.name, ".", 0)


### MAIN
### ============================================================================
if __name__ == "__main__":
    server.run()
