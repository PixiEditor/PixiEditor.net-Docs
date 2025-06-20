import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
import { z } from 'astro/zod';
import { videosSchema } from 'starlight-videos/schemas';

export const collections = {
	docs: defineCollection({ loader: docsLoader(), schema: docsSchema({ 
		extend: 
			z.object({
				node: z.object({
					name: z.string(),
					category: z.string(),
					description: z.string(),
					isPair: z.boolean().optional().default(false),
					hasPreview: z.boolean().optional().default(false),
					icon: z.string().optional(),
					inputs: z.array(z.object({
						name: z.string(),
						type: z.string(),
						description: z.string().optional(),
						default: z.any().optional(),
					})).optional().nullable(),
				outputs: z.array(z.object({
						name: z.string(),
						type: z.string(),
						description: z.string().optional(),
					})).optional().nullable(),
					
				}).optional(),
			})
	}) }),
};
