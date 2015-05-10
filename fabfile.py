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
env.hosts = ['etapi.duckdns.org']
env.activate = "source %s/%s" % (remote_app_dir, "env/bin/activate")

########## END CONFIG


########## HELPERS

def package_installed(pkg_name):
    """ref: http:superuser.com/questions/427318/#comment490784_427339"""
    cmd_f = 'dpkg-query -l "%s" | grep -q ^.i'
    cmd = cmd_f % (pkg_name)
    with settings(warn_only=True):
        result = sudo(cmd)
    return result.succeeded

def yes_install(pkg_name):
    """ref: http://stackoverflow.com/a/10439058/1093087"""
    sudo('apt-get --force-yes --yes install %s' % (pkg_name))

def install_node():
    if exists("/opt/node") is False:
        sudo("mkdir -p /opt/node")
        with cd('/tmp'):
            sudo("wget https://s3-eu-west-1.amazonaws.com/conoroneill.net/wp-content/uploads/2015/02/node-v0.12.0-linux-arm-pi.tar.gz")
            sudo("tar xzf node-v0.12.0-linux-arm-pi.tar.gz")
            sudo("cp -r node-v0.12.0-linux-arm-pi/* /opt/node")
            sudo("rm -rf node-v0.12.0-linux-arm-pi*")
            if exists("/usr/local/bin/node"):
                sudo("rm /usr/local/bin/node")
            if exists("/usr/local/bin/npm"):
                sudo("rm /usr/local/bin/npm")
            sudo("ln -s /opt/node/bin/node /usr/local/bin/node")
            sudo("ln -s /opt/node/bin/npm /usr/local/bin/npm")

def add_remote():
    """
    Add production Git repository to remotes
    """
    with lcd(local_app_dir):
        local('git remote add production pi@192.168.0.120:/home/git/etapi.git')

def create_db():
    """
    Initialize the database.
    """
    with cd(remote_app_dir):
        with prefix(env.activate):
            if exists(remote_db_dir + "/etapi.db") is False:
                run('ETAPI_ENV=prod python manage.py createdb')

def drop_db():
    """
    Drops the database.
    """
    with cd(remote_app_dir):
        with prefix(env.activate):
            run('ETAPI_ENV=prod python manage.py dropdb')

def push_changes_to_production():
    with lcd(local_app_dir):
        local('git push production master')

def install_pip_requirements():
    with cd(remote_app_dir):
        with prefix(env.activate):
            run('pip install -r requirements.txt')

def install_npm_packages():
    with cd(remote_app_dir):
        run('npm install')

def install_bower_packages():
    with cd(remote_app_dir):
        run('./node_modules/.bin/bower install')

def make_migrations():
    with cd(remote_app_dir):
        with prefix(env.activate):
            run('ETAPI_ENV=prod python manage.py db upgrade')

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
)

def install_requirements():
    """ Install required packages. """
    sudo('apt-get update')
    for package in PACKAGES:
        if not package_installed(package):
            yes_install(package)

def create_project_dir():
    """
    1. Create required project directories and files
    2. Create a virtualenv
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
    install_node()
    create_project_dir()
    configure_nginx()
    configure_supervisor()
    configure_git()
    push_changes_to_production()
    install_pip_requirements()
    create_db()


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
    install_pip_requirements()

    # Install NPM packages
    local('echo Installing NPM packages')
    #install_npm_packages()

    # Install Bower packages
    local('echo Installing Bower packages')
    #install_bower_packages()

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
