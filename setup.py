from setuptools import setup


setup(name="gsa-module",
      version="0.3.0",
      description="Package to conduct global sensitivity analysis of computer simulation",
      url="https://bitbucket.org/damar-wicaksono/gsa-module",
      author="Damar Wicaksono",
      author_email="damar.wicaksono@gmail.com",
      license="MIT",
      packages=["gsa_module"],
      scripts=["bin/create_sample"],
      zip_safe=False)
