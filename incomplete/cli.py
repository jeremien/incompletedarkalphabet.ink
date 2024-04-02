import click
import os
import pathlib

from typing import List
from jaraco import path
from PIL import Image

from incomplete import app

"""
Constants
"""
CURRENT_PATH = pathlib.Path().resolve()
SOURCE_PATH = str(CURRENT_PATH) + "/src"
IMAGE_PATH = str(CURRENT_PATH) + "/incomplete/static/images"
BASE_WIDTH = 850
BASE_HEIGHT = 1386


@app.cli.command("process")
def process():
    files = os.listdir(SOURCE_PATH)
    process_file(files)


def process_file(list_files: List[str]) -> None:
    """
    list all files and dir in source directory
    and prepare to save

    ARGS:
        Array of files in directory

    """
    for f in enumerate(list_files):

        src_file = SOURCE_PATH + "/" + f[1]
        output_dir = IMAGE_PATH + "/" + f[1]

        if os.path.isfile(src_file):
            continue
        else:
            sub_files = os.listdir(src_file)

            if os.path.exists(output_dir):
                print(output_dir)
            else:
                os.mkdir(output_dir)

            for i in enumerate(sub_files):
                if test_ext(src_file + "/" + i[1]):
                    _, file_ext = os.path.splitext(f[1])
                    convert_file(
                        src_file + "/" + i[1], output_dir + "/" + str(i[0]) + ".webp"
                    )

    click.echo("*** end ***")


def convert_file(src_file: str, dist_file: str) -> None:
    """
    Convert image for web to print
    same width and greyscale
    same filetype (webp)

    ARGS:
        source file path
        dist file path
    TODO normalisation des images ?
    """

    click.echo("*** convert and save ***")

    img = Image.open(src_file)

    img_base = Image.new(mode="L", size=(BASE_WIDTH, BASE_HEIGHT), color="white")
    img.thumbnail((BASE_WIDTH, BASE_HEIGHT))

    marge_width = int((BASE_WIDTH - img.size[0]) / 2)
    marge_height = int((BASE_HEIGHT - img.size[1]) / 2)

    back_img = img_base.copy()
    back_img.paste(img, (marge_width, marge_height))

    back_img.save(dist_file, "webp", optimize=True, quality=90)


def is_hidden(filepath: str) -> bool:
    """
        Test if file is an hidden file with a dot

        ARG:
            filepath : file path

    TODO réecrire fonction sans la package jaraco
    """

    name = os.path.basename(os.path.abspath(filepath))
    return path.is_hidden(name)


def test_ext(filepath: str) -> bool:
    """
        Test if extension is only image

        ARG:
            filepath : file path
    TODO simplifier
    """

    filepath, file_ext = os.path.splitext(filepath)
    if is_hidden(filepath):
        return False
    else:
        if (
            file_ext == ".jpg"
            or file_ext == ".png"
            or file_ext == ".webp"
            or file_ext == ".gif"
            or file_ext == ".JPG"
            or file_ext == ".JPEG"
            or file_ext == ".jpeg"
        ):
            return True
