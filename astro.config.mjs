// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://pixieditor.net',
  base: '/docs/',

  integrations: [starlight({
      title: 'PixiEditor Docs',
      editLink: {
          baseUrl: "https://github.com/PixiEditor/PixiEditor.net-Docs/tree/main",
      },
      social: [
          { icon: 'github', label: 'GitHub', href: 'https://github.com/PixiEditor/PixiEditor' },
          { icon: 'discord', label: 'Discord', href: "https://discord.gg/qSRMYmq" }
      ],
      logo: {
          light: './src/assets/logo-light.svg',
          dark: './src/assets/logo-dark.svg',
          replacesTitle: true
      },
      customCss: [
          './src/styles/global.css'
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
      })],

  vite: {
    plugins: [tailwindcss()],
  },
});