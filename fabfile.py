import os
from datetime import datetime

from settings import PROJECT_NAME, PROJECT_ROOT as DEV_PROJECT_ROOT
from django.conf import settings

from fabric.api import local, run, cd, env, sudo, get
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


def staging():
    """Sets up the staging environment for fab remote commands"""
    from settings.staging import SSH_HOSTS, DATABASES as STAGING_DATABASES
    env.user = 'baseproject'
    env.hosts = SSH_HOSTS
    env.database = STAGING_DATABASES['default']
    env.remote_mysql_pw_arg = get_remote_mysql_pass_arg()

    env.CODE_DIR = '/home/baseproject/webapps/%s/src/%s/' % (PROJECT_NAME, PROJECT_NAME)


def prod():
    """Sets up the prod environment for fab remote commands"""
    from settings.prod import SSH_HOSTS, DATABASES as PROD_DATABASES
    env.user = 'adamlord'
    env.hosts = SSH_HOSTS
    env.database = PROD_DATABASES['default']
    env.remote_mysql_pw_arg = get_remote_mysql_pass_arg()

    env.CODE_DIR = '/home/adamlord/webapps/foreverland_python/src/foreverland/'


def _launch(full=False):
    """Launch new code. Does a git pull, migrate and bounce"""
    DUMP_FILENAME = 'launchdump-%s.sql.gz' % datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    run('mysqldump --host=%s -u%s %s %s | gzip > /tmp/%s' % (
        env.database['HOST'], env.database['USER'], env.remote_mysql_pw_arg, env.database['NAME'], DUMP_FILENAME))

    with cd(env.CODE_DIR):
        run('git pull')
        if full:
            _run_in_ve('pip install -r requirements.pip')
            migrate()
        _run_in_ve('python manage.py collectstatic --noinput -i *.less')
        _run_in_ve('find . -name \*.pyc -delete')

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
    except IndexError:
        raise Exception("Wrong index provided")
    except ValueError:
        raise Exception("Argument must be integer")

    local('ssh adamlord@%s' % host)


@runs_once
def migrate():
    """Does a syncdb, a dry run of migrate and a real migration if that suceeds."""
    with cd(env.CODE_DIR):
        _run_in_ve('python manage.py syncdb --noinput; python manage.py migrate --db-dry-run --noinput; python manage.py migrate --noinput')


def bounce():
    """Bounce apache + memcache"""
    # _run_in_ve('python manage.py compress')

    # APACHE CONFIG
    with cd(env.CODE_DIR):
        '../../apache2/bin/restart'

    # NGINX CONFIG
    #sudo('service uwsgi stop', pty=False)
    #sudo('service uwsgi start', pty=False)
    #sudo('/etc/init.d/nginx restart', pty=False)
    #sudo('/etc/init.d/nginx start', pty=False)

    # sudo('/etc/init.d/memcached restart', pty=False)

# rsync -rva adamlord@adamlord.webfactional.com:/home/adamlord/webapps/foreverland_python/src/foreverland/uploads/ /Users/adamlord/work/foreverland/src/foreverland/uploads

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


def slurpdb():
    """Gets a copy of the remote db and puts it into dev environment"""
    DUMP_FILENAME = 'dump-2015-01-24-11-15-41.sql'

    if confirm('This may replace your db (you will get opportunity to specify which one). You sure?'):
    #     run('mysqldump --host=%s -u%s %s %s | gzip > /tmp/%s' % (
    #         env.database['HOST'], env.database['USER'], env.remote_mysql_pw_arg, env.database['NAME'],
    #         DUMP_FILENAME))
    #     get('/tmp/%s' % DUMP_FILENAME, os.path.basename(DUMP_FILENAME))  # download db
    #     local('gzip -d %s' % os.path.basename(DUMP_FILENAME))  # ungzip
        freshdb()
        local('%s %s < %s' % (MYSQL_USER_PASSWD, DEFAULT_DB_SETTINGS['NAME'], DUMP_FILENAME))
        # local('rm %s' % DUMP_FILENAME_SQL)


