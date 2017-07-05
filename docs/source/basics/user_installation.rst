.. gsa_module_installation:

Installing ``gsa-module``
-------------------------

Obtaining and installing ``gsa-module`` is simple.
First is to download the current version the current version hosted in bitbucket_ 
and install it to your machine locally.
``gsa-module`` is written in python3 and can be installed using ``pip``::

    > git clone https://bitbucket.org/lrs-uq/gsa-module
    > cd gsa_module
    > pip install .

Verifying the installation can be done by invoking::

    > python
    >>> import gsa_module as gsa
    >>> gsa.__version__
    '0.9.0'

If you want to modify the package on the fly without re-installing it everytime to check the effect
use the ``-e`` (editable mode) when invoking ``pip``::

    > pip install -e .

 
.. _bitbucket: https://bitbucket.org/lrs-uq/gsa-module
