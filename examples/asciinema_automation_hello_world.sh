#$ delay 10
cat examples/hello_world.sh

#$ expect bash-3.2\$ (change \$ to your prompt, or change expect instruction to wait instruction)
asciinema-automation --asciinema-arguments " --overwrite" examples/hello_world.sh examples/test.cast

#$ expect delay\r\n
asciinema play examples/test.cast
