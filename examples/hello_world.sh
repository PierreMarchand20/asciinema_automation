# mean of gaussian delay between key strokes, default to 50ms
#$ delay 150

echo "Hello world"
#$ expect \$

# wait instructions change the time between instructions, default to 80ms
#$ wait 1000

echo "I now wait 1000ms"
#$ expect \$

#$ delay 10
echo "I am writing with a 10ms delay"
#$ expect \$
