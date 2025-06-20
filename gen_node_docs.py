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
    r'Create(?:Func)?Input<([^>]+)>\(([^,]+),\s*"([^"]+)"(?:,\s*(.+?))?\)'
)

output_pattern_generic = re.compile(
    r'Create(?:Func)?Output<([^>]+)>\(([^,]+),\s*"([^"]+)"(?:,\s*(.+?))?\)'
)


# Without generics: CreateRenderInput(...), CreateRenderOutput(...)
input_pattern_nongeneric = re.compile(
    r'Create(?:Render)?Input\(([^,]+),\s*"([^"]+)"(?:,\s*(.+?))?\)'
)

output_pattern_nongeneric = re.compile(
    r'Create(?:Render)?Output\(([^,]+),\s*"([^"]+)"(?:,\s*(.+?))?\)'
)


property_pattern = re.compile(
    r'public\s+(InputProperty|FuncOutputProperty|OutputProperty|FuncInputProperty|InputProperty|FuncOutputProperty)<([^>]+)>\s+(\w+)\s*\{'
)

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

def extract_inputs_outputs_from_content(file_content, prop_types):
    inputs = []
    outputs = []

    # generic inputs
    for match in input_pattern_generic.finditer(file_content):
        type_, name, label, default = match.groups()
        inputs.append({
            "name": screaming_to_words(label),
            "type": type_.strip(),
            "description": "TODO: Add a description.",
            "default": default.strip() if default else None
        })

    # non-generic inputs
    for match in input_pattern_nongeneric.finditer(file_content):
        name, label, default = match.groups()
        type_ = prop_types.get(name, "unknown")  # look up type from properties
        inputs.append({
            "name": screaming_to_words(label),
            "type": type_,
            "description": "TODO: Add a description.",
            "default": default.strip() if default else None
        })

    # generic outputs
    for match in output_pattern_generic.finditer(file_content):
        type_, name, label, default = match.groups()
        outputs.append({
            "name": screaming_to_words(label),
            "type": type_.strip(),
            "description": "TODO: Add a description.",
            "default": default.strip() if default else None
        })

    # non-generic outputs
    for match in output_pattern_nongeneric.finditer(file_content):
        name, label, default = match.groups()
        type_ = prop_types.get(name, "unknown")  # look up type from properties
        outputs.append({
            "name": screaming_to_words(label),
            "type": type_,
            "description": "TODO: Add a description.",
            "default": default.strip() if default else None
        })

    return inputs, outputs


def find_base_class_name(file_content):
    # Extract base class from class declaration, first base class only
    match = re.search(r'class\s+\w+\s*:\s*([\w\d_]+)', file_content)
    if match:
        return match.group(1)
    return None

def find_node_file_by_classname(classname):
    # Look for a file matching <classname>.cs (or <classname>Node.cs)
    # We'll assume files end with Node.cs, so try classname + "Node.cs"
    candidate = nodes_dir / f"{classname}Node.cs"
    if candidate.exists():
        return candidate
    
    # Traverse directories to find the file
    for file in nodes_dir.rglob(f"{classname}Node.cs"):
        if file.exists():
            return file

    # Fallback: classname + ".cs"
    candidate = nodes_dir / f"{classname}.cs"
    if candidate.exists():
        return candidate
    
    # Traverse directories to find the file
    for file in nodes_dir.rglob(f"{classname}.cs"):
        if file.exists():
            return file

    return None

def extract_node_metadata_recursive(file_path, collected_inputs=None, collected_outputs=None, collected_isPair=False, collected_hasPreview=False):
    if collected_inputs is None:
        collected_inputs = []
    if collected_outputs is None:
        collected_outputs = []

    with file_path.open("r", encoding="utf-8") as f:
        content = f.read()

    prop_types = extract_property_types(content)  # extract property types from this class

    # Gather inputs and outputs for this class
    inputs, outputs = extract_inputs_outputs_from_content(content, prop_types)
    collected_inputs.extend(inputs)
    collected_outputs.extend(outputs)

    # Gather isPair and hasPreview flags if any found here (or keep old True)
    if not collected_isPair:
        collected_isPair = bool(pair_pattern.search(content))
    if not collected_hasPreview:
        collected_hasPreview = "RenderNode" in content or "IPreviewRenderable" in content

    # Find base class, stop if base class is "Node"
    base_class = find_base_class_name(content)
    if not base_class or base_class == "Node":
        return {
            "inputs": collected_inputs,
            "outputs": collected_outputs,
            "isPair": collected_isPair,
            "hasPreview": collected_hasPreview
        }

    # Find base class file and recurse if found
    base_file = find_node_file_by_classname(base_class)
    if base_file is None:
        # Base class file not found, stop here
        return {
            "inputs": collected_inputs,
            "outputs": collected_outputs,
            "isPair": collected_isPair,
            "hasPreview": collected_hasPreview
        }

    # Recurse up the hierarchy
    return extract_node_metadata_recursive(base_file, collected_inputs, collected_outputs, collected_isPair, collected_hasPreview)

def extract_property_types(file_content):
    prop_types = {}
    for match in property_pattern.finditer(file_content):
        prop_kind, generic_type, prop_name = match.groups()
        prop_types[prop_name] = generic_type.strip()
    return prop_types


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

        node_meta = extract_node_metadata_recursive(node_path)
        merged = merge_metadata(viewmodel_meta, node_meta)

        write_mdx_file(merged, to_kebab_case(key))

if __name__ == "__main__":
    main()
