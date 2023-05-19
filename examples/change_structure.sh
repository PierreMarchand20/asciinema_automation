#$ delay 50

mkdir my_directory
#$ expect \$

cd my_directory
#$ expect \$

basename $PWD
#$ expect my_directory\r\n

touch my_textfile.txt
#$ expect \$

ls
#$ expect my_textfile.txt\r\n

rm my_textfile.txt
#$ expect \$

ls 
#$ expect \$

cd ..
#$ expect \$

rm -r my_directory
#$ expect \$

ls
#$ expect \$
