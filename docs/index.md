# domain-park.org
Domain-park is an open-source DNS Name server that implements best practice MX, SPF, DKIM, and DMARC DNS records in order to prevent spoofing of registered but unused domain names. For more detail on what this means, check out the [domain-park announcement post on nicholashairs.com](https://www.nicholashairs.com/posts/preventing-email-spoofing-on-unused-domains/).

There are two ways that you can take advantage of domain-park. The easiest way is to use our free public servers. If you want more control, you can also run your own private server.

**Note: the `domain-park` software and domain-park.org are currently in alpha release and may be prone to bugs, down-time, or other unexpected behaviour.** Please report bugs via [GitHub issues](https://github.com/nhairs/domain-park/issues).

# Free Public Servers
In order to make these protections available to all, domain-park.org has free to use public name servers. In order to use these name servers you will need to update the name servers used by each domain to one or more of the following name servers:

```
ns1.domain-park.org
ns2.domain-park.org
ns3.domain-park.org
ns4.domain-park.org
```

The process of updating your name server will be dependent on where your domain is registered. They will have documentation on how to do this, but there are too many to list them here.

## Disclaimer
Although care is taken in the operation of domain-park.org, using a third-party name server to manage your domains does come with risks. If these risks are unacceptable to you or your organisation then you should not use the public servers and consider running your own instance of domain-park.


# Private Servers
In order to run your own instance of domain-park you will need a server with a publicly accessible IP address and Python 3.6+. For installation and usage refer to the [readme on GitHub](https://github.com/nhairs/domain-park). Currently domain-park has only been tested on Ubuntu.

# Author
The domain-park software and domain-park.org website have been created by [Nicholas Hairs](https://www.nicholashairs.com) - a security professional working in Australian tech.
