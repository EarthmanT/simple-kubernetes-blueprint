#!/usr/bin/env python

import subprocess
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
from cloudify.exceptions import NonRecoverableError

START_COMMAND = 'sudo kubeadm join --token {0} {1}:{2}'


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

    hostname = execute_command('hostname')
    ctx.instance.runtime_properties['hostname'] = hostname.rstrip('\n')

    # Get the master cluster info.
    masters = \
        [x for x in ctx.instance.relationships if
         x.target.instance.runtime_properties.get(
             'KUBERNETES_MASTER', False)]
    if len(masters) != 1:
        bootstrap_token = inputs.get('bootstrap_token')
        master_ip = inputs.get('master_ip')
        master_port = inputs.get('master_port')
    else:
        props = masters[0].target.instance.runtime_properties
        bootstrap_token = props.get('bootstrap_token')
        master_ip = props.get('master_ip')
        master_port = props.get('master_port')

    if not bootstrap_token and not master_ip and not master_port:
        raise NonRecoverableError(
            'The following required variables are empty: '
            'bootstrap_token, master_ip and master_port')

    # Join the cluster.
    join_command = \
        'sudo kubeadm join --token {0} {1}:{2} --skip-preflight-checks'.format(
            bootstrap_token, master_ip, master_port)
    execute_command(join_command)

    # Install weave-related utils
    execute_command('sudo curl -L git.io/weave -o /usr/local/bin/weave')
    execute_command('sudo chmod a+x /usr/local/bin/weave')
    execute_command('sudo curl -L git.io/scope -o /usr/local/bin/scope')
    execute_command('sudo chmod a+x /usr/local/bin/scope')
    execute_command('/usr/local/bin/scope launch')
