---
title: How Domain Park protects your domains
description: A closer look at the DNS records that declare your domain does not send email, receive email, or serve a website.
order: 3
outline: true
---

## One DNS service for unused domains

- Explain authoritative DNS and delegation, with a simple lookup example.
- Describe how the software responds to supported queries without per-domain configuration.
- Identify examples below as responses from the source implementation, not a guarantee that every public server runs the same version or configuration.
- Review the [DNS implementation](https://github.com/nhairs/domain-park/blob/master/src/domain_park/server.py) when expanding this article, including query matching at the apex and subdomains.

## SPF: no authorised email senders

```text
v=spf1 -all
```

- Explain the SPF all mechanism, its hard-fail qualifier, and envelope-sender checks.
- Cover the implementation's apex and subdomain TXT handling.
- Explain why SPF alone is not the same as protecting the visible From header.

## DMARC: request rejection of unauthenticated email

```text
v=DMARC1; p=reject;
```

- Explain alignment, the visible From domain, and the reject policy.
- Explain that recipients decide how to handle messages and may override the requested policy.
- Cover optional aggregate and forensic reporting addresses as software configuration; do not claim they are enabled on the public service.
- Review subdomain policy inheritance before describing its limits.

## DKIM: publish no usable signing key

```text
v=DKIM1; p=
```

- Explain selectors and the empty public key returned by the selector-matching rules.
- Explain what an empty key means for signature validation, without describing it as a substitute for DMARC.

## Null MX: declare that email is not accepted

```text
0 .
```

- Explain Null MX and how it differs from having no MX record.
- Clarify that this controls receiving email, rather than authenticating outgoing email.
- Check the implementation's apex query scope when discussing subdomains.

## Address records and certificate issuance

```text
CAA 0 issue ";"
```

- Explain that the implementation returns no apex A or AAAA answers, so it does not provide a parking webpage on visitors' domains.
- Explain the CAA issue property and the empty issuer value.
- Review certificate-authority processing, wildcard handling, and operational limitations before making broad certificate guarantees.
- Avoid claiming this removes previously issued certificates.

## Limits and verification

- Summarise dependence on receiving mail systems, certificate-authority behaviour, correct delegation, and domain-account security.
- Explain what is outside this service: active mailboxes, attacker-owned lookalikes, and registrar-account compromise.
- Link to [the verification guide](/guides/verify-and-troubleshoot/) for practical checks.
