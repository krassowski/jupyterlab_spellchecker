import json
from pathlib import Path

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    skip_if_exists
)
import setuptools

HERE = Path(__file__).parent.resolve()

# The name of the project
name = "jupyterlab-spellchecker"

lab_path = (HERE / name.replace('-', '_') / "labextension")

# Representative files that should exist after a successful build
jstargets = [
    str(lab_path / "package.json"),
]

package_data_spec = {
    name: ["*"],
}

labext_name = "@ijmbarr/jupyterlab_spellchecker"

data_files_spec = [
    ("share/jupyter/labextensions/%s" % labext_name, str(lab_path), "**"),
    ("share/jupyter/labextensions/%s" % labext_name, str(HERE), "install.json"),
    ("share/jupyter/dictionaries", str(HERE / "dictionaries"), "**"),
    ("etc/jupyter/jupyter_notebook_config.d", "jupyter-config/jupyter_notebook_config.d", "jupyterlab_spellchecker.json"),
    ("etc/jupyter/jupyter_server_config.d", "jupyter-config/jupyter_server_config.d", "jupyterlab_spellchecker.json"),
]

cmdclass = create_cmdclass("jsdeps",
    package_data_spec=package_data_spec,
    data_files_spec=data_files_spec
)

js_command = combine_commands(
    install_npm(HERE, build_cmd="build:prod", npm=["jlpm"]),
    ensure_targets(jstargets),
)

is_repo = (HERE / ".git").exists()
if is_repo:
    cmdclass["jsdeps"] = js_command
else:
    cmdclass["jsdeps"] = skip_if_exists(jstargets, js_command)

long_description = (HERE / "README.md").read_text()

# Get the package info from package.json
pkg_json = json.loads((HERE / "package.json").read_bytes())

setup_args = dict(
    name=name,
    version=pkg_json["version"],
    url=pkg_json["homepage"],
    project_urls={
        'Bug Tracker': pkg_json["bugs"]["url"],
        'Source Code': pkg_json["homepage"]
    },
    author=pkg_json["author"]["name"],
    description=pkg_json["description"],
    license=pkg_json["license"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    cmdclass=cmdclass,
    packages=setuptools.find_packages(),
    install_requires=[
        "babel",
        "jupyterlab~=3.0",
    ],
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.6",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "JupyterLab", "JupyterLab3"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Jupyter",
        "Framework :: Jupyter :: JupyterLab",
        "Framework :: Jupyter :: JupyterLab :: 3",
        "Framework :: Jupyter :: JupyterLab :: Extensions",
        "Framework :: Jupyter :: JupyterLab :: Extensions :: Prebuilt"
    ],
)


if __name__ == "__main__":
    setuptools.setup(**setup_args)
