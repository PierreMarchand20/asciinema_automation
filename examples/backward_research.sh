touch my_first_file.txt
#$ expect \r\n

touch my_second_file.txt
#$ expect \r\n

rm my_first_file.txt
#$ expect \r\n

#$ sendcontrol r

#$ delay 500

#$ send tou
#$ expect my_second_file.txt

#$ wait 1000

#$ sendcontrol r
#$ expect first_file.txt

#$ sendcontrol m
#$ wait 80
#$ delay 150
#$ expect \n


ls my_first_file.txt
#$ expect first_file.txt
