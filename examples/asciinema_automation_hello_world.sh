#$ delay 10

cat examples/hello_world.sh
#$ expect expect delay

asciinema-automation --asciinema-arguments " --overwrite" examples/hello_world.sh examples/test.cast
#$ expect bash-3.2\$ 
# change bash-3.2\$  to your prompt, or remove to just wait

asciinema play examples/test.cast
#$ expect delay\r\n
