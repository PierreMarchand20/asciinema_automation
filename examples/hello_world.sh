# delay instructions change the time (or mean of gaussian if standard deviation is given) between key strokes
#$ delay 50

echo "Hello world"
#$ expect \$

# wait instructions change the time between instructions
#$ wait 1000

echo "I have waited 1000ms"
#$ expect \$

#$ delay 10
echo "I am writing with a 10ms delay"
#$ expect \$
