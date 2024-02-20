import os
import pathlib
import logging
import glob
from typing import List, Dict
import pwd
import stat
from flask import Blueprint, render_template

bp = Blueprint("pages", __name__)
LOG = logging.getLogger(__name__)

# constantes
CURRENT_PATH = pathlib.Path().resolve()
PATH = str(CURRENT_PATH) + '/incomplete/static/images'
# LIST_DIR = os.listdir(PATH)


@bp.route("/")
def home():

    # LOG.debug(directory_contents(PATH))

    data = directory_contents(PATH)

    return render_template("pages/home.html", data=data['data'])

# ajouter la date de modification, l'extension


def get_files_contents(path: str) -> List:
    """Returns sub directory contents

    Lists directory contents in a list

    Args:
        path (str): sub directory path
    """

    images = []
    files = glob.glob(path + '/*.jpg')

    for file in files:

        file_attr = {'name': os.path.basename(file), 'size': '{} kb'.format(round(os.path.getsize(file) / 1028))}
        # size in kilobytes
        if os.path.isfile(file):
            file_attr['type'] = 'file'
        else:
            file_attr['type'] = 'dir'
        images.append(file_attr)

    return images


def directory_contents(path: str) -> Dict:
    """Returns root directory contents

    Lists directory contents in a dict

    Args:
        path (str): directory path
    """
    root_files = {'data': []}
    directories = os.listdir(path)
    # print(files)
    for directory in directories:

        file_attr = {}
        file_path = '{}/{}'.format(path, directory)
        file_attr['name'] = os.path.basename(file_path)
        # size in kilobytes
        file_attr['size'] = '{} kb'.format(round(os.path.getsize(file_path) / 1028))
        file_attr['files'] = get_files_contents(file_path)
        if os.path.isfile(file_path):
            file_attr['type'] = 'file'
        else:
            file_attr['type'] = 'dir'
        root_files['data'].append(file_attr)
    # bd.logger.debug(json_body)
    return root_files


def get_owner(path):
    """Get owner of file or directory

    Args:
        path (str): file path
    """
    information = os.stat(path)
    return pwd.getpwuid(information.st_uid)[0]


def get_permissions(path):
    """Get permission of file or directory in octal

    Args:
        path (str): file path
    """
    return oct(stat.S_IMODE(os.stat(path).st_mode))[-3:]
