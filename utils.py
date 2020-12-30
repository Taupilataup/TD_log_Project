import argparse
import shutil
import subprocess
import sys

import src.bdd.bdd
from src.bdd.Project import ProjectManager


def run():
    # Run container
    bash_command = "docker-compose -f docker/docker-compose.yml up -d"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    process.communicate()

    bash_command = "alembic upgrade head"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    process.communicate()

    print("To visualize data please visit: http://localhost:8888")
    print("Username: tdlog")
    print("Password: tdlog")


def install():
    if sys.prefix == sys.base_prefix:
        ans = input("You are not in a virtual env, proceed anyway ? (y/n)")
        if ans != 'y':
            return

    docker = shutil.which('docker')
    docker_compose = shutil.which('docker-compose')

    if not docker or not docker_compose:
        print("Please install docker and docker-compose.")
        return

    # Install python requirements
    bash_command = "pip install -r requirements.txt"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    process.communicate()

    # Build docker container
    bash_command = "docker-compose -f docker/docker-compose.yml build"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    process.communicate()

def drop(project_name):
    """Drop Project from BDD."""
    ProjectManager().drop_project(project_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Install/Run BDD for development purpose.")
    parser.add_argument('action', choices=['install', 'run', 'drop'], help="What should I do ?")
    parser.add_argument('project_name', nargs=1, default=None)
    args = parser.parse_args()

    if args.action == 'run':
        run()
    elif args.action == 'install':
        install()
    elif args.action == 'drop':
        if args.project_name:
            drop(args.project_name)
        else:
            print("Usage: python utils.py drop PROJECT_NAME.")
