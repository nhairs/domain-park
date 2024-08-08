# domain-park.org

Domain-park.org is a free service for securely parking unused domains:

- **Prevents Email Spoofing**: protect your staff, your customers, and the general public from phishing emails using your unused domains.
  - Implements best practice MX, [SPF, DKIM, and DMARC](https://www.cyber.gov.au/resources-business-and-government/maintaining-devices-and-systems/system-hardening-and-administration/email-hardening/how-combat-fake-emails) records.
- **Prevents Domain Takeover**: avoid domains becoming [Sitting Ducks](https://krebsonsecurity.com/2024/07/dont-let-your-domain-name-become-a-sitting-duck/).
  - Check if your DNS provider is vulnerable to DNS takeover [here](https://github.com/indianajson/can-i-take-over-dns?tab=readme-ov-file).
- **Simple Setup**: just set domain-park.org as your name servers, no signup or further configuration required.
  - Many registrars will let you update in bulk or set default name servers for new domains, why not use domain-park.org to quickly protect your domains?
- **Free**: using the public domain-park.org name servers is free no matter how many domains you have.

# Free Public Namer Servers
In order to use these name servers you will need to update the name servers used by each domain to one or more of the following name servers:

```
ns1.domain-park.org
ns2.domain-park.org
ns3.domain-park.org
ns4.domain-park.org
```

The process of updating your name server will be dependent on where your domain is registered.

# Author
The domain-park software and domain-park.org website have been created by [Nicholas Hairs](https://www.nicholashairs.com).

For more information you can check out the [domain-park announcement post on nicholashairs.com](https://www.nicholashairs.com/posts/preventing-email-spoofing-on-unused-domains/).
