git add --all
echo "shell executed: git add --all"
echo "enter commit label: "
read inp
git commit -m  "$inp"
echo "shell executed: git commit -m : '$inp'" 
git push heroku master
echo "shell executed: git push heroku master"
