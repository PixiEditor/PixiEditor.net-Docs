import os
import re
import yaml
from pathlib import Path

# Paths to your directories
nodes_dir = Path("../PixiEditor/src/PixiEditor.ChangeableDocument/Changeables/Graph/Nodes")
viewmodels_dir = Path("../PixiEditor/src/PixiEditor/ViewModels/Document/Nodes")
output_dir = Path("src/content/docs/usage/Node Graph/Nodes/")

# Match ViewModel metadata
viewmodel_pattern = re.compile(r'\[NodeViewModel\("([^"]+)",\s*"([^"]+)",\s*([^\)]+)\)\]')
pair_pattern = re.compile(r'\[PairNode\(typeof\(([^)]+)\)')
input_pattern = re.compile(r'Create(?:Func)?Input<([^>]+)>\("([^"]+)",\s*"([^"]+)"(?:,\s*(.+?))?\)')
output_pattern = re.compile(r'Create(?:Func)?Output<([^>]+)>\("([^"]+)",\s*"([^"]+)"(?:,\s*(.+?))?\)')
class_inheritance_pattern = re.compile(r'class\s+\w+\s*:\s*([^ {]+)')
interface_pattern = re.compile(r'class\s+\w+\s*:\s*[^,{]+,\s*([^ {]+)')

def screaming_to_words(text):
    return " ".join(word.capitalize() for word in text.split("_"))

def extract_viewmodel_metadata(file_content):
    match = viewmodel_pattern.search(file_content)
    if not match:
        return None
    name, category, icon = match.groups()
    return {
        "name": screaming_to_words(name),
        "category": screaming_to_words(category),
        "icon": f"icon-{icon.split('.')[-1].lower()}"
    }

def extract_node_metadata(file_content):
    metadata = {
        "isPair": bool(pair_pattern.search(file_content)),
        "hasPreview": "RenderNode" in file_content or "IPreviewRenderable" in file_content,
        "inputs": [],
        "outputs": []
    }

    for match in input_pattern.finditer(file_content):
        type_, name, label, default = match.groups()
        metadata["inputs"].append({
            "name": screaming_to_words(label),
            "type": type_.strip(),
            "default": default.strip() if default else None
        })

    for match in output_pattern.finditer(file_content):
        type_, name, label, default = match.groups()
        metadata["outputs"].append({
            "name": screaming_to_words(label),
            "type": type_.strip(),
            "default": default.strip() if default else None
        })

    return metadata

def to_kebab_case(name: str) -> str:
    # Convert PascalCase or camelCase to kebab-case
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    kebab = re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()
    return kebab

def merge_metadata(viewmodel_meta, node_meta):
    merged = {
        "name": viewmodel_meta["name"].replace("Node", ""),
        "category": viewmodel_meta["category"],
        "icon": viewmodel_meta["icon"],
        "isPair": node_meta.get("isPair", False),
        "hasPreview": node_meta.get("hasPreview", False),
        "inputs": node_meta.get("inputs") or None,
        "outputs": node_meta.get("outputs") or None,
        "description": "TODO: Add a description."
    }
    return merged

def write_mdx_file(metadata, name):
    title = f"{metadata['name']}"
    frontmatter = {
        "title": title,
        "node": metadata
    }

    yaml_frontmatter = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True)
    content = f"---\n{yaml_frontmatter}---\n"

    mdx_path = output_dir / f"{name}.mdx"
    if mdx_path.exists():
        print(f"Skipping {name}: File already exists.")
        return
    output_dir.mkdir(parents=True, exist_ok=True)

    new_content = content

    with mdx_path.open("w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    nodes = {f.name.replace("Node.cs", ""): f for f in nodes_dir.rglob("*Node.cs")}
    viewmodels = {f.name.replace("NodeViewModel.cs", ""): f for f in viewmodels_dir.rglob("*NodeViewModel.cs")}

    for key in sorted(set(nodes.keys()) & set(viewmodels.keys())):
        viewmodel_path = viewmodels[key]
        node_path = nodes[key]

        with viewmodel_path.open("r", encoding="utf-8") as f:
            vm_content = f.read()

        with node_path.open("r", encoding="utf-8") as f:
            node_content = f.read()

        viewmodel_meta = extract_viewmodel_metadata(vm_content)
        if not viewmodel_meta:
            print(f"Skipping {key}: No ViewModel metadata found.")
            continue

        node_meta = extract_node_metadata(node_content)
        merged = merge_metadata(viewmodel_meta, node_meta)

        write_mdx_file(merged, to_kebab_case(key))

if __name__ == "__main__":
    main()
