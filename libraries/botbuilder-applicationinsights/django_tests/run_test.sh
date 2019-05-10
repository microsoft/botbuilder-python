#!/bin/bash

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# It is expected at this point that django and applicationinsights are both installed into a
# virtualenv.
django_version=$(python -c "import django ; print('.'.join(map(str, django.VERSION[0:2])))")
test $? -eq 0 || exit 1

# Create a new temporary work directory
TMPDIR=$(mktemp -d)
SRCDIR=$(pwd)
function cleanup
{
	cd $SRCDIR
	rm -rf $TMPDIR
	exit $1
}
trap cleanup EXIT SIGINT
cd $TMPDIR

# Set up Django project
django-admin startproject aitest
cd aitest
cp $SRCDIR/views.py aitest/views.py
cp $SRCDIR/tests.py aitest/tests.py
cp $SRCDIR/urls.py aitest/urls.py
cp $SRCDIR/template.html aitest/template.html

./manage.py test
exit $?