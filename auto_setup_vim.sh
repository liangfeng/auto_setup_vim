#! /usr/bin/env bash

# Fetch vim source code and build latest vim.
rm -rf ./vim/
git clone https://github.com/b4winckler/vim.git vim
cd ./vim/src/
make distclean
./configure --with-features=huge --disable-selinux --enable-cscope --enable-multibyte --without-x --enable-pythoninterp --with-compiledby='Liang Feng <liang.feng98 AT gmail DOT com>'
make
sudo make install

# Create tmp dir for vimplugins.
mkdir -p ~/tmp/

# Fetch vim cfg and plugins.
cd ~
rm -rf ~/.vim/
git clone https://github.com/liangfeng/vimrc.git .vim
ln -sf ~/.vim/_vimrc .vimrc

mkdir -p ~/.vim/bundle/
cd ~/.vim/bundle
git clone https://github.com/Shougo/neobundle.vim.git

vim -u ~/.vimrc -c "try | NeoBundleUpdate! $* | finally | qall! | endtry" -U NONE -i NONE -V1 -e -s

# Done
