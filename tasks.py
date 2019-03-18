from invoke import task

exclude_command = '--exclude nlpre/spacy_models/'

@task
def test(c):
    c.run("nosetests --with-coverage --cover-package nlpre --cover-html")

@task
def lint(c):
    c.run(f"black -l 80 nlpre tests {exclude_command}")
    c.run(f"flake8 nlpre --ignore=E501,E203,W503 {exclude_command}")

@task
def view_cover(c):
    c.run("xdg-open cover/index.html")

@task
def clean(c):
    c.run('rm -rvf .coverage cover/ .tox *.egg-info/ docs/ dist/')
    for tag in ["*.pyc", "*~",]:
        c.run(f"find . -name '%s' | xargs -I {tag} rm -v {tag}")

