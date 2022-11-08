####################################################################################################
#
# Copyright (C) 2022 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

from pathlib import Path
import os

from invoke import task

####################################################################################################

SOURCE_PATH = Path(__file__).absolute().parents[1]
# QML_PATH = PATH.joinpath('qml')
# RCC_PATH = PATH.joinpath('rcc')

####################################################################################################

# @task
# def clean(ctx):   # noqa:
#     for _ in (
#             'application.rcc',
#             'resources.py',
#     ):
#         RCC_PATH.joinpath(_).unlink()

####################################################################################################

# @task
# def rcc(ctx):   # noqa:
#     with ctx.cd(RCC_PATH):
#         ctx.run('pyside6-rcc application.qrc -o resources.py')

####################################################################################################

@task()
def qml(ctx, qml_path):
    # qml = Path(ctx.Qt.bin_path).joinpath('qml')
    qml = 'pyside6-qml'
    qml_path = Path(qml_path).absolute()
    # includes = ' '.join([f'-I {_}' for _ in (QML_PATH,)])
    includes = ''
    command = f'{qml} {includes} {qml_path}'
    env = {
        'QT_LOGGING_RULES': ';'.join((
            '*.debug=true',
            'qt.*.debug=false',
            '*.info=true',
        )),
    }
    # with ctx.cd('.'):
    ctx.run(command, env=env)

####################################################################################################

@task()
def get_qt_source(ctx):
    # path = Path(path)
    path = Path(ctx.Qt.source_path)
    if not path.exists():
        # https://wiki.qt.io/Building_Qt_6_from_Git
        ctx.run(f'git clone git://code.qt.io/qt/qt5.git {path}')
    with ctx.cd(path):
        # branch = 'dev'
        branch = 'v6.4.0'
        ctx.run(f'git switch {branch}')
        ctx.run(f'perl init-repository --module-subset')

####################################################################################################

@task()
def find_qml_source(ctx, pattern):
    pattern = pattern.lower()
    qt_path = Path(ctx.Qt.source_path).resolve()
    controls_path = qt_path.joinpath('qtquickcontrols2', 'src')
    print(controls_path)
    for root, _, filenames in os.walk(controls_path):
        root = Path(root)
        for filename in filenames:
            filename = Path(filename)
            if filename.suffix == '.qml':
                if pattern in filename.name.lower():
                    file_path = root.joinpath(filename)
                    print(file_path)

####################################################################################################

@task()
def find_qml(ctx, follow=False):
    directories = set()
    for root, _, filenames in os.walk(SOURCE_PATH, followlinks=follow):
        root = Path(root)
        for filename in filenames:
            filename = Path(filename)
            if filename.suffix == '.qml':
                directories.add(root.relative_to(SOURCE_PATH))

    pyqt = [_ for _ in directories if 'PyQt' in str(_)]
    pyside = [_ for _ in directories if 'PySide' in str(_)]
    BASE_URL = 'https://github.com/FabriceSalvaire/qt-python-examples/tree/main/'
    for wrapper in (pyside, pyqt):
        for _ in sorted(wrapper):
            title = str(_).replace('/', ' / ')
            print(f'* [{title}]({BASE_URL}{_})')

####################################################################################################

# @task()
# def cmake(ctx):
# /opt/Qt/Tools/CMake/bin/cmake -D CMAKE_PREFIX_PATH:PATH=/opt/Qt/6.4.0/gcc_64/ ../multipage
