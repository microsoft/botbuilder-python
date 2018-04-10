@echo off

rd /s /q generated
echo [91mWARNING:[0m There is manual code for lines 127-130 in attachments_operations_async.py and lines 12-26 in the connector_client.py.
echo [91mCalling this command script has removed those sections of code.[0m
call autorest README.md --python --use="git+https://github.com/Azure/autorest.python#async"

rd /s /q ..\botbuilder-schema\botbuilder\schema
rd /s /q ..\botframework-connector\botframework\connector\operations
del ..\botframework-connector\botframework\connector\connector_client.py

move generated\botframework\connector\models ..\botbuilder-schema\botbuilder\schema
move generated\botframework\connector\operations ..\botframework-connector\botframework\connector\operations
move generated\botframework\connector\connector_client.py ..\botframework-connector\botframework\connector\connector_client.py