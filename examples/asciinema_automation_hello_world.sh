#$ delay 10
cat examples/hello_world.sh

asciinema-automation --asciinema-arguments " --overwrite" examples/hello_world.sh examples/test.cast

#$ expect delay
#$ wait 5000
asciinema play examples/test.cast
