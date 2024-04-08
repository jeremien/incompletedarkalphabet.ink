import pathlib
import os
import glob
import markdown

from datetime import datetime
from flask import render_template, abort
from os.path import exists
from typing import List, Dict

from incomplete import app

"""
Constants
"""
CURRENT_PATH = pathlib.Path().resolve()
IMAGE_PATH = str(CURRENT_PATH) + "/incomplete/static/images"
TXT_PATH = str(CURRENT_PATH) + "/incomplete/static/txt/"


@app.template_filter()
def unix_to_date(unix_time):
    """
    Flask filter to render the correct date time format
    """

    date = datetime.fromtimestamp(unix_time)
    return date.strftime("%d/%m/%Y")


@app.route("/")
def home():
    """
    Serve images content for the index
    """

    data = directory_contents(IMAGE_PATH)

    total_bytes = get_dir_size(IMAGE_PATH)
    total_mb = round((total_bytes / 1024) / 1024)
    total_files = get_num_files(IMAGE_PATH)
    # TODO récupérer les vrais données
    total_data = {
        "mb": total_mb,
        "files": total_files,
        "type": ".webp",
        "size": "850x1390",
    }
    data["page_title"] = "Index"
    return render_template("pages/home.html", data=data["data"], total=total_data)


@app.route("/<page>")
def get_page(page):
    """
    Serve a new page based on markdown file
    """

    if exists(TXT_PATH + page + ".md"):
        data = {"page_title": page.title()}
        with open(TXT_PATH + page + ".md", "r") as f:
            text = f.read()
            data["html"] = markdown.markdown(text)
        # LOG.debug(data)
        return render_template("pages/page.html", data=data)
    else:
        abort(404)


@app.route("/book")
def book():
    """
    Serve the book template
    """

    data = directory_contents(IMAGE_PATH)

    return render_template(
        "pages/book.html",
        data=data["data"],
    )


@app.errorhandler(404)
def page_not_found(e):
    """
    Return a 404 page when the path is wrong
    """

    return render_template("404.html"), 404


"""
functions
"""


def get_num_files(path: str) -> int:
    """
    Return the number of files in the folder
    """

    count = 0
    for root_dir, cur_dir, files in os.walk(path):
        count += len(files)
    return count


def get_dir_size(path: str) -> int:
    """
    Returns directory size in bytes
    Args:
        path (str): path
    """

    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def get_files_contents(path: str) -> List:
    """
    Returns sub directory contents

    Lists directory contents in a list

    Args:
        path (str): sub directory path
    """

    images = []
    files = glob.glob(path + "/*.webp")

    for file in files:

        file_attr = {
            "name": os.path.basename(file),
            "date": os.path.getmtime(file),
            "size": "{}".format(round(os.path.getsize(file) / 1024)),
            "type": os.path.splitext(file),
        }

        # size in kilobytes
        if os.path.isfile(file):
            file_attr["type"] = "file"
        else:
            file_attr["type"] = "dir"
        images.append(file_attr)

    return images


def directory_contents(path: str) -> Dict:
    """
    Returns root directory contents

    Lists directory contents in a dict

    Args:
        path (str): directory path
    """

    root_files = {"data": []}
    directories = os.listdir(path)

    for directory in directories:
        file_attr = {}
        file_path = "{}/{}".format(path, directory)
        file_attr["name"] = os.path.basename(file_path)

        # size in kilobytes
        file_attr["size"] = "{} kb".format(round(os.path.getsize(file_path) / 1028))
        file_attr["files"] = get_files_contents(file_path)
        if os.path.isfile(file_path):
            file_attr["type"] = "file"
        else:
            file_attr["type"] = "dir"
        root_files["data"].append(file_attr)
    return root_files

