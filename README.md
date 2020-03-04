# Domain Park: Prevent abuse of parked domains

[![PyPi](https://img.shields.io/pypi/v/domain-park.svg)](https://pypi.python.org/pypi/domai-park/)
[![Python Versions](https://img.shields.io/pypi/pyversions/domain-park.svg)](https://github.com/nhairs/domain-park)
[![License](https://img.shields.io/github/license/nhairs/domain-park.svg)](https://github.com/nhairs/domain-park/blob/master/LICENCE)

`domain-park` is a DNS Name Server designed to prevent spoofed emails on parked domains.

*Features:*
- Implement best practice DNS records for SPF, DKIM, DMARC, MX compliance.
- Handle unlimited domains with little to no configuration.

`domain-park` is currently Alpha software and does not have complete documentation, testing, or implementation of certain features.

## Installation
### Install via pip
```shell
pip3 install --user domain-park
```

## Usage
```
domain-park --help
usage: domain-park [-h] [--version] [--host HOST] [--port PORT]
                   [--tcp | --udp] [--ips]

optional arguments:
  -h, --help   show this help message and exit
  --version    show program's version number and exit
  --host HOST  Host (IP) to bind to. Use --ips to see available. Defaults to
               localhost.
  --port PORT  Port to bind to. Defaults to 9953.
  --tcp        Use TCPv4 socket for transport.
  --udp        Use UDPv4 socket for transport. (default)
  --ips        Print available IPs and exit
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


## Bugs, Feature Requests etc
TLDR: Please [submit an issue on github](https://github.com/nhairs/domain-park/issues).

In the case of bug reports, please help me help you by following best practices [[1](https://marker.io/blog/write-bug-report/)] [[2](https://www.chiark.greenend.org.uk/~sgtatham/bugs.html)].

In the case of feature requests, please provide background to the problem you are trying to solve so to help find a solution that makes the most sense for the library as well as your usecase.

## Development
The only development dependency is bash and docker. All actions are run within docker for ease of use. See `./dev.sh help` for commands. Typical commands are `format`, `lint`, `test`, `repl`, `build`.

I am still working through open source licencing and contributing, so not taking PRs at this point in time. Instead raise and issue and I'll try get to it as soon a feasible.

## Licence
This project is licenced under the MIT Licence - see [`LICENCE`](https://github.com/nahirs/domain-park/blob/master/LICENCE).

This project may include other open source licenced software - see [`NOTICE`](https://github.com/nhairs/domain-park/blob/master/NOTICE).

## Authors
A project by Nicholas Hairs - [www.nicholashairs.com](https://www.nicholashairs.com).
