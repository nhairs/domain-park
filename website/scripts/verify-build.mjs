import assert from 'node:assert/strict';
import { readFile, readdir, stat } from 'node:fs/promises';
import { resolve, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { siteConfig } from '../src/config/site.ts';

const root = fileURLToPath(new URL('../dist/', import.meta.url));
const origin = new URL(siteConfig.siteUrl);
const failures = [];
const check = (condition, message) => { if (!condition) failures.push(message); };
const attributes = (tag) => Object.fromEntries(
  Array.from(tag.matchAll(/([\w:-]+)\s*=\s*"([^"]*)"/g), (match) => [match[1], match[2]]),
);
const tags = (html, name) => Array.from(html.matchAll(new RegExp(`<${name}\\b[^>]*>`, 'gi')), (match) => attributes(match[0]));
const exists = async (path) => { try { return (await stat(path)).isFile(); } catch { return false; } };
async function walk(path) {
  const entries = await readdir(path, { withFileTypes: true });
  const files = await Promise.all(entries.map((entry) => entry.isDirectory() ? walk(join(path, entry.name)) : [join(path, entry.name)]));
  return files.flat();
}

const files = await walk(root);
const pages = files.filter((path) => path.endsWith('.html'));
const titles = new Set();
const descriptions = new Set();
const pageCache = new Map();
let checkedLinks = 0;
const fileForUrl = async (url) => {
  // Astro renders the /404/ route into GitHub Pages' special 404.html file.
  if (url.pathname === '/404/') return join(root, '404.html');
  const target = resolve(root, `.${decodeURIComponent(url.pathname)}`);
  assert(!relative(root, target).startsWith('..'), `Path outside build: ${url.href}`);
  if (await exists(target)) return target;
  const index = join(target, 'index.html');
  return await exists(index) ? index : undefined;
};

for (const path of pages) {
  const html = await readFile(path, 'utf8');
  pageCache.set(path, html);
  const name = relative(root, path);
  const route = name === '404.html' ? '/404/' : `/${name.replace(/index\.html$/, '')}`;
  const title = html.match(/<title>([\s\S]*?)<\/title>/i)?.[1];
  check(Boolean(title) && !titles.has(title), `${name}: missing or duplicate title`);
  titles.add(title);
  const metas = tags(html, 'meta');
  const description = metas.find((meta) => meta.name === 'description')?.content;
  check(Boolean(description) && !descriptions.has(description), `${name}: missing or duplicate description`);
  descriptions.add(description);
  check(tags(html, 'h1').length === 1, `${name}: expected exactly one h1`);
  const canonical = tags(html, 'link').find((link) => link.rel === 'canonical')?.href;
  check(canonical === new URL(route, origin).href, `${name}: incorrect canonical ${canonical}`);
  const robots = metas.find((meta) => meta.name === 'robots')?.content;
  check(Boolean(robots), `${name}: missing robots metadata`);
  const isReview = html.includes('Article outline · for review') || (await readFile(join(root, 'robots.txt'), 'utf8')).includes('Disallow: /');
  check(!isReview || robots?.includes('noindex'), `${name}: review content must be noindex`);
  check(name !== '404.html' || robots?.includes('noindex'), `${name}: 404 must be noindex`);
  for (const property of ['og:title', 'og:description', 'og:url', 'og:image']) {
    check(Boolean(metas.find((meta) => meta.property === property)?.content), `${name}: missing ${property}`);
  }
  check(metas.find((meta) => meta.property === 'og:url')?.content === canonical, `${name}: Open Graph URL differs from canonical`);
  check(metas.find((meta) => meta.property === 'og:image')?.content === new URL(siteConfig.ogImage, origin).href, `${name}: incorrect social image URL`);
  check(Boolean(metas.find((meta) => meta.name === 'twitter:card')), `${name}: missing social card`);
  check(!/maria-lake|hello@maria|nextpoint|cookie-consent|googletagmanager|google-analytics/i.test(html), `${name}: template demo or tracking content remains`);
  check(!tags(html, 'script').some((script) => script.src?.startsWith('http')), `${name}: unexpected third-party script`);
  for (const tag of [...tags(html, 'a'), ...tags(html, 'link'), ...tags(html, 'script'), ...tags(html, 'img')]) {
    const href = tag.href || tag.src;
    if (!href || /^(mailto:|tel:|data:)/.test(href)) continue;
    const url = new URL(href.replaceAll('&amp;', '&'), new URL(route, origin));
    if (url.origin !== origin.origin) continue;
    const target = await fileForUrl(url);
    check(Boolean(target), `${name}: broken local link or asset ${href}`);
    checkedLinks++;
    if (target?.endsWith('.html') && url.hash) {
      const targetHtml = pageCache.get(target) ?? await readFile(target, 'utf8');
      pageCache.set(target, targetHtml);
      const ids = Array.from(targetHtml.matchAll(/\bid="([^"]+)"/g), (match) => match[1]);
      check(ids.includes(decodeURIComponent(url.hash.slice(1))), `${name}: missing fragment ${href}`);
    }
  }
}

const guideFiles = (await readdir(fileURLToPath(new URL('../src/content/guides/', import.meta.url)))).filter((name) => name.endsWith('.md'));
for (const name of guideFiles) {
  check(await exists(join(root, 'guides', name.replace(/\.md$/, ''), 'index.html')), `Missing guide page: ${name}`);
}
const homepage = await readFile(join(root, 'index.html'), 'utf8');
for (const name of siteConfig.nameservers) check(homepage.includes(`<code>${name}</code>`), `Homepage missing nameserver: ${name}`);
check((await readFile(join(root, 'CNAME'), 'utf8')).trim() === origin.hostname, 'Incorrect custom-domain CNAME');
check(await exists(join(root, siteConfig.ogImage.slice(1))), 'Missing social image');
const robots = await readFile(join(root, 'robots.txt'), 'utf8');
if (robots.includes('Allow: /')) {
  check(robots.includes(`${siteConfig.siteUrl}/sitemap-index.xml`), 'Incorrect sitemap URL in robots.txt');
  check(await exists(join(root, 'sitemap-index.xml')), 'Missing production sitemap index');
  const sitemapFiles = files.filter((file) => /sitemap-\d+\.xml$/.test(file));
  const sitemap = (await Promise.all(sitemapFiles.map((file) => readFile(file, 'utf8')))).join('');
  for (const page of pages.filter((file) => !file.endsWith('404.html'))) {
    const route = `/${relative(root, page).replace(/index\.html$/, '')}`;
    check(sitemap.includes(new URL(route, origin).href), `Production sitemap missing ${route}`);
  }
  check(!sitemap.includes(`${siteConfig.siteUrl}/404/`), '404 appears in sitemap');
  check(!homepage.includes('Preview outline'), 'Production homepage still links to outlines');
}
assert.equal(failures.length, 0, failures.join('\n'));
console.log(`Verified ${pages.length} pages, ${guideFiles.length} guides, and ${checkedLinks} internal links/assets.`);
