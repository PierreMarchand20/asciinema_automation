#$ delay 10
cat examples/hello_world.sh

#$ wait 5000
asciinema-automation --asciinema-arguments " --overwrite" examples/hello_world.sh examples/test.cast

#$ expect delay
asciinema play examples/test.cast
