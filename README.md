# asciinema-automation

Asciinema-Automation is a Python package which provides a small CLI utility to automate [asciinema](https://asciinema.org) recordings. The only dependencies are asciinema and [Pexpect](https://pexpect.readthedocs.io/).

## Example

![demo](demo.gif)

This example is generated reading with `asciinema-automation` a script that calls `asciinema-automation` which reads the `hello_world.sh` example in this repository :upside_down_face:

## Installation

You need to call `git clone` to recover the source code of this repository

```bash
git clone https://github.com/PierreMarchand20/asciinema_automation.git 
```

and then call pip in your local folder of this repository to install this package and its dependencies

```bash
pip3 install . 
```

## History

This repository is inspired by [asciiscript](https://github.com/christopher-dG/asciiscript), which is not maintained any more. I first made a fork, but being not very familiar with go, I preferred to rewrite everything in python.
