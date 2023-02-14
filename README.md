# Rpi-Repo

## history:
echo 'HISTTIMEFORMAT="%d/%m/%y %T "' >> ~/.bashrc \
source ~/.bashrc

## ssh:
mkdir .ssh \
ssh-keygen -t rsa -C "oliwier.pszeniczko@gmail.com" -f "id_rsa_ollieux_rpi" \
eval "$(ssh-agent -s)" \
ssh-add ~/.ssh/id_rsa_ollieux_rpi \
ssh -T git@github.com

## catalog -> git:
git init\
git remote add origin <> \
git config user.email oliwier.pszeniczko@gmail.com \
git config user.name Ollieux \
git pull origin main

## git -> catalog:
git clone http:<> \
git config user.email oliwier.pszeniczko@gmail.com \
git config user.name Ollieux \

##Open-cv:
sudo apt-get install python3-pip python3-virtualenv

mkdir project \
cd project/
virtualenv env

sudo apt install -y build-essential cmake pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5 python3-dev

pip install --upgrade pip setuptools wheel

pip install opencv-python==4.5.3.56

## Owner change:
git rebase -i --root\
git commit --amend --author="Ollieux <oliwier.pszeniczko@gmail.com>" --no-edit\
git rebase --continue\

## Wifi
sudo apt-get install -y linux-headers \
git clone https://github.com/lwfinger/rtl8188eu.git \
cd rtl8188eu/ \
make \
sudo make install \
sudo reboot \
sudo nano /etc/network/interfaces \
sudo nano /etc/wpa_supplicant.conf

## additonal
sudo apt-get install conky \
pip install imutils


