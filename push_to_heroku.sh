git add --all
echo "executed: git add --all"
echo "enter commit label: "
read inp
git commit -m  "$inp"
echo "executed: git commit -m : '$inp'" 
git push heroku master
echo "executed: git push heroku master"
