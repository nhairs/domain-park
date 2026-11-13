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

Also note that Domain Park does **not** support subdomains, only use it for your registered domain.

## Update your nameservers

Navigate to the domain management settings of your domain provider and set the nameservers to our servers:

```
ns1.domain-park.org
ns2.domain-park.org
ns3.domain-park.org
ns4.domain-park.org
```

As many providers will include DNS, you may need to first select a setting such as "external", "custom", or "I'll use my own nameservers" in the domain management settings. The exact process for this will vary between providers, so follow the [official provider instructions](#provider-nameserver-guides).

That's it. You're done. 🥳

It can still take 48 hours for the parking to take affect as some caches may still be using your old nameservers.

If you're an IT admin looking after a large number of domains you should consider using your providers bulk settings or infrastructure as code to make the change as a batch.

## Verify the changes

[TODO: update this]

- Explain caching and why different resolvers may show different results temporarily.
- Avoid a guaranteed propagation time; cover provider and TTL variation.
- Link to [verification and troubleshooting](/guides/verify-and-troubleshoot/).

## Provider nameserver guides

Follow your provider's instructions for changing the nameservers of a domain registered with them. When entering custom nameservers, use the four Domain Park nameservers listed in [Update your nameservers](#update-your-nameservers).

- [123 Reg](https://www.123-reg.co.uk/support/domains/how-do-i-change-the-nameservers-for-my-domain-name/)
- [Alibaba Cloud](https://www.alibabacloud.com/help/en/dws/user-guide/modify-dns-server)
- [AWS Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-register-other-dns-service.html)
- [BigRock](https://www.bigrock.in/help/article/Change-the-Name-Servers-of-a-Domain-Name-in-BigRock)
- [Bluehost](https://www.bluehost.com/help/article/custom-nameservers)
- [Crazy Domains](https://www.crazydomains.com/help/article/change-the-name-servers-of-your-cd-domain)
- [DreamHost](https://help.dreamhost.com/hc/en-us/articles/360038897151-Changing-your-nameservers-at-DreamHost)
- [Dynadot](https://www.dynadot.com/help/question/set-name-servers)
- [Enom](https://support.enom.com/support/solutions/articles/201000065375-nameservers-ns-)
- [Gandi](https://docs.gandi.net/en/domain_names/common_operations/changing_nameservers.html)
- [GoDaddy](https://www.godaddy.com/en-au/help/change-my-domain-nameservers-664)
- [Google Cloud Domains](https://docs.cloud.google.com/domains/docs/edit-registration-settings#edit-dns-settings)
- [HostGator](https://www.hostgator.com/help/article/i-bought-my-domain-from-hostgator-how-do-i-make-dns-changes)
- [Hostinger](https://www.hostinger.com/support/1696789-how-to-change-nameservers-at-hostinger/)
- [Hover](https://support.hover.com/support/solutions/articles/201000064742-changing-your-domain-nameservers)
- [IONOS](https://www.ionos.com/help/domains/using-your-own-name-servers/using-your-own-name-servers-for-a-domain/)
- [Name.com](https://www.name.com/support/articles/205934547-changing-nameservers-for-dns-management)
- [Namecheap](https://www.namecheap.com/support/knowledgebase/article.aspx/767/10/how-to-change-dns-for-a-domain/)
- [NameSilo](https://www.namesilo.com/support/v2/services-faq/domain/1.2)
- [Network Solutions](https://www.networksolutions.com/help/article/manage-dns-adns-records)
- [OVHcloud](https://docs.ovhcloud.com/en/guides/web-cloud/domains/dns-server-edit)
- [Porkbun](https://kb.porkbun.com/article/22-how-to-change-nameservers)
- [SiteGround](https://www.siteground.com/kb/how_to_change_my_ns_record)
- [Spaceship](https://www.spaceship.com/knowledgebase/connect-domain-custom-nameservers/)
- [Squarespace](https://support.squarespace.com/hc/en-us/articles/4404183898125-Review-change-or-reset-your-domain-s-nameservers)
- [Tencent Cloud](https://www.tencentcloud.com/document/product/242/42867)
- [Vercel](https://vercel.com/docs/domains/managing-nameservers)
- [WordPress.com](https://wordpress.com/support/domains/change-name-servers/)

Some providers restrict changes to external nameservers. Cloudflare Registrar requires you to transfer your domain to another registrar before using a different DNS provider. See [Cloudflare's nameserver guidance](https://developers.cloudflare.com/dns/nameservers/update-nameservers/).

For domains purchased through Azure App Service Domains, Microsoft support directs customers to transfer the domain to another registrar to change nameservers. See [Microsoft's guidance on changing App Service domain nameservers](https://learn.microsoft.com/en-us/answers/questions/2283480/unable-to-change-nameservers-for-azure-app-service).

## Unparking your domain

If you decide that you'd like to stop using Domain Park you simply need to change your nameservers back to their original settings, or a new DNS provider.

When doing so, you should wait at least 48 hours before you attempt to use the new domain as some caches may still be using the Domain Park nameservers.
