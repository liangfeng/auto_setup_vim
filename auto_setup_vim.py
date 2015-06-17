#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
from subprocess import call
import os
from os import path

def get_vim_src_dir():
    return path.join(sys.path[0], '..', 'vim_src')

def get_vim_cfg_dir():
    vim_cfg_dir = ''
    if sys.platform.startswith('linux'):
        vim_cfg_dir = path.join(path.expanduser('~'), '.vim')
    elif sys.platform.startswith('win'):
        vim_cfg_dir = path.join(path.expanduser('~'), 'vimfiles')
    return vim_cfg_dir

def get_vim_installed_dir_on_win():
    # XXX: When new version vim released, need change version number.
    return r'C:\Program Files (x86)\Vim\vim74'

def get_vs_dev_cmd_on_win():
    # XXX: When install new version visual c++, need change path.
    os.environ['SDK_INCLUDE_DIR'] = r'C:\Program Files (x86)\Microsoft SDKs\Windows\v7.1A\Include'
    return r'C:\Program Files (x86)\Microsoft Visual Studio 12.0\Common7\Tools\VsDevCmd.bat'

# install python-devel and lua-devel, if necessary and on Linux.
def install_dep_libs():
    import platform
    if platform.linux_distribution()[0] in {'Ubuntu','debian'}:
        call('sudo apt-get -y install clang libpython2.7 libpython2.7-dev libpython3-dev > /dev/null', shell=True)
        call('sudo apt-get -y install luajit libluajit-5.1-2 libluajit-5.1-dev > /dev/null', shell=True)
        call('sudo apt-get -y install xorg-dev  libreadline6-dev libncurses5-dev libgnome2-dev libgnomeui-dev > /dev/null', shell=True)
        call('sudo apt-get -y install libgtk2.0-dev libatk1.0-dev libbonoboui2-dev libcairo2-dev libx11-dev libxpm-dev libxt-dev > /dev/null', shell=True)
    elif platform.linux_distribution()[0] in {'centos', 'redhat'}:
        call('sudo yum -y install python-devel > /dev/null', shell=True)
        call('sudo yum -y install lua-devel > /dev/null', shell=True)

# get latest vim src from github.
def get_vim_src():
    vim_src_dir = get_vim_src_dir()
    if path.exists(vim_src_dir):
        os.chdir(vim_src_dir)
        print 'Updating vim src...'
        call('git pull', shell=True)
        os.chdir('..')
    else:
        print 'Cloning vim src...'
        call('git clone https://github.com/b4winckler/vim.git ' + vim_src_dir, shell=True)

# install vim hybird version(GUI&Console) from src on linux.
def install_vim_on_linux():
    call('make distclean', shell=True)

    configure_cmd = []
    configure_cmd.append('./configure')
    configure_cmd.append('--with-features=huge')
    configure_cmd.append('--disable-selinux')
    configure_cmd.append('--disable-netbeans')
    configure_cmd.append('--enable-cscope')
    configure_cmd.append('--enable-multibyte')
    configure_cmd.append('--enable-pythoninterp=dynamic')
    configure_cmd.append('--enable-python3interp=dynamic')
    configure_cmd.append('--enable-luainterp=dynamic')
    configure_cmd.append('--with-luajit')
    configure_cmd.append('--enable-gui=gnome2')
    configure_cmd.append("--with-compiledby='Liang Feng <liang.feng98 AT gmail DOT com>'")
    call(' '.join(configure_cmd), shell=True)

    call('make -j 16', shell=True)
    call('sudo make install', shell=True)

