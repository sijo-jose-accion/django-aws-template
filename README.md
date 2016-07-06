{% comment "This comment section will be deleted in the generated project" %}

## django-aws-template ##

### Build Status ###

An opinionated Django project starter intended for people that will release to AWS. It assumes

1. main django server will be released to AWS Elastic Beanstalk,
2. static files will be released to s3/cloudfront using a gulp based flow (not django collectstatics)
3. Use docker for development/testing
4. Use a common set of django packages for the basics. In particular, django-allauth for social authentication
and djangorestframework for a rest API.

### Features ###

- Ready Bootstrap-themed, gulp based web pages
- User Registration/Sign up with social login support (using django-allauth)
- Ready to provide rest api for all models (using djangorestframework)
- Gulp based flow to build CSS/JS files and release directly to s3/cloudfront (based on `yo webapp`)
- Better Security with 12-Factor recommendations
- Logging/Debugging Helpers
- Works on Python 3.4+ (should work on 2.7+ but has not been actively tested)

### Quick start: ###

```
$ python3 -m venv .virtualenv/my_proj
$ . .virtualenv/my_proj/bin/activate
$ pip install django
$ django-admin.py startproject --template=https://github.com/dkarchmer/django-aws-template/archive/master.zip --extension=py,md,html,env,json,config my_proj
```

The do the following manual work:

* Create a .ebextensions directory with decired Elastic Beanstalk options. See https://github.com/dkarchmer/django-aws-template/tree/master/server/.ebextensions

* Search and replace `mydomain` with your own domain
* Search and replace `mystaticbucket` with your own S3 Bucket Name
* Search and replace `myawsregion` with your own AWS_REGION
* Search and replace `myawsprofile` with your own profile. Use `default` if you created the default one from `aws configure`
* Search and replace `mycloudfrontdistributionid` with your CloudFront Distribution ID
* Search  `need-value` and add the appropriate value based on your setup

*Rest of this README will be copied to the generated project.*

{% endcomment %}

# {{ project_name }} #

Project is built with Python using the Django Web Framework.
It is based on the django-aws-template (https://github.com/dkarchmer/django-aws-template)

This project has the following basic features:

* Custom Authentication Model with django-allauth
* Rest API

## Installation

### Assumptions

You must have the following installed on your computer

* Python 3.4 or greater
* Docker
* nodeJS v4 or v5
* bower

For MacOS, see https://gist.github.com/dkarchmer/d8124f3ae1aa498eea8f0d658be214a5

### Python Environment ###

To set up a development environment quickly, first install Python 3. It comes with virtualenv built-in. So create a virtual env by:

```
$ python3 -m venv  ~/.virtualenv/iotile
$ .  ~/.virtualenv/iotile/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt
$ pip install -r server/requirements.txt
$ cp server/config/settings/sample-local.env server/config/settings/.local.env
$ cp server/config/settings/sample-docker.env server/config/settings/.docker.env
$ cp server/config/settings/sample-production.env server/config/settings/.production.env
```

### Static Files

We use nodeJS with Gulp and Bower to process static files:

```
$ cd webapp
$ bower install
$ npm install
$ gulp
```

But we also need all static files for third party Django libraries

```
cd ../server
$ python manage.py collecstatic
```

### Database ###

To create database (SQLite3 for development), run

```
$ cd ../server
$ python manage.py migrate
$ python manage.py init-basic-data
```

`init-basic-data` will create a super user with username=admin, email=env(INITIAL_ADMIN_EMAIL) and password=admin.
Make sure you change the password right away.
It also creates django-allauth SocialApp records for Facebook, Google and Twitter (to avoid later errors). You will have to modify these records (from admin pages) with your own secret keys, or remove these social networks from the settings.



### Testing

```
$ cd ../server
$ python manage.py test
```

### Using Docker

I am not documenting how to install the template with docker, so you will need a local copy of python and django to install the template, but once installed (i.e., the project is on your file system), you can use docker for everything else

Docker can be used to avoid having to install nodejs and python specific packages.

To build the webapp static file (this part is not fully tested)

```
docker build -t my_proj/builder webapp
docker run --rm -v ${PWD}/webapp:/usr/src/app --entrypoint npm -t my_proj/builder install
docker run --rm -v ${PWD}/webapp:/usr/src/app --entrypoint bower -t my_proj/builder --allow-root --config.interactive=false install
docker run --rm -v ${PWD}:/usr/src/app -t my_proj/builder templates
```

After the webapp static files have been build, Docker Compose can be used to run the whole server, including a proper
Postgres database. Note this is not intended for Production. For production, AWS Elastic Beanstalk should be used.

```
docker-compose -f docker-compose.utest.yml up     # To run a test within a Docker container
docker-compose -f docker-compose.yml up           # To run Docker based server and databases
```

## Elastic Beanstack Deployment

Review all files under `server/.ebextensions`, and modify if needed. Note that many settings are
commented out as they require your own AWS settings.

For early development, the `create` command will ask *Elastic Beanstalk (EB)* to create and manage its own
RDS Postgres database. This also means that when the *EB* environment is terminated, the database will be
terminated as well.

Once the models are more stable, and for sure for production, it is recommended that you create your own
RDS database (outside *EB*), and simply tell Django to use that. The `.ebextensions/01_main.config` has
a bunch of `RDS_` environment variables (commented out) to use for this. Simply enable them, and set the
proper RDS address.

### Creating the environment

Make sure you have search for all instances of `mydomain` in the code and replace with the proper settings.
Also make sure you have created your own `server/config/settings/.production.env` based on the
`sample-production.env` file.

Look for the `EDIT` comments in `tasks.py` and `gulpfile.js` and edit as needed.

After your have done all the required editing, the `create` Invoke command will run *Gulp* to deploy all static files,
and then do the `eb init` and `eb create`:

```
invoke create
```

### Deployment (development cycle)

After your have created the environment, you can deploy code changes with the following command (which will run *Gulp*
and `eb deploy`:

```
invoke deploy
```
