#$ delay 10

mkdir my_folder_with_a_very_long_name
#$ expect \r\n

#$ delay 150

#$ send cd my_folder

#$ wait 800
#$ sendcontrol i
#$ expect name

#$ sendcontrol m
#$ expect \n

pwd
#$ expect very_long_name
