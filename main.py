import base64
import urllib.parse
import webbrowser
from pathlib import Path
from xml.etree import ElementTree as ET


def decode_textobject(data):
    """Декодирует Base64 → URL → HTML."""
    try:
        decoded_html = urllib.parse.unquote(base64.b64decode(data).decode("utf-8"))
        return decoded_html
    except Exception as e:
        print(f"Ошибка декодирования: {e}")
        return None


def render_html(html_content, output_file):
    """Сохраняет HTML в файл и открывает в браузере."""
    html_path = Path(output_file)
    html_path.write_text(html_content, encoding="utf-8")
    webbrowser.open(f"file://{html_path.absolute()}")


def process_xml(xml_file):
    """Парсит XML, находит textobject и декодирует их."""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Находим все textobject
        for i, textobject in enumerate(root.findall(".//textobject"), start=1):
            data = textobject.find("data").text
            if not data:
                continue

            decoded_html = decode_textobject(data)
            if decoded_html:
                print(f"\n--- Textobject {i} ---")
                print(decoded_html)
                render_html(decoded_html, f"textobject_{i}.html")

    except Exception as e:
        print(f"Ошибка обработки XML: {e}")


if __name__ == "__main__":
    xml_file = "C:/Users/s.u.mirzagitov/Downloads/2-1 DHCPv4.xml"  # Укажите путь к вашему XML
    process_xml(xml_file)