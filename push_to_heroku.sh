git add --all
echo "shell executed: git add --all"
#echo "enter commit label: "
#read inp
#git commit -m  "$inp"
git commit -m "updating app"
echo 'shell executed: git commit -m "updating app"' 
echo "shell executing...: git push heroku master"
git push heroku master
