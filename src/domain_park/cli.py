### IMPORTS
### ============================================================================
## Standard Library
import argparse
import logging
import sys
from typing import List, Dict, Any

## Installed
import netifaces  # type: ignore
import nserver

## Application
from . import _version
from .server import server as nserver_server

### CONSTANTS
### ============================================================================
DESCRIPTION = (
    "domain-park is a DNS Name Server that can be used to prevent spoofed emails on parked domains."
)

EPILOG = """For full information including licence see https://github.com/nhairs/domain-park

Copyright (c) 2020 Nicholas Hairs
"""

_APP = None

### FUNCTIONS
### ============================================================================
def get_available_ips():
    """Get all available IPv4 Address on this machine.
    """
    # Source: https://stackoverflow.com/a/274644
    ip_list = []
    for interface in netifaces.interfaces():
        for link in netifaces.ifaddresses(interface).get(netifaces.AF_INET, []):
            ip_list.append(link["addr"] + f" ({interface})")

    # shortcut for all
    ip_list.append("0.0.0.0 (all above)")
    return ip_list


def main(argv=None):
    """Main function for use with setup.py
    """
    global _APP  # pylint: disable=global-statement

    _APP = Application(argv)
    _APP.run()
    return


### CLASSES
### ============================================================================
class Application:
    """domain-park application.

    Handles reading config and instantiating nserver instance.
    """

    def __init__(self, argv: List[str] = None):
        self.argv = argv if argv is not None else sys.argv[1:]
        self.parser = self.get_parser()
        self.args = self.parser.parse_args(self.argv)
        self.config = self.get_config()
        self.server = self.get_server()
        return

    def run(self) -> None:
        """Run application.
        """
        if self.args.ips:
            print("\n".join(get_available_ips()))
            return
        self.server.run()
        return

    @staticmethod
    def get_parser() -> argparse.ArgumentParser:
        """Get argument parser.
        """
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=DESCRIPTION,
            epilog=EPILOG,
        )

        parser.add_argument("--version", action="version", version=_version.get_version_info_full())

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

        # TODO
        # - implement rua, ruf

        parser.add_argument("--ips", action="store_true", help="Print available IPs and exit")

        parser.set_defaults(transport="UDPv4")
        return parser

    @staticmethod
    def get_config() -> Dict[str, Any]:
        """Get config taking into account command line arguments.
        """
        return {}

    def get_server(self) -> nserver.NameServer:
        """Get NameServer instance.
        """
        server = nserver_server

        server.settings.SERVER_TYPE = self.args.transport
        server.settings.SERVER_ADDRESS = self.args.host
        server.settings.SERVER_PORT = self.args.port
        server.settings.CONSOLE_LOG_LEVEL = logging.WARNING
        return server
