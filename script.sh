python cron.py quizz &
while true; do
  python quizz.py
  echo "RESTART QUIZZ"
done
