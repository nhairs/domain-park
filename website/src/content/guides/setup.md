---
title: How to set up Domain Park
description: Park your unused domains with Domain Park, from changing nameservers at your domain provider to checking the setup.
icon: wrench
order: 2
outline: false
---

So you've decided to securely park your domains, but what's next?

Parking your domains on domain-park.org is a straight forward process that can be done in less than 10 minutes.

## Preparing to use Domain Park

Before you park your domain you should make sure it's not being used. This includes checking for existing websites, email servers, and subdomains. You should also backup your DNS records as not all providers will retain them when chaning nameservers.

Parking your domain will mean that all these services will become inaccessible using this name, and although the process is reversible, it can take up 48 hours to reverse the change.

You will also need to make sure that you have access to the *name server settings* for that domain. This will usually be on the website where you registered your domain.

If you are using DNSSEC you will need to disable this for your domain - Domain Park does not currently support DNSSEC.

## Update your nameservers

Navigate to the domain management settings of your domain provider and set the nameservers to our servers:

```
ns1.domain-park.org
ns2.domain-park.org
ns3.domain-park.org
ns4.domain-park.org
```

As many providers will include DNS, you may need to first select a setting such as "external", "custom", or "I'll use my own nameservers" in the domain management settings. The exact process for this will vary between providers so we've linked the official instructions of popular providers below. [TODO: how to link to heading]

That's it. You're done. 🥳

It can still take 48 hours for the parking to take affect as some caches may still be using your old nameservers.

If you're an IT admin looking after a large number of domains you should consider using your providers bulk settings or infrastructure as code to make the change as a batch.

## Verify the changes

[TODO: update this]

- Explain caching and why different resolvers may show different results temporarily.
- Avoid a guaranteed propagation time; cover provider and TTL variation.
- Link to [verification and troubleshooting](/guides/verify-and-troubleshoot/).

## Provider nameserver guides

[TODO: generate alphabetical list, there's probably at least 20 providers]

- [AWS](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-register-other-dns-service.html)
- [Gandi](https://docs.gandi.net/en/domain_names/common_operations/changing_nameservers.html)
- [GoDaddy](https://www.godaddy.com/en-au/help/change-my-domain-nameservers-664)
- [Squarespace](https://support.squarespace.com/hc/en-us/articles/4404183898125-Review-change-or-reset-your-domain-s-nameservers)

## Unparking your domain

If you decide that you'd like to stop using Domain Park you simply need to change your nameservers back to their original settings, or a new DNS provider.

When doing so, you should wait at least 48 hours before you attempt to use the new domain as some caches may still be using the Domain Park nameservers.
