import base64
import urllib.parse
import webbrowser
from pathlib import Path
from xml.etree import ElementTree as ET


def decode_textobject(data):
    """Декодирует Base64 → URL → HTML"""
    try:
        return urllib.parse.unquote(base64.b64decode(data).decode("utf-8"))
    except Exception as e:
        print(f"Ошибка декодирования: {e}")
        return None


def process_xml(xml_file, output_html="combined.html"):
    """Обрабатывает XML и объединяет все textobject в один HTML."""
    combined_html = "<!DOCTYPE html><html><head><meta charset='UTF-8'></head><body>"

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for textobject in root.findall(".//textobject"):
            data = textobject.find("data").text
            if not data:
                continue

            decoded = decode_textobject(data)
            if decoded:
                combined_html += decoded  # Просто добавляем HTML друг за другом

        combined_html += "</body></html>"

        # Сохраняем и открываем
        Path(output_html).write_text(combined_html, encoding="utf-8")
        webbrowser.open(f"file://{Path(output_html).absolute()}")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    process_xml("2-1 DHCPv4.unl")  # Укажите ваш XML-файл