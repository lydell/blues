from fabric.decorators import task

from refabric.api import run, info
from refabric.context_managers import sudo
from refabric.contrib import blueprints

from . import debian


blueprint = blueprints.get(__name__)

start = debian.service_task('rabbitmq-server', 'start')
stop = debian.service_task('rabbitmq-server', 'stop')
restart = debian.service_task('rabbitmq-server', 'restart')
reload = debian.service_task('rabbitmq-server', 'reload')


@task
def setup():
    install()
    upgrade()


def install():
    package_name = 'rabbitmq-server'
    debian.debconf_set_selections('%s rabbitmq-server/upgrade_previous note' % package_name)

    with sudo():
        info('Adding apt key for {}', package_name)
        run("apt-key adv --keyserver pgp.mit.edu --recv-keys 0x056E8E56")

        info('Adding apt repository for {}', package_name)
        debian.add_apt_repository('http://www.rabbitmq.com/debian/ testing main')
        debian.apt_get('update')

        info('Installing {}', package_name)
        debian.apt_get('install', package_name)


@task
def upgrade():
    uploads = blueprint.upload('./', '/etc/rabbitmq/')
    if uploads:
        restart()
