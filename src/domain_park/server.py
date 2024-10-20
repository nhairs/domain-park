# References:
#   - https://www.dmarcanalyzer.com/setup-parked-or-inactive-domains/
#   - https://www.cyber.gov.au/publications/how-to-combat-fake-emails
#   - https://www.m3aawg.org/sites/default/files/m3aawg_parked_domains_bp-2015-12.pdf

### IMPORTS
### ============================================================================
## Future
from __future__ import annotations

## Standard Library

## Installed
from nserver import NameServer, Response, A, TXT, NS, MX, CAA, Settings

## Application


### SERVER
### ============================================================================
def make_server(
    name_servers: list[tuple[str | None, str]],
    rua_address: str | None = None,
    ruf_address: str | None = None,
    settings: Settings | None = None,
) -> NameServer:
    """Factory for producing domain-park servers

    Args:
        name_servers: NS records
        rua_address:
        ruf_address:
        settings:
    """

    server = NameServer("domain-park", settings)  # pylint: disable=invalid-name

    @server.rule("{base_domain}", ["NS"])
    def name_server_responder(query):
        """Provide name servers."""
        # pylint: disable=no-member
        # We attach extra things to server.settings in the cli wrapper

        response = Response()
        for host, ip in name_servers:
            if host is None:
                response.answers.append(NS(query.name, ip))
            else:
                response.answers.append(NS(query.name, host))
                response.additional.append(A(host, ip))
        return response

    @server.rule("_dmarc.{base_domain}", ["TXT"])
    def dmarc_record_responder(query):
        """Provide DMARC with reject policy."""
        # pylint: disable=no-member
        # We attach extra things to server.settings in the cli wrapper

        dmarc_string = "v=DMARC1; p=reject;"

        if rua_address:
            dmarc_string += f" rua=mailto:{rua_address};"

        if ruf_address:
            dmarc_string += f" ruf=mailto:{ruf_address};"

        return TXT(query.name, dmarc_string)

    @server.rule("**._domainkey.{base_domain}", ["TXT"])
    @server.rule("**._domainkey.**.{base_domain}", ["TXT"])
    def dkim_record_responder(query):
        """Provide empty DKIM key to all potential lookups."""
        return TXT(query.name, "v=DKIM1; p=")

    @server.rule("{base_domain}", ["TXT"])
    @server.rule("**.{base_domain}", ["TXT"])
    def spf_record_responder(query):
        """Provide SPF that rejects all."""
        return TXT(query.name, "v=spf1 -all")

    @server.rule("{base_domain}", ["MX"])
    def mx_record_responder(query):
        """Provide empty MX record."""
        return MX(query.name, ".", 0)

    @server.rule("{base_domain}", ["A", "AAAA"])
    def a_record_responder(query):  # pylint: disable=unused-argument
        """Provide no A/AAAA records"""
        return Response()

    @server.rule("{base_domain}", ["CAA"])
    @server.rule("**.{base_domain}", ["CAA"])
    def caa_record_responder(query):
        """Provide CAA that rejects all."""
        # TODO: look into priority flag and determine if it should be set.
        # TODO: look into add iodef records to allow reporting
        return CAA(query.name, 0, "issue", ";")

    return server
