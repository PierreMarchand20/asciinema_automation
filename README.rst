asciinema-automation
####################

.. image:: https://badge.fury.io/py/asciinema-automation.svg
    :target: https://badge.fury.io/py/asciinema-automation

.. image:: https://github.com/PierreMarchand20/asciinema_automation/actions/workflows/CI.yml/badge.svg
    :target: https://github.com/PierreMarchand20/asciinema_automation/actions/workflows/CI.yml

asciinema-automation is a Python package which provides a small CLI utility to automate `asciinema <https://asciinema.org>`_ recordings. The only dependencies are asciinema and `Pexpect <https://pexpect.readthedocs.io/>`_.

Recording is made easier by:

- making the live recording for you, to get the perfect take in one go (no more missed keys!),
- while looking not too robotic by adding Gaussian delay between keystrokes.

One specificity of this package is that 

- it makes automated recording as **reproducible and robust** as possible. In particular, there is no need to add a manually set waiting time between commands to wait for previous outputs. 

To that end, you can write the commands you wish to showcase in a text file, and using comment lines starting by :code:`#$` (see `examples` folder and `example`_), you can specify the expected output of each command, and/or change the configuration of the automated recording on-the-fly.

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
