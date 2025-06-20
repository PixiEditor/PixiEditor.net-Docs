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
						typeLink: z.string().optional(),
						min: z.string().optional(),
						max: z.string().optional(),
						hideSocket: z.boolean().optional().default(false),
						isContextful: z.boolean().optional().default(false),
						description: z.string().optional(),
						default: z.any().optional(),
					})).optional().nullable(),
				outputs: z.array(z.object({
						name: z.string(),
						type: z.string(),
						min: z.string().optional(),
						max: z.string().optional(),
						typeLink: z.string().optional(),
						hideSocket: z.boolean().optional().default(false),
						default: z.any().optional(),
						isContextful: z.boolean().optional().default(false),
						description: z.string().optional(),
					})).optional().nullable(),
					
				}).optional(),
			})
	}) }),
};
