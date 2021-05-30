# Remesh Prompt

## Overview
This is a django mvt project with sqlite that aims to recreate a simple version of remesh.

This is for interview purposes at remesh.ai.

## Homepage
https://github.com/MajorZiploc/remesh_prompt

## All scripts mentioned in this readme need to be copied from the readme rendered in a markdown renderer. Not copied directly from this README file. You can copy straight from the github home page of this project

## Requirements
- Assumes global python is v3 for creation of the virtual environment
- python 3.8.x
- pip 20.x.x or 21.x.x
- python3-venv
- bash --version GNU bash, version 5.x.xx

## Development tools
- vscode
- python extension for vscode - ms-python.python
- pylance extension for vscode - ms-python.vscode-pylance
- bash --version GNU bash, version 5.0.17(1)-release (x86\_64-pc-linux-gnu)
- wsl ubuntu 20.04 windows 10
- python 3.8.5
- pip 20.0.2

## Setup the project - Uses Django 'python manage.py <command>' flow - Refer to the Troubleshooting section at the bottom of this README if you run into problems

### Go into the server folder. All server commands assume you are in that directory.

> cd ./server


NOTE: all \*.sh files will work regardless of what directory you call them from

### first time up front setup - creation of python virtual environment
> mkdir -p ~/.virtualenvs && python -m venv ~/.virtualenvs/remesh\_prompt\_server

### launch virtual environment
> source ~/.virtualenvs/remesh\_prompt\_server/bin/activate

### install dependencies
> pip install -e .

### NOTE: All following scripts assume you have the python virtual environment created, installed, and active from the above steps

### run migrations for db (makes migrations and performs the migrations)
> ./utility\_scripts/quick\_migrations.sh

### run server
> ./utility\_scripts/run\_server.sh

### visit local website - copy the following and put into a web browser
> http://127.0.0.1:8000/

### run tests
> ./utility\_scripts/run\_tests.sh

### (optional) Create super user to use admin pages
> python manage.py createsuperuser

## Troubleshooting

- Time zone setting is TIME_ZONE = 'America/Chicago'. If you are in a different time zone, you may have to change this in server/mysite/settings.py to your timezone

Here is a link to valid time zone settings:

https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568

This app was developed on a Windows 10 machine. I have checked many times to ensure that you dont experience issues on Linux. But there is always a chance you will encounter one of the following.

Even with the use of a linux subsystem to develop, there can be some issues when running on a linux machine.

- File formating - You may experience errors when running scripts related to \r or :. This is due to the files being formatted incorrectly. Use the following script at the ROOT of this project. DO NOT RUN OUTSIDE OF THIS PROJECT. REQUIRES dos2unix. Install through your package manager.
> find . -regextype egrep -iregex ".\*" -type f -not -path '\*/\_\_pycache\_\_/\*' -not -path '\*/bin/\*' -not -path '\*/obj/\*' -not -path '\*/.git/\*' -not -path '\*/.svn/\*' -not -path '\*/node\_modules/\*' -not -path '\*/.ionide/\*' -exec dos2unix "{}" \\;

- Script files not executable. The utility\_scripts may not have permissions to be run. Use the following script at the ROOT of this project. DO NOT RUN OUTSIDE OF THIS PROJECT.
> find . -regextype egrep -iregex ".\*\.sh" -type f -not -path '\*/\_\_pycache\_\_/\*' -not -path '\*/bin/\*' -not -path '\*/obj/\*' -not -path '\*/.git/\*' -not -path '\*/.svn/\*' -not -path '\*/node\_modules/\*' -not -path '\*/.ionide/\*' -exec chmod +777 "{}" \\;

## Linting

Makes use of autopep8

Run the following to lint the whole project (requires you have setup the virutal environment):

> ./utility\_scripts/lint.sh

