ssh-add -D
ssh-add ~/.ssh/jinningsjtu
cd `dirname $0`
python process.py
git add .
git commit -m "new commit"
git push origin master
ssh-add -D
ssh-add ~/.ssh/jinningli
