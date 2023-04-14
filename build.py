# -*- coding: utf-8 -*-
import argparse
import contextlib
import os
import re
import shutil
import subprocess
import sys
import zipapp
from pathlib import Path


BUILD_DIR = "build"
SRC = [
    "backend",
    ("frontend/dist", "frontend")
]
RESULT = "partyDecider.pyz"
MAIN = "backend.__main__:main"
PY_COMPILE = ["python3.10", "python3.11"]
EXTRA_MAIN = """
import backend
backend.config.IS_ZIP_APP = True
"""


def check_call(args, **kwargs) -> int:
    print("#", *args)
    return subprocess.check_call(args, **kwargs)


def check_output(args, **kwargs) -> str:
    print("#", *args)
    return subprocess.check_output(args, **kwargs).decode(sys.getdefaultencoding())


def load_toml(f: open):
    try:
        import tomllib as lib
    except ImportError:
        try:
            import tomlkit as lib
        except ImportError:
            raise ImportError(
                "Neither tomllib nor tomlkit exist."
                " Please install tomlkit or use at least Python 3.11"
            )
    return lib.load(f)


def get_pkg_deps(pkgs: list[str] | set[str]) -> set[str]:
    output = check_output(["pip", "show", *pkgs]).split("\n")
    result = set()
    for line in output:
        if line.startswith("Requires: "):
            for pkg in line.removeprefix("Requires: ").split(","):
                pkg = pkg.strip()
                if pkg:
                    result.add(pkg)
    return result


def get_dep_tree(pkgs: list[str]) -> set[str]:
    """
    Iteratively resolve dependencies for given packages.
    If a package has unresolved dependencies,
    resolve their dependencies until no unresolved dependencies exist.
    """
    found_deps = set(pkgs)
    unchecked = set(found_deps)
    while unchecked:
        now = get_pkg_deps(unchecked)
        unchecked = now - found_deps
        found_deps |= unchecked
    return found_deps


def get_deps() -> list[str]:
    """
    Get exactly installed dependencies from packages that are listed in pyproject.toml dependencies list.
    """
    pkg_pattern = re.compile(r"^([\w_-]+).=.+")

    with open("pyproject.toml", "rb") as f:
        data = load_toml(f)
    deps: list[str] = data["project"]["dependencies"]
    dep_names = [pkg_pattern.match(pkg).group(1) for pkg in deps]
    all_deps = get_dep_tree(dep_names)

    installed = check_output(["pip", "--require-virtualenv", "freeze"]).split("\n")
    required_installed = []
    for pkg in installed:
        if not pkg.strip():
            continue
        name = pkg_pattern.match(pkg).group(1)
        if name in all_deps:
            required_installed.append(pkg)

    print("Project dependencies:", ", ".join(deps))
    print("Installed:", ", ".join(required_installed))

    return required_installed


def make_filter(no_cache: bool) -> callable:
    def file_filter(path: Path) -> bool:
        """
        Filter contents that is being added into the archive.
        Do not include:
        - bin/*
        - *.dist-info/
        """
        if no_cache and "__pycache__" in path.parts:
            return False
        return path.parts[0] != "bin" and not path.parts[0].endswith(".dist-info")

    return file_filter


def copy_deps():
    # Resolve all required dependencies.
    deps = get_deps()

    if deps:
        # Install dependencies into the build directory.
        check_call(
            [
                "pip",
                "--disable-pip-version-check",
                "install",
                # "--platform", "none",
                # "--only-binary", ":all:",
                "--target",
                BUILD_DIR,
                *deps,
            ]
        )


def compile_all():
    with contextlib.chdir(BUILD_DIR):
        for v in PY_COMPILE:
            cmd = [v, "-m", "compileall", "."]
            try:
                check_call(cmd)
            except OSError as e:
                print("- failed to execute:", e.args[0])


def build_node_stuff(args):
    with contextlib.chdir("frontend"):
        if args.preview:
            cmd = ["npm", "run", "preview"]
        else:
            cmd = ["npm", "run", "build"]
        check_call(cmd)


def copy_files():
    for s in SRC:
        if isinstance(s, tuple):
            src, dst = s
            dst = os.path.join(BUILD_DIR, dst)
        else:
            src = s
            dst = os.path.join(BUILD_DIR, s)

        if os.path.isdir(src):
            print("# cp -r", src, dst)
            shutil.copytree(src, dst, dirs_exist_ok=True)
        elif os.path.isfile(src) or os.path.islink(src):
            print("# cp", src, dst)
            shutil.copyfile(src, dst)
        else:
            raise FileNotFoundError(src)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--keep",
        "-k",
        action="store_true",
        help="Don't remove build directory first if it exists.",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Do quick update of project code. Implies --keep",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Compile frontend in preview mode (without minification) instead of build.",
    )

    args = parser.parse_args()

    if not args.keep and not args.quick and os.path.exists(BUILD_DIR):
        print("# rm -rf", BUILD_DIR)
        shutil.rmtree(BUILD_DIR)

    if not os.path.exists(BUILD_DIR):
        print("# mkdir", BUILD_DIR)
        os.mkdir(BUILD_DIR)

    if not args.quick:
        copy_deps()

    with open(os.path.join(BUILD_DIR, "__main__.py"), "wt") as f:
        pkg, fn = MAIN.split(":")
        f.write(
            f"""\
import {pkg}
{EXTRA_MAIN}
{pkg}.{fn}()
"""
        )

    if not args.quick:
        compile_all()

        build_node_stuff(args)

    copy_files()

    print("# zipapp", BUILD_DIR, "-o", RESULT)
    zipapp.create_archive(
        source=BUILD_DIR,
        target=RESULT,
        interpreter="/usr/bin/env python",
        compressed=True,
        filter=make_filter(args.quick),
    )


if __name__ == "__main__":
    main()
