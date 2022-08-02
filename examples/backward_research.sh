touch my_first_file.txt

touch my_second_file.txt

rm my_first_file.txt

#$ expect
#$ send 
#$ control r
#$ expect my_second_file.txt
#$ delay 500
tou

#$ wait 1000
#$ expect first_file.txt
#$ sendcontrol r

#$ expect \n
#$ sendcontrol m
