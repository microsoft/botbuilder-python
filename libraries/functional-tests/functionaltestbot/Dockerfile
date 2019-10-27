# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

FROM    tiangolo/uwsgi-nginx-flask:python3.6

# Setup for nginx
RUN  mkdir -p /home/LogFiles \
     && apt update \
     && apt install -y --no-install-recommends vim 

EXPOSE 3978
 
COPY /functionaltestbot /functionaltestbot


RUN  pip3 install -r /functionaltestbot/requirements.txt

ENV FLASK_APP=/functionaltestbot/main.py
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH ${PATH}:/home/site/wwwroot

WORKDIR bot
# Initialize models


# For Debugging, uncomment the following: 
#ENTRYPOINT ["python3.6", "-c", "import time ; time.sleep(500000)"]

# For Devops, they don't like entry points.  This is now in the devops 
# pipeline.
# ENTRYPOINT [ "flask" ]
# CMD [ "run", "--port", "3978", "--host", "0.0.0.0" ]