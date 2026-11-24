import sys
import xml.etree.ElementTree as ET

from parser import parse_text
from errors import ConfigLanguageError


def value_to_xml(parent, value):
    if isinstance(value, list):
        array_element = ET.SubElement(parent, "array")
        for item in value:
            value_to_xml(array_element, item)
    elif isinstance(value, int):
        ET.SubElement(parent, "number").text = str(value)
    elif isinstance(value, dict):
        element = ET.SubElement(parent, "constant")
        element.set("name", value["name"])
        value_to_xml(element, value["value"])
    else:
        ET.SubElement(parent, "value").text = str(value)


def convert_to_xml(data):
    root = ET.Element("config")

    for item in data:
        value_to_xml(root, item)

    ET.indent(root, space="    ")

    return ET.tostring(root, encoding="unicode")

def main():
    source = sys.stdin.read()

    try:
        result = parse_text(source)
        xml = convert_to_xml(result)
        print(xml)
    except ConfigLanguageError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()