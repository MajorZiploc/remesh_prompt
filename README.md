# Remesh Prompt

## Overview
This is a django project that aims to recreate a simple version of remesh.

This is for interview purposes at remesh.ai.

## Requirements
- python 3.8.x
- pip 20.x.x
- python3-venv
- bash --version GNU bash, version 5.x.xx

## Development tools
- vscode
- python extension for vscode - ms-python.python
- pylance extension for vscode - ms-python.vscode-pylance
- bash --version GNU bash, version 5.0.17(1)-release (x86\_64-pc-linux-gnu)
- wsl1 ubuntu 20.04
- python 3.8.5
- pip 20.0.2

## Setup the server

### Go into the server folder. All server commands assume you are in that directory.

> cd ./server


NOTE: all \*.sh files will work regardless of what directory you call them from

### first time up front setup
> mkdir -p ~/.virtualenvs && python -m venv ~/.virtualenvs/body\_comp\_server

### launch virtual environment
> source ~/.virtualenvs/body\_comp\_server/bin/activate

### install dependencies
> pip install -e .

### run migrations for db (makes migrations and performs the migrations)
> ./utility\_scripts/quick\_migrations.sh

### run server
> ./utility\_scripts/run\_server.sh

### run tests
> ./utility\_scripts/run\_tests.sh

### viewing db migrations
> python manage.py sqlmigrate <app\_name> <migration\_name>


## Troubleshooting
This app was developed on a Windows 10 machine. I have checked many times to ensure that you dont experience issues on Linux. But there is always a change you will encounter one of the following.

Even with the use of a linux subsystem to develop, there can be some issues when running on a linux machine.

- File formating - You may experience errors when running scripts related to \r or :. This is due to the files being formatted incorrectly. Use the following script at the ROOT of the project. DO NOT RUN OUTSIDE OF THIS PROJECT. REQUIRES dos2unix. Install through your package manager.
> find . -regextype egrep -iregex ".\*" -type f -not -path '\*/\_\_pycache\_\_/\*' -not -path '\*/bin/\*' -not -path '\*/obj/\*' -not -path '\*/.git/\*' -not -path '\*/.svn/\*' -not -path '\*/node\_modules/\*' -not -path '\*/.ionide/\*' -exec dos2unix "{}" \;

- Script files not executable. The utility\_scripts may not have permissions to be run. Use the following script at the ROOT of the project. DO NOT RUN OUTSIDE OF THIS PROJECT.
> find . -regextype egrep -iregex ".\*\.sh" -type f -not -path '\*/\_\_pycache\_\_/\*' -not -path '\*/bin/\*' -not -path '\*/obj/\*' -not -path '\*/.git/\*' -not -path '\*/.svn/\*' -not -path '\*/node\_modules/\*' -not -path '\*/.ionide/\*' -exec chmod +777 "{}" \;

## Linting

Makes use of autopep8

Run the following to lint the whole project:

> ./utility\_scripts/lint.sh

