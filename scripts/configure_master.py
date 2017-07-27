#!/usr/bin/env python

import pwd
import grp
import os
import getpass
import subprocess
from cloudify import ctx


def execute_command(_command):

    ctx.logger.debug('_command {0}.'.format(_command))

    subprocess_args = {
        'args': _command.split(),
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE
    }

    ctx.logger.debug('subprocess_args {0}.'.format(subprocess_args))

    process = subprocess.Popen(**subprocess_args)
    output, error = process.communicate()

    ctx.logger.debug('command: {0} '.format(_command))
    ctx.logger.debug('output: {0} '.format(output))
    ctx.logger.debug('error: {0} '.format(error))
    ctx.logger.debug('process.returncode: {0} '.format(process.returncode))

    if process.returncode:
        ctx.logger.error('Running `{0}` returns error.'.format(_command))
        return False

    return output


if __name__ == '__main__':

    # Start the Kube Master
    start_output = execute_command('sudo kubeadm init --skip-preflight-checks')
    for line in start_output.split('\n'):
        if 'kubeadm join' in line:
            ctx.instance.runtime_properties['join_command'] = line.lstrip()

    # Add the kubeadmin config to environment
    agent_user = getpass.getuser()
    uid = pwd.getpwnam(agent_user).pw_uid
    gid = grp.getgrnam('docker').gr_gid
    admin_file_dest = os.path.join(os.path.expanduser('~'), 'admin.conf')

    execute_command('sudo cp {0} {1}'.format('/etc/kubernetes/admin.conf', admin_file_dest))
    execute_command('sudo chown {0}:{1} {2}'.format(uid, gid, admin_file_dest))

    with open(os.path.join(os.path.expanduser('~'), '.bashrc'), 'a') as outfile:
        outfile.write('export KUBECONFIG=$HOME/admin.conf')
    os.environ['KUBECONFIG'] = admin_file_dest
    execute_command('kubectl apply -f https://git.io/weave-kube-1.6')

    # Install weave-related utils
    execute_command('sudo curl -L git.io/weave -o /usr/local/bin/weave')
    execute_command('sudo chmod a+x /usr/local/bin/weave')
    execute_command('sudo curl -L git.io/scope -o /usr/local/bin/scope')
    execute_command('sudo chmod a+x /usr/local/bin/scope')
    execute_command('scope launch')
