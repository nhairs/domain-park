### IMPORTS
### ============================================================================
## Future
from __future__ import annotations

## Standard Library
import argparse

## Installed
import netifaces
import nserver
import pillar.application

## Application
from . import _version
from .server import make_server

### CONSTANTS
### ============================================================================
_APP = None


### FUNCTIONS
### ============================================================================
def get_available_ips():
    """Get all available IPv4 Address on this machine."""
    # Source: https://stackoverflow.com/a/274644
    ip_list = []
    for interface in netifaces.interfaces():
        for link in netifaces.ifaddresses(interface).get(netifaces.AF_INET, []):
            ip_list.append(link["addr"] + f" ({interface})")

    # shortcut for all
    ip_list.append("0.0.0.0 (all above)")
    return ip_list


def main(argv=None):
    """Main function for use with setup.py"""
    global _APP  # pylint: disable=global-statement

    _APP = Application(argv)
    return _APP.run()


### CLASSES
### ============================================================================
class IpsAction(argparse.Action):
    "ArgParse Action to print IPs and exit"
    # Ref: https://stackoverflow.com/a/25596386/12281814

    def __call__(self, parser, *args, **kwargs):
        print("\n".join(get_available_ips()))
        parser.exit(0)
        return


class Application(pillar.application.Application):
    """domain-park is a DNS Name Server that can be used to prevent spoofed emails on parked domains."""

    application_name = "domain-park"
    name = "domain_park"
    version = _version.get_version_info_full()
    epilog = (
        "For full information including licence see https://github.com/nhairs/domain-park\n\n"
        "Copyright (c) 2020 Nicholas Hairs"
    )
    config_args_enabled = False
    logging_manifest = pillar.application.LoggingManifest(additional_namespaces=["nserver"])  # type: ignore[call-arg]

    server: nserver.NameServer

    def get_argument_parser(self) -> argparse.ArgumentParser:
        parser = super().get_argument_parser()

        # Server settings
        parser.add_argument(
            "--host",
            action="store",
            default="localhost",
            help="Host (IP) to bind to. Use --ips to see available. Defaults to localhost.",
        )

        parser.add_argument(
            "--port",
            action="store",
            default=9953,
            type=int,
            help="Port to bind to. Defaults to 9953.",
        )

        transport_group = parser.add_mutually_exclusive_group()
        transport_group.add_argument(
            "--tcp",
            action="store_const",
            const="TCPv4",
            dest="transport",
            help="Use TCPv4 socket for transport.",
        )
        transport_group.add_argument(
            "--udp",
            action="store_const",
            const="UDPv4",
            dest="transport",
            help="Use UDPv4 socket for transport. (default)",
        )

        # DNS settings
        parser.add_argument(
            "-n",
            "--nameserver",
            required=True,
            action="append",
            help="Add NameServer to list returned on NS lookups. This should be equal to the NS records available publicly running domain-park. Must be supplied at least once, and has no limit. Reccomended to have 2-4 Name Servers. Expected to be in the format of either 'FQDN:IP' or 'HOST'",
            dest="nameservers",
            metavar="NAMESERVER",
        )

        parser.add_argument(
            "--rua",
            action="store",
            help="Email address to use for DMARC aggregate repots.",
            metavar="EMAIL",
        )

        parser.add_argument(
            "--ruf",
            action="store",
            help="Email address to use for DMARC forensic reports.",
            metavar="EMAIL",
        )

        parser.add_argument(
            "--ips",
            action=IpsAction,
            nargs=0,
            help="Print available IPs and exit",
        )

        parser.set_defaults(transport="UDPv4")
        return parser

    def get_server(self) -> nserver.NameServer:
        """Get NameServer instance."""

        settings = nserver.Settings()
        settings.server_transport = self.args.transport
        settings.server_address = self.args.host
        settings.server_port = self.args.port
        settings.console_log_level = 0

        nameservers = []
        for nameserver in self.args.nameservers:
            if ":" in nameserver:
                host, ip = nameserver.split(":")
            else:
                # assume IP
                host = None
                ip = nameserver

            # TODO: IP validation

            nameservers.append((host, ip))

        return make_server(nameservers, self.args.rua, self.args.ruf, settings)

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.server = self.get_server()
        return

    def main(self) -> None:
        if self.args.ips:
            print("\n".join(get_available_ips()))
            return

        self.server.run()
        return
