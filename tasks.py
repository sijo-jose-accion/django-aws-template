import os
from invoke import run, task

AWS_PROFILE = 'myprofile'
AWS_REGION  = 'us-east-1'

DEFAULT_SERVER_APP_NAME = 'mydomain'
DEFAULT_SERVER_ENV_NAME = 'mydomain-1'

PROFILE_OPT = '--profile {profile}'.format(profile=AWS_PROFILE)
REGION_OPT = '--region {region}'.format(region=AWS_REGION)

SERVER_AMI = '64bit Amazon Linux 2015.09 v2.0.8 running Python 3.4'

SERVER_INSTANCE_TYPE = 't2.micro'


@task
def create(env=DEFAULT_SERVER_ENV_NAME, app=DEFAULT_SERVER_APP_NAME):
    os.chdir('server')
    run('eb init -p "{ami}" {region} {profile} {name}'.format(region=REGION_OPT,
                                                              ami=SERVER_AMI,
                                                              profile=PROFILE_OPT,
                                                              name=app))

    # basic = '--timeout 30 --instance_type t2.micro --service-role aws-elasticbeanstalk-service-role'
    basic = '--timeout 30 --instance_type {0}'.format(SERVER_INSTANCE_TYPE)
    run("eb create {basic} {region} {profile} -c {cname} {name}".format(basic=basic,
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

        run('gulp')
    os.chdir('server')
    run('eb deploy --region={region}'.format(region=AWS_REGION))


@task
def ssh(type='server'):
    os.chdir('server')
    run('eb ssh')

@task
def local_build():
    run('gulp build_local_all')



