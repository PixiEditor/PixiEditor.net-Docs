#!/usr/bin/dotnet run
#:package YamlDotNet@18.1.0

using System.Reflection;
using System.Text;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

const string changeableDll = "../PixiEditor/src/PixiEditor.Desktop/bin/Debug/net8.0/PixiEditor.ChangeableDocument.dll";
const string editorDll = "../PixiEditor/src/PixiEditor.Desktop/bin/Debug/net8.0/PixiEditor.dll";
const string uiCommonDll = "../PixiEditor/src/PixiEditor.Desktop/bin/Debug/net8.0/PixiEditor.UI.Common.dll";

const string outputDir = "src/content/docs/usage/Node Graph/Nodes/";

var changeableAssembly = Assembly.LoadFrom(changeableDll);
var editorAssembly = Assembly.LoadFrom(editorDll);
var uiCommonAssembly = Assembly.LoadFrom(uiCommonDll);

var nodeType = changeableAssembly.GetType(
    "PixiEditor.ChangeableDocument.Changeables.Graph.Nodes.Node");

if (nodeType == null)
    throw new Exception("Node type not found");


var existingDocs = new HashSet<string>(
    StringComparer.OrdinalIgnoreCase);

if (Directory.Exists(outputDir))
{
    foreach (var file in Directory.GetFiles(
        outputDir,
        "*.mdx",
        SearchOption.AllDirectories))
    {
        // Check filename
        existingDocs.Add(
            Path.GetFileName(file));


        // Check PIXIEDITOR marker
        var lines = File.ReadLines(file)
            .Take(3)
            .ToArray();

        foreach (var line in lines)
        {
            if (line.StartsWith("#PIXIEDITOR:",
                    StringComparison.OrdinalIgnoreCase))
            {
                var nodeName = line["#PIXIEDITOR:".Length..]
                    .Trim();

                if (!string.IsNullOrWhiteSpace(nodeName))
                {
                    existingDocs.Add(
                        "#PIXIEDITOR:" + nodeName);
                }
            }
        }
    }
}


var nodeClasses = changeableAssembly
    .GetTypes()
    .Where(t =>
        !t.IsAbstract &&
        nodeType.IsAssignableFrom(t));


Directory.CreateDirectory(outputDir);


var serializer = new SerializerBuilder()
    .ConfigureDefaultValuesHandling(
        DefaultValuesHandling.OmitNull)
    .Build();



foreach (var node in nodeClasses.OrderBy(x => x.Name))
{
    var viewModel = FindViewModel(
        node,
        editorAssembly);

    if (viewModel == null)
        continue;


var viewModelMetadata =
    ExtractViewModelMetadata(
        viewModel,
        uiCommonAssembly);

    if (viewModelMetadata == null)
    {
        Console.WriteLine(
            $"Skipping {node.Name}: missing metadata");

        continue;
    }


    var nodeMetadata =
        ExtractNodeMetadata(node);


    var docName =
        ToKebabCase(
            node.Name.Replace("Node", ""));

if (existingDocs.Contains(docName + ".mdx"))
{
    Console.WriteLine(
        $"Skipping {node.Name}: {docName}.mdx already exists.");

    continue;
}

if (existingDocs.Contains("#PIXIEDITOR:" + node.Name.Replace("Node", "")))
{
    Console.WriteLine(
        $"Skipping {node.Name}: PIXIEDITOR marker exists.");

    continue;
}


    var metadata = new Dictionary<string, object>
    {
        ["title"] = viewModelMetadata["name"],

        ["node"] = new Dictionary<string, object>
        {
            ["name"] = viewModelMetadata["name"],
            ["category"] = viewModelMetadata["category"],
            ["icon"] = viewModelMetadata["icon"],

            ["isPair"] = nodeMetadata.IsPair,
            ["hasPreview"] = nodeMetadata.HasPreview,

            ["inputs"] =
                nodeMetadata.Inputs.Count > 0
                    ? nodeMetadata.Inputs
                    : null,

            ["outputs"] =
                nodeMetadata.Outputs.Count > 0
                    ? nodeMetadata.Outputs
                    : null,

            ["description"] =
                "TODO: Add a description."
        }
    };


    var yaml = serializer.Serialize(metadata);

var category =
    viewModelMetadata["category"]
        .ToString()!;


var categoryFolder =
    Path.Combine(
        outputDir,
        category);


Directory.CreateDirectory(categoryFolder);


var path = Path.Combine(
    categoryFolder,
    docName + ".mdx");


    File.WriteAllText(
        path,
        $"---\n{yaml}---\n",
        Encoding.UTF8);


    Console.WriteLine(
        $"Generated {path}");
}



static Type? FindViewModel(
    Type node,
    Assembly assembly)
{
    return assembly
        .GetTypes()
        .FirstOrDefault(t =>
            t.Name == node.Name + "ViewModel");
}



