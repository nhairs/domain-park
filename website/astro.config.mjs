import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import { publicationBuild, siteConfig } from './src/config/site.ts';

export default defineConfig({
  site: siteConfig.siteUrl,
  output: 'static',
  trailingSlash: 'always',
  integrations: publicationBuild ? [sitemap({ filter: (page) => !page.endsWith('/404/') })] : [],
  vite: { plugins: [tailwindcss()] },
  markdown: {
    shikiConfig: { themes: { light: 'github-light', dark: 'github-dark' } },
  },
});
