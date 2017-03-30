#!/usr/bin/env python

import os
import subprocess
from cloudify import ctx
from cloudify.exceptions import NonRecoverableError
import stat

work_environment = os.environ.copy()
work_dir = os.path.expanduser("~")


def install_docker(script):
    ctx.logger.info('Installing Docker.')
    process = subprocess.Popen(
        ['sudo', 'sh', script],
        stdout=open(os.devnull, 'w'),
        stderr=subprocess.PIPE
    )

    output, error = process.communicate()

    if process.returncode:
        raise NonRecoverableError(
            'Failed to start Docker bootstrap. '
            'Output: {0}'
            'Error: {1}'.format(output, error)
        )

    return


def check_for_docker():

    command = 'docker ps'

    try:
        process = subprocess.Popen(
            command.split()
        )
    except OSError:
        return False

    output, error = process.communicate()

    ctx.logger.debug(
        'Command: {0} '
        'Command output: {1} '
        'Command error: {2} '
        'Return code: {3}'.format(command, output, error, process.returncode))

    if process.returncode:
        ctx.logger.error('Docker PS returncode was negative. '
                         'Risk of bad installation.')
        return False

    return True


if __name__ == '__main__':

    command = 'sudo apt-get update'
    subprocess.Popen(
        command.split(),
        stdout=open(os.devnull, 'w'),
        stderr=open(os.devnull, 'w')
    ).wait()

    if not check_for_docker():
        ctx.logger.info('Install Docker.')
        path_to_script = os.path.join('scripts/', 'install_docker.sh')
        install_script = ctx.download_resource(path_to_script)
        st = os.stat(install_script)
        os.chmod(install_script, st.st_mode | stat.S_IEXEC)
        install_docker(install_script)

    if not check_for_docker():
        raise NonRecoverableError(
            'Failed to install Docker. '
            'Check debug log for more info. '
        )
