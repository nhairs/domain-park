# Benchmarking Domain-park

Ideally `nsever` should be benchmarkable, but while it's not I'll document how to do DNS server benchmarking here.

## Setup

### Benchmarking tools

We will use the following tools:

- [jedicst11/dnsblast](https://github.com/jedisct1/dnsblast)
    - requires C compiler
- [sandeeprenjith/dnsblast](https://github.com/sandeeprenjith/dnsblast)
    - requires Go


There is a also [general list on senki.org](https://www.senki.org/network-operations-scaling/dns-latency-and-performance-test-tools/).

### Our tools

We will obviously need `domain-park` installed locally.

However to test production-like performance, we will need something to load-balance between `domain-park` instances. For this we will use [coredns](https://coredns.io/).

If we want to test response-rate-limiting or general ratelimiting we will need to compile this ourselves.

```shell
# install go if not already install
# https://go.dev/doc/install

git clone https://github.com/coredns/coredns.git

cd coredns

cat >> plugin.cfg <<EOF
rrl:github.com/coredns/rrl/plugins/rrl
ratelimit:github.com/milgradesec/ratelimit
EOF

make
```


## Testing

### Server Commands - single

Each of these commands need to run at the same time - easiest done through seperate terminals.

```shell
# coredns (if you want it)
./coredns -conf corefile-single

# domain-park
domain-park -n ns1.domain-park.org:178.128.60.87 --tcp --host localhost --port 5301
```

### Server Commands - multi

Same as single mode but more commands (use i3 to manage alllll these windows).

```shell
# coredns (required this time)
./coredns -conf corefile-multi

# domain-park
domain-park -n ns1.domain-park.org:178.128.60.87 --tcp --host localhost --port 5301
domain-park -n ns1.domain-park.org:178.128.60.87 --tcp --host localhost --port 5302
domain-park -n ns1.domain-park.org:178.128.60.87 --tcp --host localhost --port 5304
```

### Monitoring Sockets

A lot of the reason for doing these load tests is to check what is happening with socket state when in TCP mode.

```shell
sudo watch -n 0.5 ss -tna dport eq 5301
```

### Testing with jedicst11/dnsblast

```shell

# note coredns running on 5300, change to other port if testing domain-park directly.
# To test different query rates change this value:
#                         |
#                         V
dnsblast 127.0.0.1 100000 10 5300
```

**We can also use this version of dnsblast to fuzz**
This is more effective to run against `domain-park` directly than through `coredns` as we will find more errors with our python code if they are not being sanitised first.

```shell
# note need to run in UDP mode.
# unfortunately this means won't fuzz TCP connections
# we can somewhat fuzz TCP connections behind coredns. See above caveat.

domain-park -n ns1.domain-park.org:178.128.60.87 --udp --host localhost --port 5301

dnsblast fuzz 127.0.0.1 50000 100 5301
```

### Testing with sandeeprenjith/dnsblast

```shell
# this tool uses <sub>.<domain>.lab by default for testing
# domain-park doesn't have A records on subdomains, so use TXT instead

/dnsblast -s 127.0.0.1 -p 5300 -t 10 -type TXT -l 10
```
