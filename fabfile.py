from fabric.api import local

exclude_command = '--exclude nlpre/spacy_models/'

def test():
    #local("flake8 nlpre --builtins basestring")
    local("nosetests --with-coverage --cover-package nlpre --cover-html")
    #local("aspell check README.md")
    #local("flake8 tests")
    #local("detox")

def lint():
    local("black nlpre tests %s"%exclude_command)
    local("flake8 nlpre --ignore=E501,E203 %s"%exclude_command)   

def cover():
    local("xdg-open cover/index.html")

def push():
    local("git pull")
    test()
    local("git commit -a")
    local("git push")

def clean():
    local('rm -rvf .coverage cover/ .tox *.egg-info/ docs/ dist/')
    for tag in ["*.pyc", "*~",]:
        local("find . -name '%s' | xargs -I {} rm -v {}"%(tag))

