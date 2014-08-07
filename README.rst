RefactorDoc: Docstring refactor sphinx extension
================================================

.. image:: https://travis-ci.org/enthought/refactordoc.svg?branch=master
   :target: https://travis-ci.org/enthought/refactordoc
   :alt: Build status

.. image:: https://img.shields.io/coveralls/enthought/refactordoc.svg
   :target: https://coveralls.io/r/enthought/refactordoc?branch=master
   :alt: Coverage status


The RefactorDoc extension parses the function and class docstrings as
they are retrieved by the autodoc extension and refactors the section
blocks into sphinx friendly rst. The extension shares similarities
with alternatives (such as numpydoc) but aims at reflecting the
original form of the docstring.

Key aims of RefactorDoc are:

    - Do not change the order of sections.
    - Allow sphinx directives between (and inside) section blocks.
    - Easier to debug (native support for debugging) and extend
      (future versions).

Repository
----------

The RefactorDoc extension lives at Github. You can clone the repository
using::

    $ git clone https://github.com/enthought/refactordoc.git


Installation
------------

1. Install ``refactordoc`` from pypi using pip::

    $ pip install reafactordoc

2. Add refactor-doc to the extensions variable of your sphinx ``conf.py``::

    extensions = [
        ...,
        'refactordoc',
        ...,
    ]
