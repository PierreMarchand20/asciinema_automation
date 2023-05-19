#$ delay 50

touch my_first_file.txt
#$ expect \$

touch my_second_file.txt
#$ expect \$

rm my_first_file.txt
#$ expect \$

#$ sendcontrol r

#$ delay 500

#$ send touch
#$ expect second

#$ wait 1000

#$ sendcontrol r
#$ expect first

#$ sendcontrol m
#$ expect \$

#$ wait 80
#$ delay 50

ls my_first_file.txt
#$ expect \$
