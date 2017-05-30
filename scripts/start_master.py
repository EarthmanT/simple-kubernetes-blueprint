#!/usr/bin/env python

import os
import subprocess
from cloudify import ctx
from cloudify.exceptions import RecoverableError


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


def check_kubedns_status(_get_pods):

    ctx.logger.debug('get_pods: {0} '.format(_get_pods))

    for pod_line in _get_pods.split('\n'):
        ctx.logger.debug('pod_line: {0} '.format(pod_line))
        try:
            _namespace, _name, _ready, _status, _restarts, _age = pod_line.split()
        except ValueError:
            pass
        else:
            if 'kube-dns' in _name and 'Running' not in _status:
                return False
            elif 'kube-dns' in _name and 'Running' in _status:
                return True
    return False


if __name__ == '__main__':

    admin_file_dest = os.path.join(os.path.expanduser('~'), 'admin.conf')
    os.environ['KUBECONFIG'] = admin_file_dest

    get_pods = execute_command('kubectl get pods --all-namespaces')

    if not check_kubedns_status(get_pods):
        raise RecoverableError('kube-dns not Running')

    with open(admin_file_dest, 'r') as outfile:
        configuration_file_contents = outfile.read()

    ctx.instance.runtime_properties['configuration_file_content'] = \
        configuration_file_contents
