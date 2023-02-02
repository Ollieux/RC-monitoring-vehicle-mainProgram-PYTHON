# Rpi-Repo

## history:
echo 'HISTTIMEFORMAT="%d/%m/%y %T "' >> ~/.bashrc\
source ~/.bashrc

## ssh:
mkdir .ssh\
ssh-keygen -t rsa -C "oliwier.pszeniczko@gmail.com" -f "id_rsa_ollieux_rpi"\
eval "$(ssh-agent -s)"\
ssh-add ~/.ssh/id_rsa_ollieux_rpi\
ssh -T git@github.com

## catalog -> git:
git init
git remote add origin <>\
git config user.email <>\
git config user.name <>\
git pull origin main

# git -> catalog:
git clone http:\
git config user.email <>\
git config user.name <>