# install vim from src on win.
def install_vim_on_win():
    build_console_options = []
    build_console_options.append('nmake -f Make_mvc.mak')
    build_console_options.append('FEATURES=HUGE')
    build_console_options.append('MBYTE=yes')
    build_console_options.append('CSCOPE=yes')
    build_console_options.append('SNIFF=no')
    build_console_options.append('NETBEANS=no')
    build_console_options.append('CPUNR=pentium4')
    build_console_options.append('DEBUG=no')
    build_console_options.append('MAP=yes')
    build_console_options.append('PYTHON=C:\Python27')
    build_console_options.append('PYTHON_VER=27')
    build_console_options.append('DYNAMIC_PYTHON=yes')
    build_console_options.append('LUA=C:\luajit')
    build_console_options.append('LUA_VER=51')
    build_console_options.append('DYNAMIC_LUA=yes')
    build_console_options.append('USERNAME="Liang Feng <liang.feng98 AT gmail DOT com>"')
    build_console_options.append('USERDOMAIN=China')

    build_gui_options = []
    build_gui_options.extend(build_console_options)
    build_gui_options.append('GUI=yes')
    build_gui_options.append('DIRECTX=yes')
    build_gui_options.append('OLE=yes')
    build_gui_options.append('IME=yes')
    build_gui_options.append('GIME=yes')

    # build console version, cleanup first.
    build_console_cmd = 'call ' + '"' + get_vs_dev_cmd_on_win() + '"' + ' & ' + ' '.join(build_console_options)
    call(build_console_cmd + ' clean', shell=True)
    call(build_console_cmd, shell=True)

    # build GUI version, cleanup first.
    build_gui_cmd = 'call ' + '"' + get_vs_dev_cmd_on_win() + '"' + ' & ' + ' '.join(build_gui_options)
    call(build_gui_cmd + ' clean', shell=True)
    call(build_gui_cmd, shell=True)

    call('xcopy ' + get_vim_src_dir() + r'\runtime ' + '"' + get_vim_installed_dir_on_win() + '"' + r' /D /E /H /I /Y', shell=True)
    call('xcopy ' + get_vim_src_dir() + r'\src\xxd\xxd.exe ' + '"' + get_vim_installed_dir_on_win() + '"' + r'\*' + r' /D /Y', shell=True)
    call('xcopy ' + get_vim_src_dir() + r'\src\*.exe ' + '"' + get_vim_installed_dir_on_win() + '"' + r'\*' + r' /D /Y', shell=True)
    call('xcopy ' + get_vim_src_dir() + r'\src\*.pdb ' + '"' + get_vim_installed_dir_on_win() + '"' + r'\*' + r' /D /Y', shell=True)
    call('xcopy ' + get_vim_src_dir() + r'\src\*.map ' + '"' + get_vim_installed_dir_on_win() + '"' + r'\*' + r' /D /Y', shell=True)

# install latest vim from src.
def install_vim():
    vim_src_dir = get_vim_src_dir()
    os.chdir(path.join(vim_src_dir, 'src'))

    print 'Installing vim...'
    if sys.platform.startswith('linux'):
        install_vim_on_linux()
    elif sys.platform.startswith('win'):
        install_vim_on_win()

# get vimrc from github
def get_vim_cfg():
    if path.exists(get_vim_cfg_dir()):
        os.chdir(get_vim_cfg_dir())
        print 'Updating vimrc ...'
        call('git pull', shell=True)
        os.chdir('..')
    else:
        print 'Cloning vimrc ...'
        call('git clone https://github.com/liangfeng/dotvim.git ' + '"' + get_vim_cfg_dir() + '"', shell=True)

    if sys.platform.startswith('linux'):
        os.chdir(path.expanduser('~'))
        call('ln -sf ~/.vim/vimrc .vimrc', shell=True)

# get vim cfg and install plugins from github.
def install_vim_plugins():
    os.chdir(get_vim_cfg_dir())

    bundle_dir = 'bundle'
    if not path.exists(bundle_dir):
        os.mkdir(bundle_dir)
    os.chdir(bundle_dir)

    # install neobundle.vim
    if path.exists('neobundle.vim'):
        os.chdir('neobundle.vim')
        print 'Updating neobundle.vim...'
        call('git pull', shell=True)
        os.chdir('..')
    else:
        print 'Cloning neobundle.vim...'
        call('git clone https://github.com/Shougo/neobundle.vim.git', shell=True)

    # install vimproc.vim
    if path.exists('vimproc.vim'):
        os.chdir('vimproc.vim')
        print 'Updating vimproc.vim...'
        call('git pull', shell=True)
        os.chdir('..')
    else:
        print 'Cloning vimproc.vim...'
        call('git clone https://github.com/Shougo/vimproc.vim.git', shell=True)

    os.chdir('vimproc.vim')

    print 'Building vimproc.vim...'
    if sys.platform.startswith('linux'):
        call('make', shell=True)
    elif sys.platform.startswith('win'):
        build_vimproc_cmd = 'call ' + '"' + get_vs_dev_cmd_on_win() + '"' + ' & ' + r'nmake -f make_msvc.mak'
        call(build_vimproc_cmd, shell=True)

    if sys.platform.startswith('linux'):
        vimrc_file = path.join(path.expanduser('~'), '.vimrc')
    elif sys.platform.startswith('win'):
        vimrc_file = path.join(path.join(path.expanduser('~'), 'vimfiles'), 'vimrc')

    print 'Installing left plugins...'
    call(r'vim -u ' + '"' + vimrc_file + '"' + r' -c "try | NeoBundleUpdate! | finally | qall! | endtry" -U NONE -i NONE -V1 -e -s', shell=True)
    print

# entry function
def main():
    install_dep_libs()
    get_vim_src()
    install_vim()
    get_vim_cfg()
    install_vim_plugins()
    print 'Vim auto setup done.'

if __name__ == '__main__':
    main()

# vim: set et sw=4 ts=4 ff=unix:
