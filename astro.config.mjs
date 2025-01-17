// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
    integrations: [starlight({
        title: 'PixiEditor Docs',
        social: {
            github: 'https://github.com/PixiEditor/PixiEditor',
        },
        customCss: [
            './src/tailwind.css'
        ],
        sidebar: [
            // {
            // 	label: 'Guides',
            // 	items: [
            // 		// Each item here is one entry in the navigation menu.
            // 		{ label: 'Example Guide', slug: 'guides/example' },
            // 	],
            // },
            // {
            // 	label: 'Reference',
            // 	autogenerate: { directory: 'reference' },
            // },
            {
                label: 'Getting Started 🏠',
                autogenerate: { directory: 'getting-started' },
            },
            {
                label: 'Open Beta 🚀',
                autogenerate: { directory: 'open-beta' },
            },
            {
                label: 'Usage 🎮',
                autogenerate: { directory: 'usage' },
            },
            {
                label: 'Contributing 💻',
                autogenerate: { directory: 'contribution' },
            },
            {
                label: 'Color Picker 🎨',
                autogenerate: { directory: 'color-picker' },
            },
            {
                label: 'Other 🔍',
                autogenerate: { directory: 'other' },
            },
        ],
		}), tailwind({
            applyBaseStyles: false
        })],
});