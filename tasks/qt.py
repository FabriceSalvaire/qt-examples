####################################################################################################
#
# Copyright (C) 2022 Fabrice Salvaire
# SPDX-License-Identifier: GPL-3.0-only
#
####################################################################################################

####################################################################################################

from pathlib import Path
import glob
import os
import pathlib
# import tempfile
import shutil
import sys

# import invoke
from invoke import task, call

import yaml

# https://github.com/tartley/colorama
from colorama import init   # , Fore
from termcolor import colored
# use Colorama to make Termcolor work on Windows too
init(autoreset=True)

from .lib.build import download

####################################################################################################

ROOT_PATH = Path(__file__).absolute().parents[1]

####################################################################################################

def print_colored(message: str, color: str) -> None:
    print(colored(message, color))

def print_error(message: str) -> None:
    print_colored(message, 'red')

def print_section(message: str) -> None:
    print_colored(message, 'blue')

def print_info(message: str) -> None:
    print_colored(message, 'green')

def print_section_rule() -> None:
    print_colored('─'*100, 'blue')

####################################################################################################

def _init_config(ctx, source=None) -> None:
    if hasattr(ctx.build, 'root'):
        return

    ctx.build['root'] = ROOT_PATH

    if not hasattr(ctx.build, 'qt'):
        config_files = glob.glob(str(ctx.build.root / 'build-config' / '*.yaml'))
        print_error("Usage: inv -f build-XXX.yaml build.XXX")
        print("Available config files:")
        for _ in config_files:
            _ = Path(_).relative_to(ctx.build.root)
            print(' '*4, _)
        sys.exit(1)
        # raise NameError("Config file is missing")

    #! ctx.build['resources_path'] = ctx.build.root / 'resources'

    if hasattr(ctx.build, 'path'):
        ctx.build.path = Path(ctx.build.path)
    else:
        ctx.build['path'] = ctx.build.root / f'build-{ctx.build.arch}'

    # ctx.build['openssl_source'] = ctx.build.third_parties / 'openssl' / 'openssl-source'

    ARCH = (
        'gcc_64',
        'android_x86',
        'android_x86_64',
        'android_armv7',
        'android_arm64_v8a',
    )
    if ctx.build.arch not in ARCH:
        raise NameError(f"arch must be {ARCH}")

    _set_qt(ctx)

    for _ in ('CFLAGS', 'CXXFLAGS'):
        os.environ.pop(_, None)

    # for multi-sources
    if source is not None:
        source = Path(source)
        if not source.is_dir():
            raise ValueError(f'{source} is not a directory')
        ctx.build['source'] = ROOT_PATH / source
        ctx.build.path = ctx.build.path / source.name

####################################################################################################

# def _set_qt(ctx, qt_path=None, arch='gcc_64'):
#     if qt_path is None:
#         qt_path = os.getenv('QT_PATH')
#     if qt_path is None:
#         raise NameError('The "QT_PATH" environment variable must be set to Qt path')
#     ctx.qt_path = Path(qt_path)

def _set_qt(ctx) -> None:
    ctx.build.qt = Path(ctx.build.qt)
    if not ctx.build.qt.exists():
        raise NameError("Qt not found {ctx.build.qt}")
    match sys.platform:
        case 'linux':
            host_arch = 'gcc_64'
            ctx.build['qt_host_path'] = ctx.build.qt / host_arch
            ctx.build['qt_bin_path'] = ctx.build.qt_host_path / 'bin'
            ctx.build['qt_lib_path'] = ctx.build.qt_host_path / 'lib'
            ctx.build['qt_arch_path'] = ctx.build.qt / ctx.build.arch
            ctx.build['qmake_path'] = ctx.build.qt_arch_path / 'bin' / 'qmake'
        case 'darwin':
            raise NotImplementedError
        case 'win32':
            raise NotImplementedError

####################################################################################################

@task()
def show_config(ctx):
    _init_config(ctx)

    config = dict(ctx.config.items())

    def path_representer(dumper, data):
        return dumper.represent_scalar('!PATH', str(data))

    yaml.add_representer(pathlib.PosixPath, path_representer)

    print(yaml.dump(config))

