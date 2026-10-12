---
title: How to set up Domain Park
description: Change the nameservers at your registrar, then check that your unused domain is delegated correctly.
order: 2
outline: true
---

## Before changing your nameservers

- Confirm that the domain is genuinely unused, including its subdomains.
- Record existing DNS settings and check for websites, email, forwarding, verification records, and other dependencies.
- Explain that changing delegation replaces the current DNS service; Domain Park does not preserve custom records.
- Add reviewed guidance for domains with DNSSEC enabled: check existing DS records and registrar procedures before changing DNS providers. Do not imply Domain Park supports DNSSEC without verifying the public service.

## Find the nameserver settings at your registrar

- Explain the difference between the registrar's nameserver/delegation settings and adding NS records inside a DNS zone.
- Use provider-neutral terminology: domain management, DNS settings, custom nameservers.
- Mention that some registrars support bulk updates or default nameservers for future registrations.

## Replace the current delegation

- Direct readers to use all four nameservers shown on the [homepage](/#nameservers-title).
- Explain how to replace the previous nameserver entries and save the change.
- Confirm that the public service needs no signup or per-domain configuration.
- Explain that registrar validation behaviour varies; add troubleshooting instructions after testing the public service.

## Allow the change to propagate

- Explain caching and why different resolvers may show different results temporarily.
- Avoid a guaranteed propagation time; cover provider and TTL variation.
- Link to [verification and troubleshooting](/guides/verify-and-troubleshoot/).

## Official registrar instructions

- Add links to official registrar documentation when the final prose is written.
- Select providers based on the intended readers; record the date each link and procedure was checked.
- Prefer documentation about changing authoritative nameservers, rather than editing individual DNS records.

## If you need to use the domain again

- Outline preparing a replacement DNS provider before changing delegation back.
- Explain that live email and websites require appropriate records at the new provider.
- Include a final verification step and a link to the protection guide for context.
