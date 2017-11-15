import getopt
import os
import socket

import requests
import sys
from bs4 import BeautifulSoup


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hs", ["help", "search"])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("If you want search producent and product call: -s(optional --search) producent_id product_id")
            print("For example: -s 0bc2 0502")
            sys.exit()
        elif opt in ("-s", "--search"):
            if is_connected():
                get_page(sys.argv[2], sys.argv[3])
            else:
                parse_from_file(sys.argv[2], sys.argv[3])


def is_connected():
    try:
        socket.create_connection(("http://www.linux-usb.org/usb.ids", 80))
        return True
    except OSError:
        pass
    return False


def get_filename():
    filename = ""
    for file in os.listdir():
        if file.endswith(".txt"):
            filename = file.replace(".txt", "")
    return filename


def write_to_file(filename, content):
    f = open(filename + ".txt", "a")
    f.write(content + "\n")
    f.close()


def load_from_file():
    f = open(get_filename() + ".txt", "r")
    content = f.read()
    f.close()
    return content


def get_page(producent_id, product_id):
    r = requests.get("http://www.linux-usb.org/usb.ids")
    soup = BeautifulSoup(r.content, "html.parser")
    parse_page(soup, producent_id, product_id)


def parse_page(page, producent_id, product_id):
    filename = ""
    old_filename = ""
    found_producent = False
    for line in page.get_text().splitlines():
        if "Version: " in line:
            filename = line[11:]
            old_filename = get_filename()
        if filename != old_filename:
            if os.path.exists(old_filename + ".txt"):
                os.remove(old_filename + ".txt")
            line_to_file = str(line.encode('utf-8'))
            write_to_file(filename, line_to_file)
        if producent_id in line and "\t" not in line:
            line = line[len(producent_id):]
            print("Producent:" + line)
            found_producent = True
            continue
        if found_producent and "\t" in line:
            if product_id in line:
                line = line[len(product_id) + 1:]
                print("Product:" + line)
        else:
            found_producent = False


def parse_from_file(producent_id, product_id):
    content = load_from_file()
    found_producent = False
    for line in content.splitlines():
        if producent_id in line and "\\t" not in line:
            line = line[len(producent_id) + 3:]
            print("Producent:" + line)
            found_producent = True
            continue
        if found_producent and "\\t" in line:
            if product_id in line:
                line = line[len(product_id) + 5:]
                print("Product:" + line)
        else:
            found_producent = False


if __name__ == "__main__":
    main(sys.argv[1:])