####################################################################################################

@task
def install_qt(ctx):
    print('Download Qt installer https://www.qt.io/download-qt-installer')
    # https://download.qt.io/official_releases/online_installers/qt-unified-linux-x64-online.run.mirrorlist
    qt_installer_url = 'https://download.qt.io/official_releases/online_installers/qt-unified-linux-x64-online.run'
    qt_installer_path = Path('qt_installer')
    download(qt_installer_url, qt_installer_path, executable=True)

####################################################################################################

@task
def install_android_sdk(ctx):
    # https://doc.qt.io/qt-6/android-getting-started.html
    # https://developer.android.com/studio
    # https://dl.google.com/android/repository
    commandlinetools_url = 'https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip'

    # sdkmanager --sdk_root=<ANDROID_SDK_ROOT> --install "cmdline-tools;latest" "platform-tools" "platforms;android-31" "build-tools;31.0.0" "ndk;22.1.7171670"
    # sdkmanager --sdk_root=<ANDROID_SDK_ROOT> --install "emulator" "patcher;v4"

####################################################################################################

@task()
def show_android(ctx):
    _init_config(ctx)

    sdk = Path(ctx.build.sdk)
    ndk = Path(ctx.build.ndk)
    print(f'SDK {sdk}')

    sdkmanager = sdk / 'cmdline-tools' / 'latest' / 'bin' / 'sdkmanager'
    ctx.run(f'{sdkmanager} --list_installed', echo=True)

    with open(ndk / 'source.properties') as fh:
        for line in fh.readlines():
            if line.startswith('Pkg.Revision ='):
                ndk_revision = line.split('=')[1].strip()
                print(f'NDK {ndk_revision}   {ndk}')

####################################################################################################

@task()
def linguist(ctx):
    ts_path = ctx.build.root / 'translations' / 'xxx.fr_FR.ts'
    ctx.run(f'linguist {ts_path}')

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
    controls_path = qt_path / 'qtquickcontrols2' / 'src'
    print(controls_path)
    for root, _, filenames in os.walk(controls_path):
        root = Path(root)
        for filename in filenames:
            filename = Path(filename)
            if filename.suffix == '.qml':
                if pattern in filename.name.lower():
                    file_path = root / filename
                    print(file_path)

####################################################################################################

@task()
def find_qml(ctx, follow=False):
    directories = set()
    for root, _, filenames in os.walk(ROOT_PATH, followlinks=follow):
        root = Path(root)
        for filename in filenames:
            filename = Path(filename)
            if filename.suffix == '.qml':
                directories.add(root.relative_to(ROOT_PATH))

    pyqt = [_ for _ in directories if 'PyQt' in str(_)]
    pyside = [_ for _ in directories if 'PySide' in str(_)]
    BASE_URL = 'https://github.com/FabriceSalvaire/qt-python-examples/tree/main/'
    for wrapper in (pyside, pyqt):
        for _ in sorted(wrapper):
            title = str(_).replace('/', ' / ')
            print(f'* [{title}]({BASE_URL}{_})')

####################################################################################################

@task()
def qml(ctx, qml_path):
    _init_config(ctx)

    # qml = Path(ctx.Qt.bin_path) / 'qml')
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

