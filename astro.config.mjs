// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

import tailwindcss from '@tailwindcss/vite';
import starlightVideos from 'starlight-videos';
import starlightImageZoom from 'starlight-image-zoom';
import fs from 'node:fs';
import path from 'node:path';


function getFiles(directory) {
    return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
        const fullPath = path.join(directory, entry.name);

        if (entry.isDirectory())
            return getFiles(fullPath);

        return fullPath;
    });
}

function slugifyPath(path) {
    return path
        .split('/')
        .map(segment =>
            segment
                .toLowerCase()
                .trim()
                .replace(/[^a-z0-9]+/g, '-')
                .replace(/^-+|-+$/g, '')
        )
        .join('/');
}

const usageDirectory = './src/content/docs/handbook';
const redirects = {};

for (const file of getFiles(usageDirectory)) {
    if (!file.endsWith('.md') && !file.endsWith('.mdx'))
        continue;

    const relative = path.relative(usageDirectory, file)
        .replace(/\\/g, '/')
        .replace(/\.(md|mdx)$/, '');

    const slug = slugifyPath(relative);

    redirects[`/usage/${slug}`] = `/docs/handbook/${slug}`;
}

console.log(redirects);

// https://astro.build/config
export default defineConfig({
  site: 'https://pixieditor.net',
  base: '/docs/',
  redirects: redirects,

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
              label: 'Handbook',
              autogenerate: { directory: 'handbook' },
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