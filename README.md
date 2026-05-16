# PixiEditor Docs

The Documentation for [PixiEditor](https://github.com/PixiEditor/PixiEditor)

Built with [Starlight](https://starlight.astro.build/getting-started/) and [Tailwind](https://tailwindcss.com/docs/)

## File Structure

All docs are located at `src/assets/docs`

Images can be added to `src/assets/`

### Usage

`src/contents/usage` contains documentation about the usage of PixiEditor, and is oriented towards the users of PixiEditor.

### Contribution

`src/contents/contribution` contains documentation on how to work on the source code of [PixiEditor](https://github.com/PixiEditor/PixiEditor)

It is oriented towards developers working on PixiEditor

## Developing & Running


### VS Code / VSCodium

Install yarn if you don't have it. Then run `yarn install` in the repo's core directory. Afterwards in go to the Run tab in VS Code  and run the `Development Server` launch configuration

<details>
    <summary>Development server seems to be running but http://localhost:4321/docs/ doesn't load?</summary>
    
    This can be caused by a VPN in running locally in TUN mode, try disabling the VPN or editing launch.json to run `astro dev --host` instead of `astro dev`
</details>

#### Recommended Extensions
* [Astro](https://marketplace.visualstudio.com/items?itemName=astro-build.astro-vscode)
* [Tailwind CSS](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)
* [MDX](https://marketplace.visualstudio.com/items?itemName=unifiedjs.vscode-mdx)

### CLI

```bash
yarn dev
```
