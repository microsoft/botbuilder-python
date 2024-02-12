# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

FROM  mcr.microsoft.com/oryx/python:3.10


RUN  mkdir /functionaltestbot 

EXPOSE 443
# EXPOSE 2222

COPY ./functionaltestbot /functionaltestbot
COPY setup.py /
COPY test.sh /
# RUN ls -ltr
# RUN cat prestart.sh
# RUN cat main.py

ENV FLASK_APP=/functionaltestbot/app.py
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH ${PATH}:/home/site/wwwroot

WORKDIR /

# Initialize the bot
RUN  pip3 install -e .

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
        && apt-get install -y --no-install-recommends dialog \
        && apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd \
    && apt install -y --no-install-recommends vim 
COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh

# For Debugging, uncomment the following: 
# ENTRYPOINT ["python3.6", "-c", "import time ; time.sleep(500000)"]
ENTRYPOINT ["init.sh"]
 
# For Devops, they don't like entry points.  This is now in the devops 
# pipeline.
# ENTRYPOINT [ "flask" ]
# CMD [ "run", "--port", "3978", "--host", "0.0.0.0" ]
