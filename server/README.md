# Body Comp

## Requirements
- python 3.8.x
- pip 20.x.x
- python3-venv
- bash --version GNU bash, version 5.x.xx

## Development tools
- vscode
- python extension for vscode - ms-python.python
- pylance extension for vscode - ms-python.vscode-pylance
- bash --version GNU bash, version 5.0.17(1)-release (x86_64-pc-linux-gnu)
- wsl1 ubuntu 20.04
- python 3.8.5
- pip 20.0.2

## Setup

### first time up front setup
> mkdir -p ~/.virtualenvs && python -m venv ~/.virtualenvs/body_comp_server

### launch virtual environment
> source ~/.virtualenvs/body_comp_server/bin/activate

### install dependencies
> pip install -e .

### run migrations for db (makes migrations and performs the migrations)
> ./utility_scripts/quick_migrations.sh

### run server
> ./utility_scripts/run_server.sh

### run tests
> ./utility_scripts/run_tests.sh

### viewing db migrations
> python manage.py sqlmigrate <app_name> <migration_name>


## Troubleshooting
This app was developed on a Windows 10 machine. I have checked many times to ensure that you dont experience issues on Linux. But there is always a change you will encounter one of the following.

Even with the use of a linux subsystem to develop, there can be some issues when running on a linux machine.

- File formating - You may expersion errors when running scripts related to \r or :. This is due to the files being formatted incorrectly. Use the following script at the ROOT of the project. DO NOT RUN OUTSIDE OF THIS PROJECT. REQUIRES dos2unix. Install through your package manager.
> find . -regextype egrep -iregex ".*" -type f -not -path '*/__pycache__/*' -not -path '*/bin/*' -not -path '*/obj/*' -not -path '*/.git/*' -not -path '*/.svn/*' -not -path '*/node_modules/*' -not -path '*/.ionide/*' -exec dos2unix "{}" \;

- Script files not executable. The utility_scripts may not have permissions to be run. Use the following script at the ROOT of the project. DO NOT RUN OUTSIDE OF THIS PROJECT.
> find . -regextype egrep -iregex ".*\.sh" -type f -not -path '*/__pycache__/*' -not -path '*/bin/*' -not -path '*/obj/*' -not -path '*/.git/*' -not -path '*/.svn/*' -not -path '*/node_modules/*' -not -path '*/.ionide/*' -exec chmod +777 "{}" \;

## Linting

Makes use of autopep8

Run the following to lint the whole project:

> ./utility_scripts/lint.sh

