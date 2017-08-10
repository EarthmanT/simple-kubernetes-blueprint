[![Build Status](https://circleci.com/gh/cloudify-examples/simple-kubernetes-blueprint.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/cloudify-examples/simple-kubernetes-blueprint)


##  Kubernetes Cluster Example

This blueprint creates an example Kubernetes cluster. It is intended as an example. The underlying Kubernetes configuration method used is [Kubeadm](https://kubernetes.io/docs/admin/kubeadm/), which is not considered production-ready.

Regardless of your infrastructure choice, this blueprint installs and configures on each VM:
- The Kubernetes Yum repo will be installed on your VMs.
- Docker, version 1.12.6-28.git1398f24.el7.centos
- kubelet, version 1.6.4-0.
- kubeadm, version 1.6.4-0.
- kubernetes-cni, version 0.5.1-0.
- weave


## prerequisites

You will need a *Cloudify Manager* running in either AWS, Azure, or Openstack. The Cloudify manager should be setup using the [Cloudify environment setup](https://github.com/cloudify-examples/cloudify-environment-setup) - that's how we test this blueprint. The following are therefore assumed:
* You have uploaded all of the required plugins to your manager in order to use this blueprint. (See the imports section of the blueprint.yaml file to check that you are using the correct plugins and their respective versions.)
* You have created all of the required secrets on your manager in order to use this blueprint. (See #secrets.)
* A Centos 7.X image. If you are running in AWS or Openstack, your image must support [Cloud-init](https://cloudinit.readthedocs.io/en/latest/).


#### Secrets

* Common Secrets:
  * agent_key_private
  * agent_key_public


* AWS Secrets:
  * vpc_id: This is the ID of the vpc. The same vpc that your manager is attached to.
  * private_subnet_id: This is the ID of a subnet that does not have inbound internet access on the vpc. Outbound internet access is required to download the requirements.  It must be on the same vpc designated by VPC_ID.
  * public_subnet_id: This is the ID of a subnet that does have internet access (inbound and outbound).  It must be on the same vpc designated by VPC_ID.
  * availability_zone: The availability zone that you want your instances created in. This must be the same as your public_subnet_id and private_subnet_id.
  * [ec2_region_endpoint](http://docs.aws.amazon.com/general/latest/gr/rande.html): The AWS region endpint, such as ec2.us-east-1.amazonaws.com.
  * ec2_region_name: The AWS region name, such as ec2_region_name.
  * aws_secret_access_key: Your AWS Secret Access Key. See [here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration) for more info. This may not be provided as an environment variable. The string must be set as a secret.
  * aws_access_key_id: Your AWS Access Key ID. See [here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration) for more info. This may not be provided as an environment variable. The string must be set as a secret.


* Azure Secrets:
  * location: See [here](https://azure.microsoft.com/en-us/regions/).
  * mgr_virtual_network_name: This is the name of the virtual network that your manager is attached to.
  * mgr_subnet_name: The is the name of the subnet that your manager is attached to.
  * mgr_resource_group_name: This the resource group that your manager is sitting in.
  * client_secret: Your Azure Service Principal password. See [here](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-authenticate-service-principal-cli#create-service-principal-with-password).
  * client_id: Your Azure Service Principal appId. See [here](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-authenticate-service-principal-cli#create-service-principal-with-password).
  * tenant_id: Your Azure Service Principal tenant. See [here](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-authenticate-service-principal-cli#create-service-principal-with-password).
  * subscription_id: Your Azure subscription ID.


* Openstack Secrets:
  * external_network_name: This is the network on your Openstack that represents the internet gateway network.
  * public_network_name: An openstack network. (Inbound is expected, outbound is required.)
  * public_subnet_name: A subnet on the public network.
  * private_network_name: An openstack network. (Inbound is not expected, outbound is required.)
  * private_subnet_name: A subnet on the network. (Inbound is not expected, outbound is required.)
  * router_name: This is a router that is attached to your Subnets designated in the secrets public_subnet_name and private_subnet_name.
  * region: Your Keystone V2 region.
  * keystone_url: Your Keystone V2 auth URL.
  * keystone_tenant_name: Your Keystone V2 tenant name.
  * keystone_password: Your Keystone V2 password.
  * keystone_username:Your Keystone V2 username.


### Step 1: Install the simple Kubernetes cluster


#### For AWS run:

```shell
$ cfy install \
    https://github.com/cloudify-examples/simple-kubernetes-blueprint/archive/4.1.1.zip \
    -b k8s \
    -n aws-blueprint.yaml
```


#### For Azure run:

```shell
$ cfy install \
    https://github.com/cloudify-examples/simple-kubernetes-blueprint/archive/4.1.1.zip \
    -b k8s \
    -n azure-blueprint.yaml
```


#### For Openstack run:

```shell
$ cfy install \
    https://github.com/cloudify-examples/simple-kubernetes-blueprint/archive/4.1.1.zip \
    -b k8s \
    -n openstack-blueprint.yaml
```


You should see something like this when you execute the command:

```shell
$ cfy install \
    https://github.com/cloudify-examples/simple-kubernetes-blueprint/archive/4.1.1.zip \
    -b k8s \
    -n aws-blueprint.yaml
Uploading blueprint simple-kubernetes-blueprint/aws-blueprint.yaml...
 aws-blueprint.yaml |##################################################| 100.0%
Blueprint uploaded. The blueprint's id is k8s
Creating new deployment from blueprint aws...
Deployment created. The deployment's id is k8s
Executing workflow install on deployment aws [timeout=900 seconds]
Deployment environment creation is in progress...
```


### Step 2: Verify the demo installed and started.

Once the workflow execution is complete, verify that these secrets were created:


```shell
(Incubator)UNICORN:Projects trammell$ cfy secrets list
Listing all secrets...

Secrets:
+------------------------------------------+--------------------------+--------------------------+------------+----------------+------------+
|                   key                    |        created_at        |        updated_at        | permission |  tenant_name   | created_by |
+------------------------------------------+--------------------------+--------------------------+------------+----------------+------------+
| kubernetes-admin_client_certificate_data | 2017-08-09 14:58:06.421  | 2017-08-09 14:58:06.421  |            | default_tenant |   admin    |
|     kubernetes-admin_client_key_data     | 2017-08-09 14:58:06.513  | 2017-08-09 14:58:06.513  |            | default_tenant |   admin    |
|  kubernetes_certificate_authority_data   | 2017-08-09 14:58:06.327  | 2017-08-09 14:58:06.327  |            | default_tenant |   admin    |
|           kubernetes_master_ip           | 2017-08-09 14:56:12.359  | 2017-08-09 14:56:12.359  |            | default_tenant |   admin    |
|          kubernetes_master_port          | 2017-08-09 14:56:12.452  | 2017-08-09 14:56:12.452  |            | default_tenant |   admin    |
+------------------------------------------+--------------------------+--------------------------+------------+----------------+------------+
```


### Step 3: Run demo Kubernetes applications

You can now run a demo kubernetes application:

```shell
$ cfy install \
    https://github.com/cloudify-incubator/cloudify-kubernetes-plugin/archive/master.zip \
    -b wordpress \
    -n examples/wordpress-blueprint.yaml
```
