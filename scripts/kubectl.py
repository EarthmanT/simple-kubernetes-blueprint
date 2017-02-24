#!/usr/bin/env python

import stat
import urllib
from cloudify.exceptions import NonRecoverableError
from cloudify import ctx
import os
from cloudify.state import ctx_parameters as inputs
import subprocess

PATH = os.path.join(
    os.path.expanduser('~'),
    'kubectl'
)


if __name__ == '__main__':

    ctx.logger.info('Installing kubectl')

    url = inputs['kubectl_url']

    try:
        urllib.urlretrieve(url, PATH)
    except:
        raise NonRecoverableError()

    st = os.stat(PATH)
    os.chmod(PATH, st.st_mode | stat.S_IEXEC)

    command = 'sudo mv {0} /usr/local/bin/kubectl'.format(PATH)

    result = subprocess.Popen(
        command.split(),
        cwd=os.path.expanduser('~')
    )

    output = result.communicate()

    if result.returncode:
        raise NonRecoverableError(
            'Error: {0} '
            'Output: {1}'.format(result.returncode, output)
        )
