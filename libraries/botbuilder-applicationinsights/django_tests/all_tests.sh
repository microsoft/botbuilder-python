#!/bin/bash
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

if [ -z $PYTHON ]; then
	PYTHON=$(which python)
fi

cd $(dirname $0)
BASEDIR=$(pwd)

# Django/python compatibility matrix...
if $PYTHON -c "import sys; sys.exit(1 if (sys.version_info.major == 3 and sys.version_info.minor == 6) else 0)"; then
    echo "[Error] Environment should be configured with Python 3.7!" 1>&2
	exit 2
fi
# Add more versions here (space delimited).
DJANGO_VERSIONS='2.2' 

# For each Django version...
for v in $DJANGO_VERSIONS
do
	echo ""
	echo "***"
	echo "*** Running tests for Django $v"
	echo "***"
	echo ""

	# Create new directory
	TMPDIR=$(mktemp -d)
	function cleanup
	{
		rm -rf $TMPDIR
		exit $1
	}

	trap cleanup EXIT SIGINT

	# Create virtual environment
    $PYTHON -m venv $TMPDIR/env

	# Install Django version + application insights
	. $TMPDIR/env/bin/activate
	pip install Django==$v || exit $?
	cd $BASEDIR/..
	pip install . || exit $?

	# Run tests
	cd $BASEDIR
	bash ./run_test.sh || exit $?

	# Deactivate 
	# (Windows may complain since doesn't add deactivate to path properly)
	deactivate 

	# Remove venv 
	rm -rf $TMPDIR
done