// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

import tailwindcss from '@tailwindcss/vite';
import starlightVideos from 'starlight-videos';
import starlightImageZoom from 'starlight-image-zoom';

// https://astro.build/config
export default defineConfig({
  site: 'https://pixieditor.net',
  base: '/docs/',

  integrations: [starlight({
      title: 'PixiEditor Docs',
      plugins: [starlightVideos(), starlightImageZoom()],
      components: {
            MarkdownContent: './src/components/overrides/MarkdownContent.astro',
      },
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
          {
              label: 'Development Channel',
              autogenerate: { directory: 'open-beta' },
          },
          {
              label: 'Usage',
              autogenerate: { directory: 'usage' },
              collapsed: true,
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