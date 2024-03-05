import os
import pathlib
import logging
import glob
import time
from datetime import datetime
from typing import List, Dict
import pwd
import stat
import pathlib
from flask import Blueprint, render_template

bp = Blueprint("pages", __name__, template_folder='templates')
LOG = logging.getLogger(__name__)

@bp.app_template_filter()
def unix_to_date(unix_time):
    date = datetime.fromtimestamp(unix_time)
    return date.strftime("%d/%m/%Y")

# constantes
CURRENT_PATH = pathlib.Path().resolve()
PATH = str(CURRENT_PATH) + '/incomplete/static/images'
# LIST_DIR = os.listdir(PATH)


@bp.route("/")
def home():

    data = directory_contents(PATH)

    total_bytes = get_dir_size(PATH)
    total_mb = round((total_bytes / 1024) / 1024)
    total_files = get_num_files(PATH)

    total_data = { 'mb': total_mb, 'files': total_files, 'type': '.webp', 'size': '850x1390' }
    #LOG.debug(total_files)

    return render_template("pages/home.html",
                           data=data['data'],
                           total=total_data
                           )

# ajouter la date de modification, l'extension


def get_num_files(path: str) -> int:
    count = 0
    for root_dir, cur_dir, files in os.walk(path):
        count += len(files)
    return count


def get_dir_size(path: str) -> int:
    """Returns directory size in bytes
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
    """Returns sub directory contents

    Lists directory contents in a list

    Args:
        path (str): sub directory path
    """

    images = []
    files = glob.glob(path + '/*.webp')

    for file in files:

        file_attr = {
            'name': os.path.basename(file),
            'date': os.path.getmtime(file),
            'size': '{}'.format(round(os.path.getsize(file) / 1024)),
            'type': os.path.splitext(file),
        }
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