@task(
    pre=[],
    optional=[],
)
def build(
        ctx,
        source,
        wipe=False,
        cmake=True,
        clean=False,
        make=True,
        deploy=False,
        verbose=True,
):
    print_section_rule()
    _init_config(ctx, source)
    is_android = ctx.build.arch.startswith('android')
    use_ninja = ctx.build.generator == 'ninja'

    env = {
        'LC_ALL': 'C',
    }

    print_info(f"Source path: {ctx.build.source}")
    print_info(f"Build path: {ctx.build.path}")
    print_info(f'Qt path: {ctx.build.qt}')
    # cmake = ctx.build.qt.parent / 'Tools' / 'CMake' / 'bin' / 'cmake'
    print_info(f"Arch: {ctx.build.arch}")
    print_info(f"Build type: {ctx.build.build_type}")
    print_info(f"CFLAGS: {ctx.build.cflags}")
    if is_android:
        print_info(f"NDK path: {ctx.build.ndk}")
        print_info(f"SDK path: {ctx.build.sdk}")

    if wipe:
        print_section(f'Wipe {ctx.build.path}')
        shutil.rmtree(ctx.build.path)

    if not ctx.build.path.exists():
        ctx.build.path.mkdir(parents=True)

    with ctx.cd(ctx.build.path):

        if clean:
            for _ in (
                    'CMakeCache.txt',
                    # 'compile_commands.json',
            ):
                _ = Path(_)
                if _.exists():
                    _.unlink()
            ctx.run(f'cmake --build {ctx.build.path} --target clean')

        if cmake:
            # /etc/security/limits.d/00-user.conf

            command = [
                'cmake',
                f'-S {ctx.build.source}',
                f'-B {ctx.build.path}',

                '-G Ninja' if use_ninja else '',
                # -D CMAKE_GENERATOR:STRING=Ninja

                f'-D CMAKE_BUILD_TYPE:STRING={ctx.build.build_type}',

                f'-D CMAKE_C_FLAGS:STRING="{ctx.build.cflags}"',
                f'-D CMAKE_CXX_FLAGS:STRING="{ctx.build.cflags}"',

                # mandatory
                f'-D CMAKE_PREFIX_PATH:PATH={ctx.build.qt_arch_path}',
                # for cross-compiling
                f'-D CMAKE_FIND_ROOT_PATH:PATH={ctx.build.qt_arch_path}',
                f'-D QT_HOST_PATH:PATH={ctx.build.qt_host_path}',
            ]

            # -DCMAKE_PROJECT_INCLUDE_BEFORE:FILEPATH=/srv/qt/Qt/Tools/QtCreator/share/qtcreator/package-manager/auto-setup.cmake

            if verbose:
                # cf. main CMakeLists.txt
                command.append("-D CMAKE_VERBOSE_MAKEFILE:BOOL=ON")

            if is_android:
                # https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html#cross-compiling-for-android
                # https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html
                ndk = Path(ctx.build.ndk)
                sdk = Path(ctx.build.sdk)
                toolchain_path = ndk / 'toolchains' / 'llvm' / 'prebuilt' / 'linux-x86_64' / 'bin'
                cmake_toolchain_path = ndk / 'build' / 'cmake' / 'android.toolchain.cmake'
                clang_path = toolchain_path / 'clang'
                ABI_MAP = {
                    'android_armv7': 'armeabi-v7a',
                    'android_x86': 'x86',
                }
                abi = ABI_MAP[ctx.build.arch]
                command += [
                    # This variable is specified on the command line when cross-compiling with
                    # CMake. It is the path to a file which is read early in the CMake run and which
                    # specifies locations for compilers and toolchain utilities, and other target
                    # platform and compiler related information.
                    # https://cmake.org/cmake/help/latest/variable/CMAKE_TOOLCHAIN_FILE.html
                    f'-D CMAKE_TOOLCHAIN_FILE:FILEPATH={cmake_toolchain_path}',

                    # Done
                    #   Must be specified to enable cross compiling for Android.
                    #   https://cmake.org/cmake/help/latest/variable/CMAKE_SYSTEM_NAME.html#variable:CMAKE_SYSTEM_NAME
                    #   '-DCMAKE_SYSTEM_NAME=Android',
                    #   Set to the Android API level
                    #   https://cmake.org/cmake/help/latest/variable/CMAKE_ANDROID_NDK.html#variable:CMAKE_ANDROID_NDK
                    #   f'-D CMAKE_ANDROID_NDK:PATH={ndk}',
                    #   https://cmake.org/cmake/help/latest/variable/CMAKE_SYSTEM_VERSION.html
                    #   '-DCMAKE_SYSTEM_VERSION=...',
                    #   https://cmake.org/cmake/help/latest/variable/CMAKE_ANDROID_ARCH_ABI.html
                    #   '-DCMAKE_ANDROID_ARCH_ABI=x86',

                    f'-D CMAKE_C_COMPILER:FILEPATH={clang_path}',
                    f'-D CMAKE_CXX_COMPILER:FILEPATH={clang_path}++',

                    f'-D ANDROID_NDK:PATH={ndk}',
                    f'-D ANDROID_SDK_ROOT:PATH={sdk}',
                    f'-D ANDROID_ABI:STRING={abi}',
                    '-D ANDROID_NATIVE_API_LEVEL:STRING=23',
                    '-D ANDROID_STL:STRING=c++_shared',

                   '-D QT_NO_GLOBAL_APK_TARGET_PART_OF_ALL:BOOL=ON',
                    f'-D QT_QMAKE_EXECUTABLE:FILEPATH={ctx.build.qmake_path}',
                ]

            command += [
                # https://sarcasm.github.io/notes/dev/compilation-database.html#cmake
                #     This will create a file name compile_commands.json in the build directory.
                '-D CMAKE_EXPORT_COMPILE_COMMANDS:STRING=ON',
            ]

            command += [
                '-D SANITIZE:STRING=OFF',
                '-D INSTRUMENT_FUNTIONS:STRING=OFF',
            ]

            command = ' '.join(command)
            print_section_rule()
            print_section('Run CMake ...')
            print_section(command.replace(' -', os.linesep + '  -'))
            ctx.run(command, echo=True, env=env)

            # if not is_android:
            #     print_section_rule()
            #     print_section('Run lupdate ...')
            #     ctx.run(f'cmake --build {ctx.build.path} --target xxx_lupdate', echo=True, warn=True)

            if not is_android:
                for _ in (
                        'compile_commands.json',
                        # 'config.h',
                ):
                    link = ctx.build.source / _
                    if link.exists():
                        link.unlink()
                    if not link.exists():
                        target = ctx.build.path / _
                        link.symlink_to(target)

        if make:
            print_section_rule()
            print_section('Run Ninja ...')
            import multiprocessing
            number_of_cpus = multiprocessing.cpu_count()
            number_of_cpus = 2
            # --target all
            # --clean-first
            # cmake --build [<dir> | --preset <preset>] [<options>] [-- <build-tool-options>]
            command = f'cmake --build {ctx.build.path} --parallel {number_of_cpus}'
            if verbose:
                command += ' --verbose'
            ctx.run(command)

        if is_android and deploy:
            # --target install
            print_section_rule()
            command = [
                str(ctx.build.qt_bin_path / 'androiddeployqt'),
                '--input {ctx.build.path}/android-touch-app-deployment-settings.json',
                '--output {ctx.build.path}/android-build',
                f'--android-platform android-{ctx.build.android_api}',
                f'--jdk {ctx.build.jdk}',
                '--gradle',
            ]
            command = ' '.join(command)
            print_section(command)
            ctx.run(command, echo=True)

