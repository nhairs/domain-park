import type { APIRoute } from 'astro';
import { publicationBuild, siteConfig } from '../config/site';

export const GET: APIRoute = () => new Response(
  publicationBuild
    ? `User-agent: *\nAllow: /\nSitemap: ${siteConfig.siteUrl}/sitemap-index.xml\n`
    : 'User-agent: *\nDisallow: /\n',
  { headers: { 'Content-Type': 'text/plain; charset=utf-8' } },
);
