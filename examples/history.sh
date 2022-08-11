touch my_first_file.txt
#$ expect \r\n

touch my_second_file.txt
#$ expect \r\n

rm my_first_file.txt
#$ expect \r\n

#$ delay 1000 
#$ sendarrow up 3
#$ expect first_file.txt
#$ wait 1000 
