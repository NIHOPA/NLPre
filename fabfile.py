from fabric.api import local

exclude_command = "--exclude nlpre/spacy_models/"


def test():
    local("nosetests --with-coverage --cover-package nlpre --cover-html")


def lint():
    local(f"black -l 80 nlpre tests *.py {exclude_command}")
    local(f"flake8 nlpre --ignore=E501,E203,W503 {exclude_command}")


def view_cover():
    local("xdg-open cover/index.html")


def clean():
    local("rm -rvf .coverage cover/ .tox *.egg-info/ docs/ dist/")
    for tag in ["*.pyc", "*~"]:
        local(f"find . -name '%s' | xargs -I {tag} rm -v {tag}")
