from fabric.api import local

def test():
    local("flake8 nlpre --ignore=E501")
    local("nosetests")
    #local("flake8 tests")
    local("aspell check README.md")
    #local("detox")

def lint():
    local("autopep8 nlpre/*.py -aaa --in-place")
    #local("autopep8 tests/*.py --in-place")

def push():
    local("git pull")
    test()
    local("git commit -a")
    local("git push")
