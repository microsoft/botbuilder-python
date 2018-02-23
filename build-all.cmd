cd .\libraries\botbuilder-schema\
python .\setup.py bdist_wheel
pip install .\dist\microsoft_botbuilder_schema-4-py2.py3-none-any.whl
cd ..\botframework-connector\
python .\setup.py bdist_wheel
pip install .\dist\microsoft_botframework_connector-3-py2.py3-none-any.whl
cd ..\botbuilder\
python .\setup.py bdist_wheel
pip install .\dist\microsoft_botbuilder-4.0.0a0-py3-none-any.whl
