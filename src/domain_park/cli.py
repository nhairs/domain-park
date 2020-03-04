### IMPORTS
### ============================================================================
## Standard Library
import argparse
import sys

## Installed
import netifaces  # type: ignore

## Application
from . import _version
from .server import server as nserver_server

### CONSTANTS
### ============================================================================
DESCRIPTION = f"""Version: {_version.get_version_info()}
"""

_SERVER = None
_PARSER = None

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


def main(argv=None):  # pylint: disable=missing-function-docstring,global-statement
    global _SERVER  # pylint: disable=global-statement
    global _PARSER  # pylint: disable=global-statement

    if argv is None:
        argv = sys.argv[1:]

    # Create argument parser
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument("--version", action="version", version=_version.get_version_info_full())

    parser.add_argument(
        "--host",
        action="store",
        default="localhost",
        help="Host (IP) to bind to. Use --ips to see available. Defaults to localhost.",
    )

    parser.add_argument(
        "--port", action="store", default=9953, type=int, help="Port to bind to. Defaults to 9953."
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

    # Save argument parser
    _PARSER = parser

    # Parse arguments
    args = parser.parse_args(argv)

    # special case
    if args.ips:
        print("\n".join(get_available_ips()))
        return

    # Create and configure server
    server = nserver_server

    server.settings.SERVER_TYPE = args.transport
    server.settings.SERVER_ADDRESS = args.host
    server.settings.SERVER_PORT = args.port

    # Save server
    _SERVER = server

    # Run server
    server.run()
    return