static Dictionary<string, object>? ExtractViewModelMetadata(
    Type vm,
    Assembly editorAssembly)
{
    var attribute = vm
        .GetCustomAttributes()
        .FirstOrDefault(a =>
            a.GetType().Name ==
            "NodeViewModelAttribute");


    if (attribute == null)
        return null;


    var values = attribute
        .GetType()
        .GetProperties()
        .Select(p => p.GetValue(attribute))
        .ToArray();


    var name =
        values.ElementAtOrDefault(0)
            ?.ToString()
        ?? string.Empty;


    var category =
        values.ElementAtOrDefault(1)
            ?.ToString()
        ?? string.Empty;


    var iconValue =
        values.ElementAtOrDefault(2);


var icon =
    GetIconName(
        values.ElementAtOrDefault(2),
        editorAssembly);


    return new()
    {
        ["name"] =
            ScreamingToWords(
                name.Replace("_NODE", "")),

        ["category"] =
            ScreamingToWords(category),

        ["icon"] =
            icon
    };
}



static NodeMetadata ExtractNodeMetadata(
    Type node)
{
    var inputs = new List<object>();
    var outputs = new List<object>();


    foreach (var property in node.GetProperties(
        BindingFlags.Public |
        BindingFlags.Instance |
        BindingFlags.FlattenHierarchy))
    {
        var type = property.PropertyType;


        if (!type.IsGenericType)
            continue;


        var genericName =
            type.GetGenericTypeDefinition()
                .Name;


        var argument =
            type.GetGenericArguments()
                .First()
                .Name;


        if (genericName.Contains("InputProperty"))
        {
            inputs.Add(new
            {
                name = ScreamingToWords(property.Name),
                type = MapType(argument),
                description =
                    "TODO: Add a description."
            });
        }


        if (genericName.Contains("OutputProperty"))
        {
            outputs.Add(new
            {
                name = ScreamingToWords(property.Name),
                type = MapType(argument),
                description =
                    "TODO: Add a description."
            });
        }
    }


    var isPair =
        node.GetCustomAttributes()
            .Any(a =>
                a.GetType().Name ==
                "PairNodeAttribute");


    var hasPreview =
        node.GetInterfaces()
            .Any(i =>
                i.Name.Contains("Preview") ||
                i.Name.Contains("Renderable"));


    return new()
    {
        Inputs = inputs,
        Outputs = outputs,
        IsPair = isPair,
        HasPreview = hasPreview
    };
}

static string GetIconName(
    object? iconValue,
    Assembly assembly)
{
    if (iconValue == null)
        return string.Empty;


    var iconType = assembly
        .GetTypes()
        .FirstOrDefault(t =>
            t.Name == "PixiPerfectIcons");


    if (iconType == null)
        return string.Empty;


    var iconValueString = iconValue.ToString();


    var field = iconType
        .GetFields(
            BindingFlags.Public |
            BindingFlags.Static)
        .FirstOrDefault(f =>
            f.IsLiteral &&
            f.GetRawConstantValue()?.ToString()
                == iconValueString);


    if (field == null)
        return string.Empty;


    return "icon-" + ToKebabCase(field.Name);
}

static string MapType(
    string type)
{
    return type switch
    {
        "Float1" => "Double",
        "Float2" => "VecD",
        "Int1" => "Integer",
        "Half3" => "Vec3D",
        "Half4" => "Color",
        "Int2" => "VecI",
        _ => type
    };
}



static string ScreamingToWords(string? value)
{
    if (string.IsNullOrWhiteSpace(value))
        return string.Empty;

    value = System.Text.RegularExpressions.Regex.Replace(
        value,
        "([a-z0-9])([A-Z])",
        "$1 $2");

    value = System.Text.RegularExpressions.Regex.Replace(
        value,
        "([A-Z]+)([A-Z][a-z])",
        "$1 $2");

    value = value.Replace('_', ' ');

    return string.Join(
        " ",
        value
            .Split(
                ' ',
                StringSplitOptions.RemoveEmptyEntries)
            .Select(word =>
                char.ToUpperInvariant(word[0]) +
                word.Substring(1).ToLowerInvariant()));
}

static string ToKebabCase(string value)
{
    value = System.Text.RegularExpressions.Regex.Replace(
        value,
        "([a-z0-9])([A-Z])",
        "$1-$2");


    value = System.Text.RegularExpressions.Regex.Replace(
        value,
        "([A-Z]+)([A-Z][a-z])",
        "$1-$2");


    return value
        .Replace('_', '-')
        .ToLowerInvariant();
}

class NodeMetadata
{
    public List<object> Inputs { get; set; } = [];
    public List<object> Outputs { get; set; } = [];

    public bool IsPair { get; set; }
    public bool HasPreview { get; set; }
}
