asciinema-automation
####################

.. image:: https://badge.fury.io/py/asciinema-automation.svg
    :target: https://badge.fury.io/py/asciinema-automation

Asciinema-Automation is a Python package which provides a small CLI utility to automate `asciinema <https://asciinema.org>`_ recordings. The only dependencies are asciinema and `Pexpect <https://pexpect.readthedocs.io/>`_.

Example
-------

.. image:: https://raw.githubusercontent.com/PierreMarchand20/asciinema_automation/main/demo.gif
    :alt: Demo

This example is generated reading with ``asciinema-automation`` a script that calls ``asciinema-automation`` which reads the ``hello_world.sh`` example in this repository 🙃

Numerous examples can also be found `here <https://github.com/PierreMarchand20/asciinema_playground>`_.

Installation
------------

You can use `pip <https://pip.pypa.io/en/stable/>`_ to install:

.. code:: bash
    
    python3 -m pip install asciinema-automation

Or you can install it directly using this GitHub repository. In this case, you need to call ``git clone`` to recover the source code of this repository

.. code:: bash
    
    git clone https://github.com/PierreMarchand20/asciinema_automation.git 


and then call pip in your local folder of this repository to install this package and its dependencies

.. code:: bash
    
    pip3 install . 


History
-------

This repository is inspired by `asciiscript <https://github.com/christopher-dG/asciiscript>`_, which is not maintained any more. I first made a fork, but being not very familiar with go, I preferred to rewrite everything in python.
