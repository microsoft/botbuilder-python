@echo off

rd /s /q generated
call autorest README.md --python

rd /s /q ..\botbuilder-schema\botbuilder\schema
rd /s /q ..\botframework-connector\botframework\connector\operations
del ..\botframework-connector\botframework\connector\connector_client.py

move generated\botframework\connector\models ..\botbuilder-schema\botbuilder\schema
move generated\botframework\connector\operations ..\botframework-connector\botframework\connector\operations
move generated\botframework\connector\connector_client.py ..\botframework-connector\botframework\connector\connector_client.py