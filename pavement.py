import os
from paver.easy import call_task, info, sh, task


@task
def reset_db():
    """
    Reset the Django db, keeping the admin user
    """
    sh("python hypermap/manage.py sqlclear aggregator | python hypermap/manage.py dbshell")
    sh("python hypermap/manage.py syncdb")
    sh("python hypermap/manage.py loaddata hypermap/aggregator/fixtures/aggregator.json")


@task
def run_tests():
    """
    Executes the entire test suite.
    """
    sh('python hypermap/manage.py test aggregator --settings=settings.test --failfast')
    sh('python hypermap/manage.py test dynasty --settings=settings.test --failfast')
    sh('flake8 hypermap')


@task
def run_integration_tests():
    """
    Executes the entire test suite.
    """
    call_task('start_server')
    sh('python hypermap/manage.py test tests.integration --settings=settings.test --failfast')
    call_task('stop_server')


@task
def start_server():
    sh('python hypermap/manage.py runserver 0.0.0.0:8000 &')


@task
def stop_server():
    kill_process('python', 'hypermap/manage.py')


def kill_process(procname, scriptname):
    """kill WSGI processes that may be running in development"""

    # from http://stackoverflow.com/a/2940878
    import signal
    import subprocess

    p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    for line in out.decode().splitlines():
        if procname in line and scriptname in line:
            pid = int(line.split()[1])
            info('Stopping %s %s %d' % (procname, scriptname, pid))
            os.kill(pid, signal.SIGKILL)
