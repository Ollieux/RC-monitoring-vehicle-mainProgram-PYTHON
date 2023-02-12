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
git init\
git remote add origin <>\
git config user.email oliwier.pszeniczko@gmail.com\
git config user.name Ollieux\
git pull origin main

## git -> catalog:
git clone http:<>\
git config user.email oliwier.pszeniczko@gmail.com\
git config user.name Ollieux\

##Open-cv:
pip install opencv-python==4.5.3.56

## Owner change:
git rebase -i --root\
git commit --amend --author="Ollieux <oliwier.pszeniczko@gmail.com>" --no-edit\
git rebase --continue\
