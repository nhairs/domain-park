export const siteConfig = {
  name: 'domain-park.org',
  title: 'Domain Park — Securely park your unused domains',
  description:
    'Free public DNS nameservers for unused domains. Help protect your staff, customers, and the public from email spoofing.',
  siteUrl: 'https://www.domain-park.org',
  authorName: 'Nicholas Hairs',
  authorUrl: 'https://www.nicholashairs.com',
  repositoryUrl: 'https://github.com/nhairs/domain-park',
  announcementUrl:
    'https://www.nicholashairs.com/posts/preventing-email-spoofing-on-unused-domains/',
  ogImage: '/og-image.png',
  nameservers: [
    'ns1.domain-park.org',
    'ns2.domain-park.org',
    'ns3.domain-park.org',
    'ns4.domain-park.org',
  ],
} as const;

export const publicationBuild = process.env.PUBLICATION_BUILD === 'true';
