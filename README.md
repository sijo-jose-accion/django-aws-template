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

- Ready Bootstrap-themed pages
- User Registration/Sign up with social login support (using django-allauth)
- Ready to provide rest api for all models (using djangorestframework)
- Gulp based flow to build CSS/JS files and release directly to s3/cloudfront
- Better Security with 12-Factor recommendations
- Logging/Debugging Helpers
- Works on Python 3.4+ (should work on 2.7+ but has not been actively tested)

### Quick start: ###

```
$ django-admin.py startproject --template=https://github.com/dkarchmer/django-aws-template/archive/master.zip --extension=py,md,html,env my_proj
$ cd my_proj
$ pip install -r requirements.txt
$ cd server
$ cp config/settings/local.sample.env config/settings/.local.env
$ python manage.py migrate
```
More information at: http://django-edge.readthedocs.org/

*Rest of this README will be copied to the generated project.*

{% endcomment %}

# {{ project_name }} #

Project is built with Python using the Django Web Framework.
It is based on the django-aws-template (https://github.com/dkarchmer/django-aws-template)

This project has the following basic apps:

App1 (short desc)
App2 (short desc)
App3 (short desc)
Installation

Quick start

To set up a development environment quickly, first install Python 3. It comes with virtualenv built-in. So create a virtual env by:

1. `$ python3 -m venv {{ project_name }}`
2. `$ . {{ project_name }}/bin/activate`
Install all dependencies:

pip install -r requirements.txt
Run migrations:

python manage.py migrate
Detailed instructions

Take a look at the docs for more information.