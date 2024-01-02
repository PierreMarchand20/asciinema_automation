#$ delay 10

cat ./hello_world.sh
#$ expect \$

asciinema-automation --asciinema-arguments "--overwrite -c 'env -i PS1=\"$ \" bash --noprofile --norc'" ./hello_world.sh ./test.cast
#$ expect \$ 
# change \$  to your prompt, or remove to just wait

asciinema play ./test.cast
#$ expect exit
#$ expect \$
