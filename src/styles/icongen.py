import xml.etree.ElementTree as ET

def parse_svg_font(svg_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}

    css_lines = []

    for glyph in root.findall('.//svg:glyph', ns):
        glyph_name = glyph.attrib.get('glyph-name')
        unicode_val = glyph.attrib.get('unicode')

        if glyph_name and unicode_val:
            # Convert to hex code (e.g. \e900)
            code = unicode_val.replace('&#x', '\\').replace(';', '')
            css_class = f""".icon-{glyph_name}::before {{ content: '{code}'; }}"""
            css_lines.append(css_class)

    return "\n".join(css_lines)


if __name__ == "__main__":
    svg_file = "../assets/pixiperfect-defs.svg" 
    css_output = parse_svg_font(svg_file)

    with open("iconfont.css", "w", encoding="utf-8") as f:
        f.write(css_output)

    print("CSS classes generated in iconfont.css")
