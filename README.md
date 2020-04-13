# Domain Park: Prevent abuse of parked domains

[![PyPi](https://img.shields.io/pypi/v/domain-park.svg)](https://pypi.python.org/pypi/domain-park/)
[![Python Versions](https://img.shields.io/pypi/pyversions/domain-park.svg)](https://github.com/nhairs/domain-park)
[![License](https://img.shields.io/github/license/nhairs/domain-park.svg)](https://github.com/nhairs/domain-park/blob/master/LICENCE)

`domain-park` is an open-source DNS Name server that implements best practice `MX`, SPF, DKIM, and DMARC DNS records in order to prevent spoofing of registered but unused domain names (also known as parked domains).

**Features:**
- Implement best practice DNS records for SPF, DKIM, DMARC, MX compliance.
- Handle unlimited domains with little to no configuration.
- Setup receiving of DMARC aggregate reports.

`domain-park` is currently Alpha software and does not have complete documentation, testing, or implementation of certain features.

This page is for the domain-park software, you may be looking for the [domain-park.org](https://www.domain-park.org) public name servers.

## Installation
### Install via pip
```shell
pip3 install --user domain-park
```

## Usage
```
domain-park --help
usage: domain-park [-h] [--version] [--host HOST] [--port PORT]
                   [--tcp | --udp] -n NAMESERVER [--rua EMAIL] [--ruf EMAIL]
                   [--ips]

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --host HOST           Host (IP) to bind to. Use --ips to see available.
                        Defaults to localhost.
  --port PORT           Port to bind to. Defaults to 9953.
  --tcp                 Use TCPv4 socket for transport.
  --udp                 Use UDPv4 socket for transport. (default)
  -n NAMESERVER, --nameserver NAMESERVER
                        Add NameServer to list returned on NS lookups. This
                        should be equal to the NS records available publicly
                        running domain-park. Must be supplied at least once,
                        and has no limit. Reccomended to have 2-4 Name
                        Servers. Expected to be in the format of either
                        'FQDN:IP' or 'IP'
  --rua EMAIL           Email address to use for DMARC aggregate repots.
  --ruf EMAIL           Email address to use for DMARC forensic reports.
  --ips                 Print available IPs and exit
```

Example:
```shell
domain-park -n ns1.domain-park.org -n ns2.domain-park.org
```

Once running, interact using `dig`:

```shell
dig -p 9953 @localhost NS example.com

dig -p 9953 @localhost TXT example.com
dig -p 9953 @localhost TXT foo.example.com

dig -p 9953 @localhost TXT _dmarc.example.com

dig -p 9953 @localhost TXT asdf._domainkey.example.com
dig -p 9953 @localhost TXT qwer._domainkey.foo.example.com

dig -p 9953 @localhost MX example.com
```

## Production Usage
In order to setup domain-park for use with publicly accessible domains, you will need a static IP address for the server running `domain-park` and a domain which you can set records on.

On your domain you will need to create an `A` for your name server using the static IP address. Once done you will then need to create a [glue record](https://en.wikipedia.org/wiki/Domain_Name_System#Circular_dependencies_and_glue_records) for the previously created `A` record.


## Bugs, Feature Requests etc
TLDR: Please [submit an issue on github](https://github.com/nhairs/domain-park/issues).

In the case of bug reports, please help me help you by following best practices [[1](https://marker.io/blog/write-bug-report/)] [[2](https://www.chiark.greenend.org.uk/~sgtatham/bugs.html)].

In the case of feature requests, please provide background to the problem you are trying to solve so to help find a solution that makes the most sense for the library as well as your usecase.

## Development
The only development dependency is bash and docker. All actions are run within docker for ease of use. See `./dev.sh help` for commands. Typical commands are `format`, `lint`, `test`, `repl`, `build`.

I am still working through open source licencing and contributing, so not taking PRs at this point in time. Instead raise and issue and I'll try get to it as soon a feasible.

## Licence
This project is licenced under the MIT Licence - see [`LICENCE`](https://github.com/nahirs/domain-park/blob/master/LICENCE).

This project includes other open source licenced software - see [`NOTICE`](https://github.com/nhairs/domain-park/blob/master/NOTICE).

## Authors
A project by Nicholas Hairs - [www.nicholashairs.com](https://www.nicholashairs.com).
