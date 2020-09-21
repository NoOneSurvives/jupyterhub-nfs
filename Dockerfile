# base image: jupyterhub
# this is built by docker-compose
# from the root of this repo
# Trying to use latest version
FROM jupyterhub/jupyterhub
# install dockerspawner from the current repo
#ADD . /tmp/dockerspawner
RUN pip install --no-cache dockerspawner
# install dummyauthenticator
#RUN pip install --no-cache jupyterhub-dummyauthenticator
# install cull-idle module
RUN pip install --no-cache jupyterhub_idle_culler
RUN pip install --no-cache jupyterhub-firstuseauthenticator
# load configuration
ADD ./jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
