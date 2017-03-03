from setuptools import setup


setup(
    name="gsa-module",
    version="0.5.2",
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
            "gsa_morris_generate=gsa_module.cmdln_interface:morris_generate"
        ]
    },
      zip_safe=False
)