@runs_once
def resetdb():
    if confirm("This will blow up server database. You sure?"):
        DUMP_FILENAME = 'launchdump-%s.sql.gz' % datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        run('mysqldump --host=%s -u%s %s %s | gzip > /tmp/%s' % (
            env.database['HOST'], env.database['USER'],
            env.remote_mysql_pw_arg, env.database['NAME'], DUMP_FILENAME))

        env.warn_only = True  # so fab doesnt drop out if the db doesnt exist yet.
        run('mysql --host=%s -u%s %s -e \'%s\'' % (
            env.database['HOST'], env.database['USER'], env.remote_mysql_pw_arg,
            'drop database %s' % env.database['NAME']))
        env.warn_only = False
        run('mysql --host=%s -u%s %s -e \'%s\'' % (
            env.database['HOST'], env.database['USER'], env.remote_mysql_pw_arg,
            'create database %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci' %
            env.database['NAME']))


def sphinxlocal():
    """Generates sphinx html locally"""
    local('cd docs; rm -rf build; make html')


def sphinx():
    """Generates sphinx html in env.CODE_DIR"""
    _run_in_ve('cd docs; rm -rf build; make html')


def _run_in_ve(command):
    run('cd ~/webapps/foreverland_python; source bin/activate; cd src/foreverland')


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
    local('%s "%s"' % (MYSQL_EXEC_CMD, 'create database %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci' %
        DEFAULT_DB_SETTINGS['NAME']))


def update(syncdb=True, syncdb_all=False):
    if not settings.IS_DEV:
        raise Exception('This command is to only run on DEV')

    with cd(DEV_PROJECT_ROOT):
        local('git pull')
        _local_in_ve('pip install -r requirements.pip')
        if syncdb:
            _local_in_ve('python manage.py syncdb --noinput %s' % '--all' if syncdb_all else '')
            if syncdb_all:
                _local_in_ve('python manage.py migrate --fake')  # fake all apps
            else:
                _local_in_ve('python manage.py migrate --db-dry-run --noinput')
                _local_in_ve('python manage.py migrate --noinput')


def bootstrap():
    """Bootstraps a dev box. Drops/creates db, installs requirements, does syncdb/migrate etc. Should also obfuscate
    real user emails (using django-extensions command) and also change site string in db to localhost?"""
    if confirm('This will blow up your env setup. You sure?'):
        with cd(DEV_PROJECT_ROOT):
            local('git pull')
        freshdb()
        update(syncdb_all=True)


def graphmodels():
    """Do 'pip install pygraphviz'. It'll give an error. Go into the source (in the $VIRTUAL_ENV/build/pygraphviz/setup.py
    file) and comment out and replace with these 2 lines:

    #library_path=None
    #include_path=None
    library_path='/usr/local/lib/graphviz'
    include_path='/usr/local/include/graphviz'

    This assumes you have graphviz installed (via macports or brew) of course.

    Do a 'pip install pygraphviz' again.
    """
    _local_in_ve('python manage.py graph_models -a -g -o graphed_models.png')


def _local_in_ve(command):
    kwargs = dict(capture=False)
    if hasattr(settings, 'FABRIC_LOCAL_SHELL'):
        # Points to a shell script containing custom shell execution, e.g.
        # if your default shell is ZSH you could want to use Bash with Fabric:
        # create '/bin/fabric_shell' script containing '/bin/bash -l "$@"',
        # and set: FABRIC_LOCAL_SHELL = '/bin/fabric_shell' in your local.py
        kwargs['shell'] = settings.FABRIC_LOCAL_SHELL
    local('workon %s; cd %s; %s' % (PROJECT_NAME, DEV_PROJECT_ROOT, command),
        **kwargs)


@runs_once
def sync():
    syncdb()
    sync_uploads()


@runs_once
def sync_uploads():
    host = env.hosts
    """Reset local media from remote host"""
    local("rsync -rva adamlord@%s:webapps/foreverland_python/src/foreverland/uploads/ uploads" % (
        env.host_string))


def dbtunnel(id=0):
    """
    Launch tunnel for given ssh host
    """

    try:
        remote_host = env.hosts[int(id)]
    except IndexError:
        raise Exception("Wrong index provided")
    except ValueError:
        raise Exception("Argument must be integer")

    if not 'PORT' in env.database:
        if env.database['ENGINE'] == 'django.db.backends.mysql':
            remote_port = 3306
        elif env.database['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
            remote_port = 5432
        else:
            raise Exception("Set database port")
    else:
        remote_port = env.database['PORT']

    local_port = remote_port + 1
    local('ssh -L %s:127.0.0.1:%s %s@%s -N' % (local_port, remote_port, env.user, remote_host))
