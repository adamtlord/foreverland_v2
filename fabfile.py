from fabric.api import local

DOCKER_EXEC = "docker-compose exec web"
PY3_CMD = "%s python3" % DOCKER_EXEC


def ssh(service="web"):
    """
    ssh into running service container
    :param service: ['web', 'db']
    """
    assert service in ["web", "db"], "%s is unrecognized service" % service
    local("docker-compose exec %s bash" % service)


def up_recreate():
    """
    Recreate containers even if their configuration and image haven't changed.
    """
    local("docker-compose down && docker-compose up")


def up(quick=True):
    """
    Create and start containers.
    """
    if not quick:
        command = "docker-compose up --force-recreate --build"
    else:
        command = "docker-compose up"

    local(command)


def down():
    """
    Stop all containers.
    """
    local("docker-compose down")


def stop():
    """
    Stop services.
    """
    local("docker-compose stop")


# def stopdb():
#     """
#     Kill existing db connections
#     """
#     local(
#         """docker-compose exec db psql -U toiyabe -c
#         \"select pg_terminate_web(pid) from pg_stat_activity where datname = 'toiyabe';\"
#         """
#     )


# def freshdb():
#     """
#     Drop/Create new db (local dev only)
#     """
#     local("docker exec -it toiyabe_title_db_1 dropdb -U toiyabe toiyabe")
#     local("docker exec -it toiyabe_title_db_1 createdb -U toiyabe toiyabe")


def managepy(command=""):
    """manage.py command"""
    cmd = "{0} manage.py {1}".format(PY3_CMD, command)
    local(cmd)
