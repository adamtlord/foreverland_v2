import os

from datetime import datetime

from django.conf import settings

from fabric.api import local, run, cd, env, get
from fabric.contrib.console import confirm
from fabric.decorators import runs_once


DEFAULT_DB_SETTINGS = settings.DATABASES['default']
if not DEFAULT_DB_SETTINGS['PASSWORD']:
    MYSQL_USER_PASSWD = 'mysql -u%s' % DEFAULT_DB_SETTINGS['USER']
else:
    MYSQL_USER_PASSWD = 'mysql -u%s -p\'%s\'' % (DEFAULT_DB_SETTINGS['USER'], DEFAULT_DB_SETTINGS['PASSWORD'])
MYSQL_EXEC_CMD = '%s -e' % MYSQL_USER_PASSWD

env.use_ssh_config = getattr(settings, 'FABRIC_USE_SSH_CONFIG', False)


def get_remote_mysql_pass_arg():
    """Return password argument for mysql commands (if pw is set)"""
    if env.database['PASSWORD']:
        return '-p\'%s\'' % env.database['PASSWORD']
    else:
        return ''


def prod():
    """Sets up the prod environment for fab remote commands"""
    from foreverland.settings.prod import SSH_HOSTS, DATABASES as PROD_DATABASES
    env.user = 'adamlord'
    env.hosts = SSH_HOSTS
    env.database = PROD_DATABASES['default']
    env.remote_mysql_pw_arg = get_remote_mysql_pass_arg()
    env.PYTHON_DIR = '/usr/local/bin/python2.7'
    env.CODE_DIR = '/home/adamlord/webapps/foreverland_django/foreverland/'


def _launch(full=False):
    """Launch new code. Does a git pull, migrate and bounce"""
    DUMP_FILENAME = 'launchdump-%s.sql.gz' % datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    run('mysqldump --host=%s -u%s %s %s | gzip > /tmp/%s' % (
        env.database['HOST'], env.database['USER'], env.remote_mysql_pw_arg, env.database['NAME'], DUMP_FILENAME))

    with cd(env.CODE_DIR):
        run('git pull')
        if full:
            run('pip install -r requirements.pip')
            migrate()

        run('%s manage.py collectstatic --noinput' % env.PYTHON_DIR)
        run('find . -name \*.pyc -delete')

    bounce()


def quicklaunch():
    """Launch new code. Does a git pull, migrate and bounce"""
    _launch(full=False)


def launch():
    """Launch new code. Does a git pull, migrate and bounce"""
    _launch(full=True)


def ssh():
    """Launch console for given ssh host"""
    try:
        host = env.hosts
        user = env.user
    except IndexError:
        raise Exception("Wrong index provided")
    except ValueError:
        raise Exception("Argument must be integer")

    local('ssh %s@%s' % (user, host))


@runs_once
def migrate():
    """Does a syncdb, a dry run of migrate and a real migration if that suceeds."""
    with cd(env.CODE_DIR):
        run('%s manage.py migrate --noinput' % env.PYTHON_DIR)


def bounce():
    """Bounce apache + memcache"""
    with cd(env.CODE_DIR):
        run('%s manage.py compress' % env.PYTHON_DIR)
        run('../apache2/bin/restart')


def syncdb():
    """Gets a copy of the remote db and puts it into dev environment"""
    DUMP_FILENAME = 'dump-%s.sql.gz' % datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    DUMP_FILENAME_SQL = DUMP_FILENAME[:-3]

    if confirm('This may replace your db (you will get opportunity to specify which one). You sure?'):
        run('mysqldump --host=%s -u%s %s %s | gzip > /tmp/%s' % (
            env.database['HOST'], env.database['USER'], env.remote_mysql_pw_arg, env.database['NAME'],
            DUMP_FILENAME))
        get('/tmp/%s' % DUMP_FILENAME, os.path.basename(DUMP_FILENAME))  # download db
        local('gzip -d %s' % os.path.basename(DUMP_FILENAME))  # ungzip
        freshdb()
        local('%s %s < %s' % (MYSQL_USER_PASSWD, DEFAULT_DB_SETTINGS['NAME'], DUMP_FILENAME_SQL))
        local('rm %s' % DUMP_FILENAME_SQL)


####
# dev specific fab commands
####
def r():
    """
    Shortcut to do quick runserver
    """
    if 'gunicorn' in settings.INSTALLED_APPS:
        try:
            local('kill -TERM `cat gunicorn.pid`')
        except:
            print 'No existing gunicorn process'
        local('python manage.py run_gunicorn -w 4 --timeout=240 --pid=gunicorn.pid')
    else:
        local('python manage.py runserver')

runserver = r  # alias


def deletepycs():
    local('find . -name "*.pyc" -exec rm -rf {} \;')


def freshdb():
    if not settings.IS_DEV:
        raise Exception('This command is to only run on DEV')

    env.warn_only = True  # so fab doesnt drop out if the db doesnt exist yet.
    local('%s "%s"' % (MYSQL_EXEC_CMD, 'drop database %s' % DEFAULT_DB_SETTINGS['NAME']))
    env.warn_only = False
    local('%s "%s"' % (MYSQL_EXEC_CMD, 'create database %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci' % DEFAULT_DB_SETTINGS['NAME']))


@runs_once
def sync_uploads():
    """Reset local media from remote host"""
    local("rsync -rva adamlord@%s:webapps/foreverland_uploadsserve/ uploads" % (
        env.host_string))
