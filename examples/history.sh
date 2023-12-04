#$ delay 50

touch my_first_file.txt
#$ expect \$

touch my_second_file.txt
#$ expect \$

rm my_first_file.txt
#$ expect \$

#$ delay 800

#$ sendarrow up 1
#$ expect rm my_first_file.txt

#$ sendarrow up 1
#$ expect touch my_second_file.txt

#$ sendarrow up
#$ expect first_file.txt

#$ delay 10

#$ sendcontrol m
#$ expect \$

ls
#$ expect \$
