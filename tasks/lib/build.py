####################################################################################################
#
# Copyright (C) 2022 Fabrice Salvaire
# SPDX-License-Identifier: GPL-3.0-only
#
####################################################################################################

####################################################################################################

__all__= [
    'git_clone',
    'download',
    'untar',
    'unzip',
    # 'set_executable',
]

####################################################################################################

from pathlib import Path
import os

import requests

####################################################################################################

def git_clone(ctx, url, path, branch=None, depth=1):
    print(f"Clone repository {url}")
    with ctx.cd(path.parent):
        command = f"git clone"
        if depth:
            command += f" --depth={depth}"
        if branch:
            command += f" --branch {branch}"
        command += f" {url} {path}"
        ctx.run(command, echo=True)

####################################################################################################

def git_fetch_tags(ctx):
    ctx.run('git fetch --all --tag')

def git_checkout_tags(ctx, tag):
    ctx.run('git checkout tags/{tag}')

####################################################################################################

def set_executable(path):
    path = Path(path)
    st = path.stat()
    path.chmod(st.st_mode | os.stat.S_IEXEC)

####################################################################################################

def download(url, path, executable=False):
    print(f"Get {url} ...")
    req = requests.get(url)
    with open(path, 'wb') as fh:
        fh.write(req.content)
    if executable:
        set_executable(path)

####################################################################################################

def untar(tar_path, path):
    import tarfile
    tar = tarfile.open(tar_path)
    tar.extractall(path=path)
    tar.close()

####################################################################################################

def unzip(zip_path, path):
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(path)
