# The proxy is in another container
c.ConfigurableHTTPProxy.should_start = False
c.ConfigurableHTTPProxy.api_url = 'http://proxy:8001'
# tell the hub to use Dummy Auth (for testing)
#c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'
# Use db-like authenticator
c.JupyterHub.authenticator_class = 'firstuseauthenticator.FirstUseAuthenticator'
c.FirstUseAuthenticator.dbm_path = 'password'
c.FirstUseAuthenticator.create_users = False
# Admins:
c.Authenticator.admin_users = {'kesh'}
c.JupyterHub.admin_access = True
# use SwarmSpawner
c.JupyterHub.spawner_class = 'dockerspawner.SwarmSpawner'
# The Hub should listen on all interfaces,
# so user servers can connect
c.JupyterHub.hub_ip = '0.0.0.0'
# this is the name of the 'service' in docker-compose.yml
c.JupyterHub.hub_connect_ip = 'hub'
# this is the network name for jupyterhub in docker-compose.yml
# with a leading 'swarm_' that docker-compose adds
c.SwarmSpawner.network_name = 'swarm_jupyterhub-net-nfs'
# Spawners start block
c.Spawner.cmd = ["jupyterhub-singleuser"]
# Enough for start
c.Spawner.cpu_limit = 0.5
c.Spawner.mem_limit = '128M'
# Docker data persistence
import os
def create_dir_hook(spawner):
    username = spawner.user.name  # get the username
    volume_path = os.path.join('/mnt/nfs', username)
    if not os.path.exists(volume_path):
	# 777 for all users include jovyan
        os.mkdir(volume_path, 0o777)
    mounts_user = [
                   {'type': 'bind',
                    'source': '/mnt/nfs/' + username,
                    'target': '/home/jovyan/work', }
                   ]
    spawner.extra_container_spec = {
        'mounts': mounts_user
    }

# attach the hook function to the spawner
c.Spawner.pre_spawn_hook = create_dir_hook
# debug-logging for testing
import logging
c.JupyterHub.log_level = logging.DEBUG
# Kill user server on logout
c.JupyterHub.shutdown_on_logout = True
# Autostop not using containers
import sys
c.JupyterHub.services = [
    {
        'name': 'cull-idle',
        'admin': True,
        'command': [sys.executable, '-m', 'jupyterhub_idle_culler', '--timeout=600'],
    }
]