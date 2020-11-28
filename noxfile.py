import nox

@nox.session(python=["3.6", "3.7", "3.8"])
def tests(session):
    session.install("-r", "requirements-dev.txt")
    session.run('coverage', 'run',  '-m', 'pytest')
    session.run('coverage', 'report',  '-m')

@nox.session(python=["3.6", "3.7", "3.8"])
def lint(session):
    session.install("-r", "requirements-dev.txt")
    session.run('black', 'vizno', 'tests', 'examples/api', 'examples/reports', '--check')
    session.run('isort', 'vizno', 'tests', 'examples/api', 'examples/reports', '--check-only')
    session.run('flake8', 'vizno', 'tests', 'examples/api', 'examples/reports')
    session.run('mypy', 'vizno', 'tests', 'examples/api', 'examples/reports')