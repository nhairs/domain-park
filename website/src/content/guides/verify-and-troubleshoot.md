---
title: How to check your domain is securely parked
description: Verify your nameserver delegation and DNS responses, and work through common setup problems.
order: 4
outline: true
---

## Check the delegation first

- Explain how to inspect the registrar settings and the parent-zone delegation.
- Show how recursive answers can remain cached, and explain the difference between a lookup and a delegation trace.
- Replace example.com with a domain the reader owns when running checks.

```sh
dig NS example.com
dig +trace NS example.com
```

## Query the authoritative nameservers

- Explain direct authoritative queries and repeating the checks against all four configured nameservers.
- Present expected responses alongside the final prose, after checking the live public service.
- Explain that an authoritative answer from a server alone does not prove the parent zone delegates to it.

```sh
dig @ns1.domain-park.org example.com TXT
dig @ns1.domain-park.org _dmarc.example.com TXT
dig @ns1.domain-park.org selector._domainkey.example.com TXT
dig @ns1.domain-park.org example.com MX
dig @ns1.domain-park.org example.com CAA
dig @ns1.domain-park.org example.com A
dig @ns1.domain-park.org example.com AAAA
```

## Understand the expected responses

- Cover SPF hard fail, DMARC reject, an empty DKIM key, Null MX, restrictive CAA, and absent apex address answers.
- Explain answer sections, authority sections, return codes, and why an empty answer is not automatically an error.
- Link to [the protection guide](/guides/how-protection-works/) for the meaning and limits of each record.

## Troubleshoot common problems

- Previous nameservers still appear: confirm the saved delegation and account for caching.
- Registrar refuses the update: check spelling and consult official registrar instructions.
- SERVFAIL after migration: examine delegation, nameserver reachability, and stale DNSSEC DS records.
- One nameserver differs from the others: capture answers, timestamps, and the server queried.
- A previously active service stops working: revisit the suitability check and restore the appropriate DNS provider if needed.

## Recheck later and ask for help

- Suggest periodic checks for retained and defensively registered domains.
- Provide a troubleshooting-report checklist: domain, record type, queried server, command, response, and time.
- Link to [GitHub issues](https://github.com/nhairs/domain-park/issues) and explain that issue reports are public.
