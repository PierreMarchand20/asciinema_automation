#$ delay 10
mkdir my_folder_with_a_very_long_name

#$ delay 150

#$ expect 
#$ send 
cd my_folder

#$ expect name
#$ wait 800
#$ sendcontrol i

#$ expect \n
#$ sendcontrol m

#$ send \n
pwd 
