import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const guides = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/guides' }),
  schema: z.object({
    title: z.string().min(1),
    description: z.string().min(1),
    order: z.number().int().positive(),
    icon: z.enum(['question', 'wrench', 'shield', 'search']),
    outline: z.boolean().default(true),
  }),
});

export const collections = { guides };
