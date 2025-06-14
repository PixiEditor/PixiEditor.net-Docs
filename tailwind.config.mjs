import starlightPlugin from '@astrojs/starlight-tailwind';

// Generated color palettes

/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
		},
	},
	plugins: [starlightPlugin()],
};