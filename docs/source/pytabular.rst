.. PyTabular documentation master file, created by
   sphinx-quickstart on Sun Jan 26 14:24:53 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyTabular's documentation!
=====================================

PyTabular is a Python package for processing LateX tables. Create a table
from existing Excel or csv documents, or use Python array-like objects. Then
customize the look of your tables with built-in methods. 

Advantages
----------

- array indexing
- power and control: operate on the whole table, rows, columns, and even cells!
- formatting options: bold, emphasis, underline, rotation, fontsize, spacing, color
- horizontal and vertical lines by cell, row, column
- alignment by cell, row, column
- merging
- custom formatting
- support for longtables

Dependences
-----------

Latex Packages:

- booktabs
- makecell
- longtable
- multirow
- ulem
- tabu
- caption
- pdflscape
- xcolor (with table option)

Latex Commands:

    - \renewcommand{\rothead}[2][60]{\makebox[9mm][c]{\rotatebox{#1}{\makecell[c]{#2}}}}
    - \newcommand{\mc}{\multicolumn}
    - \newcommand{\mr}{\multirow}

Python Packages:

- numpy

Installation
------------

::

	pip install pytabular

Updating pytabular
------------------

::

	pip install --upgrade pytabular

How to Use PyTabular
--------------------
We hope that PyTabular is easy to use. We provide a
`tutorial <http://jaketorcasso.com/tutorials/PyTabular_tutorial>`_ 
to help.

Indices
=======

* :ref:`modindex`