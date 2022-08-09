#$ wait 1000

asciinema rec temp_test.cast --overwrite
#$ expect done

echo "Hello World"
#$ expect World

# control instructions send control command, for example ctrl-d
#$ sendcontrol d
