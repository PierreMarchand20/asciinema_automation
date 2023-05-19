#$ delay 50

mkdir my_folder_with_a_very_long_name
#$ expect \$

#$ delay 150

#$ send cd my_folder

#$ wait 800
#$ sendcontrol i
#$ expect name

#$ wait 80
#$ delay 50

#$ sendcontrol m
#$ expect \$

basename $PWD
#$ expect \$
