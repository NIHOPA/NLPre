import os

exclude_command = '--exclude nlpre/spacy_models/'

def test():
    os.system("nosetests --with-coverage --cover-package nlpre --cover-html")

def lint():
    os.system(f"black -l 80 nlpre tests {exclude_command}")
    os.system(f"flake8 nlpre --ignore=E501,E203,W503 {exclude_command}")

def view_cover():
    os.system("xdg-open cover/index.html")

def clean():
    os.system('rm -rvf .coverage cover/ .tox *.egg-info/ docs/ dist/')
    for tag in ["*.pyc", "*~",]:
        os.system(f"find . -name '%s' | xargs -I {tag} rm -v {tag}")

