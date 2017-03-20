from setuptools import setup

exec(open('gsa_module/_version.py').read())
setup(
    name="gsa-module",
    version=__version__,
    description="Package to conduct global sensitivity analysis of computer simulation",
    url="https://bitbucket.org/damar-wicaksono/gsa-module",
    author="Damar Wicaksono",
    author_email="damar.wicaksono@gmail.com",
    license="MIT",
    packages=["gsa_module"],
    scripts=["bin/create_validset"],

    # Provide the following executable scripts on the path
    entry_points={
        "console_scripts": [
            "gsa_create_sample=gsa_module.cmdln_interface:create_sample",
            "gsa_morris_generate=gsa_module.cmdln_interface:morris_generate",
            "gsa_morris_analyze=gsa_module.cmdln_interface:morris_analyze"
        ]
    },
      zip_safe=False, install_requires=['numpy']
)
