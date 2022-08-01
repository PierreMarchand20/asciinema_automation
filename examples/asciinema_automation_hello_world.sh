cat examples/hello_world.sh

#$ wait 1000
asciinema-automation --asciinema-arguments " --overwrite" examples/hello_world.sh test.cast

asciinema play test.cast
