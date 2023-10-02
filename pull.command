ssh-add -D
ssh-add ~/.ssh/jinningsjtu
cd `dirname $0`
git pull origin master
ssh-add -D
ssh-add ~/.ssh/jinningli
