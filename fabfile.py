"""Management utilities."""


from fabric.contrib.console import confirm
from fabric.api import abort, env, local, settings, task, sudo, cd, lcd, put, run, prefix
from fabric.contrib.files import exists


########## CONFIG

local_app_dir = '.'
local_config_dir = './config'

remote_app_home_dir = '/home/www'
remote_git_dir = '/home/git'
remote_app_dir = remote_app_home_dir + '/etapi'
remote_db_dir = '/var/apps/etapi/db'
remote_nginx_dir = '/etc/nginx/sites-enabled'
remote_supervisor_dir = '/etc/supervisor/conf.d'

env.user = 'pi'
env.hosts = ['192.168.0.120']
env.activate = "source %s/%s" % (remote_app_dir, "env/bin/activate")

########## END CONFIG


########## HELPERS

def add_remote():
    """
    Add production Git repository to remotes
    """
    with lcd(local_app_dir):
        local('git remote add production pi@192.168.0.120:/home/git/etapi.git')

def init_db():
    """
    Initialize the database
    """
    with cd(remote_app_dir):
        with prefix(env.activate):
            run('python manage.py db init')

def push_changes_to_production():
    with lcd(local_app_dir):
        local('git push production master')

def install_requirements():
    with cd(remote_app_dir):
        with prefix(env.activate):
            run('pip install -r requirements.txt')

def install_npm_packages():
    with cd(remote_app_dir):
        run('npm install')

def install_bower_packages():
    with cd(remote_app_dir):
        run('bower install')

def make_migrations():
    with cd(remote_app_dir):
        with prefix(env.activate):
            run('python manage.py db migrate')
            run('python manage.py db upgrade')

def run_app():
    """ Run the app! """
    with cd(remote_app_dir):
        sudo('supervisorctl start etapi')

def restart_app():
    with cd(remote_app_dir):
        sudo('supervisorctl restart etapi')

########## END HELPERS


########## BOOTSTRAP

PACKAGES = (
    'python',
    'python-dev',
    'python-pip',
    'python-virtualenv',
    'nginx',
    'gunicorn',
    'supervisor',
    'git',
    'nodejs',
    'npm',
)

def install_requirements():
    """ Install required packages. """
    packages = ' '.join(PACKAGES)
    sudo('apt-get update')
    sudo('apt-get install -y ' + packages)

def create_project_dir():
    """
    1. Create project directories
    2. Create and activate a virtualenv
    """
    if exists(remote_app_home_dir) is False:
        sudo('mkdir ' + remote_app_home_dir)
    if exists(remote_app_dir) is False:
        sudo('mkdir ' + remote_app_dir)
    if exists(remote_app_dir + '/logs') is False:
        sudo('mkdir ' + remote_app_dir + '/logs')
    if exists(remote_db_dir) is False:
        sudo('mkdir -p ' + remote_db_dir)
        sudo('chown pi:pi ' + remote_db_dir + ' -R')
    with cd(remote_app_dir):
        if exists(remote_app_dir + '/env') is False:
            sudo('virtualenv env')

    # Change permissions
    sudo('chown pi:pi ' + remote_app_home_dir + ' -R')

def configure_nginx():
    """
    1. Remove default nginx config file
    2. Create new config file
    3. Setup new symbolic link
    4. Copy local config to remote config
    5. Restart nginx
    """
    sudo('/etc/init.d/nginx start')
    if exists('/etc/nginx/sites-enabled/default'):
        sudo('rm /etc/nginx/sites-enabled/default')
    if exists('/etc/nginx/sites-enabled/etapi') is False:
        sudo('touch /etc/nginx/sites-available/etapi')
        sudo('ln -s /etc/nginx/sites-available/etapi' +
             ' /etc/nginx/sites-enabled/etapi')
    with lcd(local_config_dir):
        with cd(remote_nginx_dir):
            put('./etapi_nginx.conf', './etapi', use_sudo=True)
    sudo('/etc/init.d/nginx restart')

def configure_supervisor():
    """
    1. Create new supervisor config file
    2. Copy local config to remote config
    3. Register new command
    """
    if exists('/etc/supervisor/conf.d/etapi.conf') is False:
        with lcd(local_config_dir):
            with cd(remote_supervisor_dir):
                put('./etapi.conf', './', use_sudo=True)
                sudo('supervisorctl reread')
                sudo('supervisorctl update')

def configure_git():
    """
    1. Setup bare Git repo
    2. Create post-receive hook
    """
    if exists(remote_git_dir) is False:
        sudo('mkdir ' + remote_git_dir)

        with cd(remote_git_dir):
            sudo('mkdir etapi.git')
            with cd('etapi.git'):
                sudo('git init --bare')
                with lcd(local_config_dir):
                    with cd('hooks'):
                        put('./post-receive', './', use_sudo=True)
                        sudo('chmod +x post-receive')

            # Change permissions
            sudo('chown pi:pi ' + remote_git_dir + ' -R')

def bootstrap():
    #install_requirements()
    create_project_dir()
    configure_nginx()
    configure_supervisor()
    configure_git()
    push_changes_to_production()
    install_requirements()
    init_db()


########## END BOOSTRAP


########## DEPLOYMENT

def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    """
    1. Push changes to production
    2. Install dependencies
    3. Make migrations
    3. Restart gunicorn via supervisor
    """
    local("echo ------------------------")
    local("echo DEPLOYING APP TO PRODUCTION")

    local("echo Push changes to production")
    push_changes_to_production()

    # Install Python requirements
    local("echo Installing Python requirements")
    install_requirements()

    # Install NPM packages
    local('echo Installing NPM packages')
    install_npm_packages()

    # Install Bower packages
    local('echo Installing Bower packages')
    install_bower_packages()

    # Make migrations
    local('echo Make migrations')
    make_migrations()

    # Restart app
    local('echo Restarting application')
    restart_app()

    local("echo DONE DEPLOYING APP TO PRODUCTION")
    local("echo ------------------------")

########## END DEPLOYMENT


########## MANAGEMENT

def status():
    """ Is our app live? """
    sudo('supervisorctl status')

########## END MANAGEMENT
