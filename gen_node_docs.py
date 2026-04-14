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
input_pattern_generic = re.compile(
    r'Create(?:(?P<kind>Func))?Input<([^>]+)>\(([^,]+),\s*"([^"]+)"(?:,\s*(.+?))?\)'
)

output_pattern_generic = re.compile(
    r'Create(?:(?P<kind>Func))?Output<([^>]+)>\(([^,]+),\s*"([^"]+)"(?:,\s*(.+?))?\)'
)

# Non-generic inputs/outputs
input_pattern_nongeneric = re.compile(
    r'Create(?:(?P<kind>Func|Render|SyncedType))?Input\(([^,]+),\s*"([^"]+)"(?:,\s*(.+?))?\)'
)

output_pattern_nongeneric = re.compile(
    r'Create(?:(?P<kind>Func|Render|SyncedType))?Output\(([^,]+),\s*"([^"]+)"(?:,\s*(.+?))?\)'
)

property_pattern = re.compile(
    r'public\s+(InputProperty|FuncOutputProperty|OutputProperty|FuncInputProperty)<([^>]+)>\s+(\w+)\s*\{'
)

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

def map_type(type_name):
    type_mapping = {
        "Float1": "Double",
        "Float2": "VecD",
        "Int1": "Integer",
        "Half3": "Vec3D",
        "Half4": "Color",
        "Int2": "VecI",
    }
    return type_mapping.get(type_name, type_name)

def extract_property_types(file_content):
    prop_types = {}
    for match in property_pattern.finditer(file_content):
        _, generic_type, prop_name = match.groups()
        prop_types[prop_name] = generic_type.strip()
    return prop_types

def extract_inputs_outputs_from_content(file_content, prop_types):
    inputs = []
    outputs = []

    # generic inputs
    for match in input_pattern_generic.finditer(file_content):
        kind, type_, name, label, default = match.groups()
        inputs.append({
            "name": screaming_to_words(label),
            "type": map_type(type_.strip()),
            "description": "TODO: Add a description.",
            "isContextful": kind == "Func",
            "default": default.strip() if default else None
        })

    # non-generic inputs
    for match in input_pattern_nongeneric.finditer(file_content):
        kind, name, label, default = match.groups()
        type_ = prop_types.get(name, "unknown")
        inputs.append({
            "name": screaming_to_words(label),
            "type": map_type(type_),
            "description": "TODO: Add a description.",
            "isContextful": kind == "Func",
            "default": default.strip() if default else None
        })

    # generic outputs
    for match in output_pattern_generic.finditer(file_content):
        kind, type_, name, label, default = match.groups()
        outputs.append({
            "name": screaming_to_words(label),
            "type": map_type(type_.strip()),
            "description": "TODO: Add a description.",
            "isContextful": kind == "Func",
            "default": default.strip() if default else None
        })

    # non-generic outputs
    for match in output_pattern_nongeneric.finditer(file_content):
        kind, name, label, default = match.groups()
        type_ = prop_types.get(name, "unknown")
        outputs.append({
            "name": screaming_to_words(label),
            "type": map_type(type_),
            "description": "TODO: Add a description.",
            "isContextful": kind == "Func",
            "default": default.strip() if default else None
        })

    return inputs, outputs

def find_base_class_name(file_content):
    match = re.search(r'class\s+\w+\s*:\s*([\w\d_]+)', file_content)
    if match:
        return match.group(1)
    return None

def find_node_file_by_classname(classname):
    for file in nodes_dir.rglob(f"{classname}Node.cs"):
        return file
    for file in nodes_dir.rglob(f"{classname}.cs"):
        return file
    return None

def extract_node_metadata_recursive(file_path, collected_inputs=None, collected_outputs=None, collected_isPair=False, collected_hasPreview=False):
    if collected_inputs is None:
        collected_inputs = []
    if collected_outputs is None:
        collected_outputs = []

    content = file_path.read_text(encoding="utf-8")
    prop_types = extract_property_types(content)

    inputs, outputs = extract_inputs_outputs_from_content(content, prop_types)
    collected_inputs.extend(inputs)
    collected_outputs.extend(outputs)

    if not collected_isPair:
        collected_isPair = bool(pair_pattern.search(content))
    if not collected_hasPreview:
        collected_hasPreview = "RenderNode" in content or "IPreviewRenderable" in content

    base_class = find_base_class_name(content)
    if not base_class or base_class == "Node":
        return {
            "inputs": collected_inputs,
            "outputs": collected_outputs,
            "isPair": collected_isPair,
            "hasPreview": collected_hasPreview
        }

    base_file = find_node_file_by_classname(base_class)
    if base_file is None:
        return {
            "inputs": collected_inputs,
            "outputs": collected_outputs,
            "isPair": collected_isPair,
            "hasPreview": collected_hasPreview
        }

    return extract_node_metadata_recursive(base_file, collected_inputs, collected_outputs, collected_isPair, collected_hasPreview)

def to_kebab_case(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def merge_metadata(viewmodel_meta, node_meta):
    return {
        "name": viewmodel_meta["name"].replace("Node", ""),
        "category": viewmodel_meta["category"],
        "icon": viewmodel_meta["icon"],
        "isPair": node_meta.get("isPair", False),
        "hasPreview": node_meta.get("hasPreview", False),
        "inputs": node_meta.get("inputs") or None,
        "outputs": node_meta.get("outputs") or None,
        "description": "TODO: Add a description."
    }

def write_mdx_file(metadata, name, existing_files):
    if f"{name}.mdx" in existing_files:
        print(f"Skipping {name}: File already exists somewhere in output_dir.")
        return

    title = metadata['name']
    frontmatter = {
        "title": title,
        "node": metadata
    }

    yaml_frontmatter = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True)
    content = f"---\n{yaml_frontmatter}---\n"

    output_dir.mkdir(parents=True, exist_ok=True)
    mdx_path = output_dir / f"{name}.mdx"

    with mdx_path.open("w", encoding="utf-8") as f:
        f.write(content)

def main():
    nodes = {f.name.replace("Node.cs", ""): f for f in nodes_dir.rglob("*Node.cs")}
    viewmodels = {f.name.replace("NodeViewModel.cs", ""): f for f in viewmodels_dir.rglob("*NodeViewModel.cs")}

    # 🔥 Precompute existing mdx files (recursive)
    existing_mdx_files = {f.name for f in output_dir.rglob("*.mdx")}

    for key in sorted(set(nodes.keys()) & set(viewmodels.keys())):
        viewmodel_path = viewmodels[key]
        node_path = nodes[key]

        vm_content = viewmodel_path.read_text(encoding="utf-8")

        viewmodel_meta = extract_viewmodel_metadata(vm_content)
        if not viewmodel_meta:
            print(f"Skipping {key}: No ViewModel metadata found.")
            continue

        node_meta = extract_node_metadata_recursive(node_path)
        merged = merge_metadata(viewmodel_meta, node_meta)

        write_mdx_file(merged, to_kebab_case(key), existing_mdx_files)

if __name__ == "__main__":
    main()