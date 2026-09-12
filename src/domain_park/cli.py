### IMPORTS
### ============================================================================
## Future
from __future__ import annotations

## Standard Library
import argparse

## Installed
import netifaces
import nserver.cli
import pillar

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


class Application(nserver.cli.CliApplication):
    """domain-park is a DNS Name Server that can be used to prevent spoofed emails on parked domains."""

    application_name = "domain-park"
    name = "domain_park"
    version = _version.get_version_info_full()
    epilog = (
        "For full information including licence see https://github.com/nhairs/domain-park\n\n"
        "Copyright (c) 2020 Nicholas Hairs"
    )
    config_args_enabled = False
    logging_manifest = pillar.application.LoggingManifest(
        console_format="[{asctime}][{log_color}{levelname}{reset}][{name}]: {message}",
        additional_namespaces=["nserver"],
    )  # type: ignore[call-arg]

    server: nserver.NameServer

    def get_argument_parser(self) -> argparse.ArgumentParser:
        parser = super().get_argument_parser()

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

        ## Remove --server action as we always load the domain-park server
        # pylint: disable=protected-access
        server_action = parser._option_string_actions.pop("--server")
        parser._actions.remove(server_action)
        parser._optionals._group_actions.remove(server_action)
        # pylint: enable=protected-access

        return parser

    def get_server(self) -> nserver.NameServer:
        """Get NameServer instance."""
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

        return make_server(nameservers, self.args.rua, self.args.ruf)