####################################################################################################

@task(
    # pre=[call(build, cmake=False)]
)
def run(ctx, source):
    _init_config(ctx, source)
    build(ctx, source, cmake=ctx.build.path.exists())

    print_section_rule()
    print('Run Environment:')
    _ = yaml.dump(dict(ctx.run_env)).strip()
    print(_)
    print_section_rule()
    command = str(ctx.build.path / 'app')
    ctx.run(command, env=ctx.run_env)

####################################################################################################

@task()
def list_avd(ctx):
    _init_config(ctx)
    avdmanager = Path(ctx.build.sdk) / 'cmdline-tools' / 'latest' / 'bin' / 'avdmanager'
    command = f"{avdmanager} list avd"
    ctx.run(command)

####################################################################################################

@task()
def start_emulator(ctx, name):
    _init_config(ctx)
    emulator = Path(ctx.build.sdk) / 'emulator' / 'emulator'
    command = f"{emulator} @{name}"
    ctx.run(command)

####################################################################################################

# @task
# def clean(ctx):   # noqa:
#     for _ in (
#             'application.rcc',
#             'resources.py',
#     ):
#         (RCC_PATH / _).unlink()

####################################################################################################

# @task
# def rcc(ctx):   # noqa:
#     with ctx.cd(RCC_PATH):
#         ctx.run('pyside6-rcc application.qrc -o resources.py')
