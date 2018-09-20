#!/bin/bash

# Update and upgrade.
sudo apt-get update
sudp apt-get upgrade

# Install softwares.

## Coding language.
sudo apt-get install python
sudo apt-get install python3
sudo apt-get install python-pip
sudo apt-get install python3-pip

sudo apt-get install golang-1.10
sudo apt-get install mysql-server
sudo apt-get install mysql-client
sudo apt-get install redis-server
sudo apt-get install redis-client

## Coding softwares and tools.
sudo apt-get install vscode
sudo apt-get install git
sudo apt-get install tig
sudo apt-get install htop
sudo apt-get install mysql-workbench
sudo apt-get install redis-desktop-manager
sudo apt-get install wireshark
sudo apt-get install postman
sudo apt-get install charles
sudo apt-get install remmina
sudo apt-get install teamviewer
sudo apt-get install tesseract-ocr
sudo apt-get install zsh
sudo sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

## Python requirements.
pip3 install requests
pip3 install PyMySQL
pip3 install configparser
pip3 install lxml
pip3 install redis
pip3 install pillow
pip3 install pytesseract
pip3 install tornado
pip3 install beautifulsoup4
pip3 install gevent

## Golang PATH setting.
sudo ln -s /usr/lib/go-1.10/bin/go /usr/bin/go
sudo mkdir ~/path/
sudo mkdir /data/
sudo mkdir /data/code/
sudo mkdir /data/code/com
sudo mkdir /data/code/com/go
sudo mkdir /data/bin/
sudo mkdir ~/com/
sudo mkdir ~/com/go/

echo "GOROOT=/usr/bin/go" > ~/path/gopath.rc
echo "GOBIN=$GOROOT/bin" >> ~/path/gopath.rc
echo "PATH=$PATH:$GOBIN:$GOROOT:/data/bin/" >> ~/path/gopath.rc
echo "GOPATH=/data/code/com/go" >> ~/path/gopath.rc
echo "export GOROOT GOBIN PATH GOPATH" >> ~/path/gopath.rc

sudo echo "source ~/path/gopath.rc" >> /etc/profile
source /etc/profile

## Other config
git config --global user.name "tau"
git config --global user.email "tauwoo@seuxw.cc"

cd /data/bin/
wget https://raw.githubusercontent.com/TauWu/auto_post/master/bin/geckodriver