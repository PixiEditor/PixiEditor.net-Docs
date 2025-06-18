// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

import tailwindcss from '@tailwindcss/vite';
import starlightVideos from 'starlight-videos';

// https://astro.build/config
export default defineConfig({
  site: 'https://pixieditor.net',
  base: '/docs/',

  integrations: [starlight({
      title: 'PixiEditor Docs',
      plugins: [starlightVideos()],
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
              label: 'Open Beta',
              autogenerate: { directory: 'open-beta' },
          },
          {
              label: 'Usage',
              autogenerate: { directory: 'usage' },
          },
          {
              label: 'Contributing',
              autogenerate: { directory: 'contribution' },
              collapsed: true,
          },
          {
              label: 'Color Picker',
              autogenerate: { directory: 'color-picker' },
              collapsed: true,
          },
          {
              label: 'Other',
              autogenerate: { directory: 'other' },
              collapsed: true,
          },
      ],
      })],

  vite: {
    plugins: [tailwindcss()],
  },
});