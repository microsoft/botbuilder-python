# DJANGO-specific tests
Django generates *code* to create projects (`django-admin startproject`) and apps.  For testing, we test the generated code.  The tests are bare-bones to be compatible across different versions of django.

- This project contains a script to execute tests against currently supported version(s) of python and django.
- Assume latest version of Application Insights.
- Relies on virtualenv to run all tests.
- Uses django commands to generate new project and execute django tests.
- To run, first `cd django_tests` and then `bash .\all_tests.sh` (ie, in Powershell) to run all permutations.

File | | Description
--- | ---
all_tests.sh | Runs our current test matrix of python/django versions.  Current matrix is python (3.7) and django (2.2). 
README.md | This file.
run_test.sh | Runs specific python/django version to create project, copy replacement files and runs tests.
template.html | Template file
tests.py | Django tests.
urls.py | url paths called by tests
views.py | paths that are called





