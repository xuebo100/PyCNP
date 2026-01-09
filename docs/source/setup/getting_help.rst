Getting help
=============

All conversations take place in the `GitHub repository <https://github.com/xuebo100/PyCNP/>`_.
If you are looking for help using PyCNP, please browse the `discussions <https://github.com/xuebo100/PyCNP/discussions>`_ page first for relevant discussions, questions and answers, modelling tips, and more.
Feel free to open your own discussion thread if you have something new to discuss!


Submitting a bug report
-----------------------

Open a new issue in the repository, using the "Bug report" template.
To help us resolve your issue quickly, please include:

* A short, self-contained code snippet that reproduces the problem
* The version of ``pycnp`` you are using
* Your operating system and Python version
* Any error messages or tracebacks

To get version information, run:

.. code-block:: python

   import pycnp
   print(pycnp.__version__)

Or from the command line:

.. code-block:: shell

   python -c 'import pycnp; print(pycnp.__version__)'


Submitting a feature request
----------------------------

Please first browse the existing issues and discussions to see if your feature has already been requested.
If not, please open a new issue in the repository, using the "Feature request" template.


Citing PyCNP
------------

If you use PyCNP in your research, please cite the following paper:

.. code-block:: bibtex

   @article{pycnp2026,
     title={PyCNP: An Open-Source Python Package for Critical Node Detection Problems},
     author={Yangming Zhou and Bo Xue and MengChu Zhou and Tieju Ma},
     year={2026},
   }