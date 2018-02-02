@echo off

rd /s /q generated
call autorest README.md --python

rd /s /q ..\botbuilder-schema\microsoft\botbuilder\schema
rd /s /q ..\botframework-connector\microsoft\botframework\connector\operations
del ..\botframework-connector\microsoft\botframework\connector\connector_client.py

move generated\botframework\connector\models ..\botbuilder-schema\microsoft\botbuilder\schema
move generated\botframework\connector\operations ..\botframework-connector\microsoft\botframework\connector\operations
move generated\botframework\connector\connector_client.py ..\botframework-connector\microsoft\botframework\connector\connector_client.py