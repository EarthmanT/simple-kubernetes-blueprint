[![Build Status](https://circleci.com/gh/cloudify-examples/simple-kubernetes-blueprint.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/cloudify-examples/simple-kubernetes-blueprint)

##  Simple Kubernetes Example Blueprint

The blueprints in this project provide orchestration for starting, healing, and scaling a [Kubernetes](https://kubenretes.io/) cluster on Openstack.  There are 2 blueprints, with slightly different use cases:
* **openstack-blueprint.yaml** : an Openstack bluieprint that orchestrates setup, teardown, autohealing, and autoscaling of the cluster
* **service-blueprint** : an example blueprint that uses the [Kubernetes plugin](https://github.com/cloudify-examples/cloudify-kubernetes-plugin) to install a simple Nginx service on the Kubernetes cluster.

### Prerequisites

These blueprints have only been tested against an Ubuntu 14.04 image with 2GB of RAM.  The image used must be pre-installed with Docker 1.11.  Any image used should have passwordless ssh, and passwordless sudo with `requiretty` false or commented out in sudoers.  Also required is an Openstack cloud environment.  The blueprints were tested on Openstack Kilo.

### Cloudify Version

These blueprints were tested on Cloudify 3.4.0.

### Operation

#### openstack-blueprint.yaml instructions

* Start a Cloudify 3.4.0 [manager](http://docs.getcloudify.org/3.4.0/manager/bootstrapping/).
* Edit the `inputs.yaml` file to add image, flavor, and user name (probably ubuntu).
* run `cfy blueprints upload -b kubernetes -p kubernetes-openstack-blueprint.yaml`
* run `cfy deployments create -b kubernetes -d kubernetes -i input/openstack.yaml`
* run `cfy executions start -d kubernetes -w install`

This will create the Kubernetes cluster, including the Kubernetes dashboard.  The Kubernetes dashboard URL is displayed by running `cfy deployments outputs -d kubernetes`.

To see autohealing in action, go to the Openstack Horizon dashboard and terminate the worker.  Then go to the Cloudify UI deployments tab.  See the `heal` workflow begin and restore the missing node.

To see autoscaling in action:
* ssh to the Cloudify manager: `cfy ssh`
* ssh to a kubernetes worker node: `sudo ssh -i /root/.ssh/agent_key.pem ubuntu@<worker-ip>`
* run `sudo apt-get install -y stress`
* run `stress -c 2 -t 10`
* Then go to the Cloudify UI deployments tab.  See the `scale` workflow begin and grow the cluster.

In a few minutes, the cluster will scale down to it's original size (one worker) due to the scale down policy in the blueprint.

To tear down the cluster, run `cfy executions start -d kubernetes -w uninstall`

#### service-blueprint.yaml instructions

* With the Kubernetes cluster started as describe above (deployment must be named `kubernetes for this example`), run `cfy blueprints upload -b service -p service-blueprint.yaml`.
* run `cfy deployments create -b service -d service`
* run `cfy executions start -d service -w install`

This will install an Nginx service and the Nginx containers on the Kubernetes environment.  This will be visible via the Kubernetes dashboard as describe above.

To uninstall the service and containers, run `cfy executions start -d service -w uninstall`
