from paver.easy import sh, task


@task
def reset_db():
    """
    Reset the Django db, keeping the admin user
    """
    sh("python manage.py sqlclear aggregator | python hypermap/manage.py dbshell")
    sh("python manage.py syncdb")
    sh("python manage.py loaddata hypermap/aggregator/fixtures/aggregator.json")

@task
def run_tests():
    """
    Executes the entire test suite.
    """
    sh('python manage.py test aggregator --settings=hypermap.settings.test --failfast')
    sh('python manage.py test dynasty --settings=hypermap.settings.test --failfast')
    sh('flake8 hypermap')

@task
def run_integration_tests():
    """
    Executes the entire test suite.
    """
    sh('python manage.py test tests.integration --settings=hypermap.settings.test --failfast')
