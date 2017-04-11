from fabric.api import local

def test():
    local("flake8 nlpre")
    local("nosetests --with-coverage --cover-package nlpre --cover-html")
    local("aspell check README.md")
    #local("flake8 tests")
    #local("detox")

def lint():
    local("autopep8 nlpre/*.py -aaa --in-place")
    #local("autopep8 tests/*.py --in-place")

def cover():
    local("xdg-open cover/index.html")

def push():
    local("git pull")
    test()
    local("git commit -a")
    local("git push")

def clean():
    local('rm -rvf .coverage cover/ .tox *.egg-info/')
    for tag in ["*.pyc", "*~",]:
        local("find . -name '%s' | xargs -I {} rm -v {}"%(tag))

