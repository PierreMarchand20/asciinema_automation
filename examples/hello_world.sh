echo "Hello world"
#$ expect world

# wait instructions change the time between instructions
#$ wait 1000

echo "I have waited 1000ms"
#$ expect 1000ms

# delay instructions change the time (or mean of gaussian if standart deviation is given) between key strokes
#$ delay 10
echo "I am writing with a 10ms delay"
#$ expect delay
