import os
from invoke import run, task

# EDIT with your own settings
AWS_PROFILE = 'myprofile'
AWS_REGION  = 'myawsregion'

# EDIT with your own settings
DEFAULT_SERVER_APP_NAME = 'mydomain'
DEFAULT_SERVER_ENV_NAME = 'mydomain-1'

PROFILE_OPT = '--profile {profile}'.format(profile=AWS_PROFILE)
REGION_OPT = '--region {region}'.format(region=AWS_REGION)

SERVER_AMI = '64bit Amazon Linux 2016.03 v2.1.0 running Python 3.4'

SERVER_INSTANCE_TYPE = 't2.micro'
# Use Elastic Beanstalk managed RDS database early during development
# But it is recommended to later switch to your own RDS outside EB, especially for production.
# This makes it easy to destroy the EB environment without destroying the database
# Note that you will need to set the env variables on .ebextensions/01_main.config
DB_CMD = '-db -db.i db.t2.micro -db.engine postgres -db.version 9.5 -db.user ebroot -db.pass pass.DB'


@task
def create(env=DEFAULT_SERVER_ENV_NAME, app=DEFAULT_SERVER_APP_NAME):
    os.chdir('server')
    run('eb init -p "{ami}" {region} {profile} {name}'.format(region=REGION_OPT,
                                                              ami=SERVER_AMI,
                                                              profile=PROFILE_OPT,
                                                              name=app))

    # basic = '--timeout 30 --instance_type t2.micro --service-role aws-elasticbeanstalk-service-role'
    basic = '--timeout 30 --instance_type {0}'.format(SERVER_INSTANCE_TYPE)
    run("eb create {basic} {db} {region} {profile} -c {cname} {name}".format(basic=basic,
                                                                             db=DB_CMD,
                                                                             region=REGION_OPT,
                                                                             profile=PROFILE_OPT,
                                                                             cname=env,
                                                                             name=env))

@task
def deploy(type='server'):
    if type == 'server':
        # Just for Server, we need to execute gulp first
        # Will deploy everything under /staticfiles. If new
        # third party packages are added, a local python manage.py collectstatic
        # will have to be run to move static files for that package to /staticfiles

        run('gulp deploy')
    os.chdir('server')
    run('eb deploy --region={region}'.format(region=AWS_REGION))


@task
def ssh(type='server'):
    os.chdir('server')
    run('eb ssh')

@task
def webapp_build():
    os.chdir('webapp')
    run('gulp templates')

@task
def initial_build():
    os.chdir('webapp')
    run('npm install')
    run('bower install')
    run('gulp templates')



