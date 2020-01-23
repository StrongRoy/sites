from fabric.contrib.files import exists,sed,append
from fabric.api import cd, env, local, run
import random

REPO_URL = 'https://github.com/StrongRoy/sites.git'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder +'/source'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()

    with cd(source_folder):
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')

def _update_settings():
    settings_path = 'source/superlists/settings.py'
    sed(settings_path,"DEBUG = True","DEBUG = False")
    sed(settings_path,
    'ALLOWED_HOSTS = .+$',f'ALLOWED_HOSTS = ["{env.host}"]'
    )
    secret_key_file =  'source/superlist/secret_key.py'
    if not exists(secret_key_file):
        chars = ''
        key = ''.join(random.SystemRandom.choice(chars) for _ in range(50))
        append(secret_key_file,f'SECRET_KEY = "{key}"')
    append(settings_path,'\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python3.6 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r ./source/requirements.txt')


def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')