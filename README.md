[![Build Status](https://circleci.com/gh/cloudify-examples/simple-kubernetes-blueprint.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/cloudify-examples/simple-kubernetes-blueprint)

##  Simple Kubernetes Blueprint

This blueprint deploys a simple Kubernetes cluster.

## prerequisites

You will need a *Cloudify Manager* running in either AWS, Azure, or Openstack.

If you have not already, set up the [example Cloudify environment](https://github.com/cloudify-examples/cloudify-environment-setup). Installing that blueprint and following all of the configuration instructions will ensure you have all of the prerequisites, including keys, plugins, and secrets.


### Step 1: Install the demo application

In this step, you will first gather two pieces of information from your Cloud account: the parameters of a Centos 7.0 image and a medium sized image. This info is already provided for AWS us-east-1 and Azure us-east.

Next you provide those inputs to the blueprint and execute install:

#### For AWS run:

```shell
$ cfy install \
    https://github.com/cloudify-examples/simple-kubernetes-blueprint/archive/4.0.1.zip \
    -b demo \
    -n aws-blueprint.yaml
```


#### For Azure run:

```shell
$ cfy install \
    https://github.com/cloudify-examples/simple-kubernetes-blueprint/archive/4.0.1.zip \
    -b demo \
    -n azure-blueprint.yaml
```


#### For Openstack run:

```shell
$ cfy install \
    https://github.com/cloudify-examples/simple-kubernetes-blueprint/archive/4.0.1.zip \
    -b demo \
    -n openstack-blueprint.yaml -i flavor=[MEDIUM_SIZED_FLAVOR] -i image=[CENTOS_7_IMAGE_ID]
```


You should see something like this when you execute the command:

```shell
$ cfy install \
    https://github.com/cloudify-examples/simple-kubernetes-blueprint/archive/4.0.1.zip \
    -b demo \
    -n aws-blueprint.yaml
Uploading blueprint simple-kubernetes-blueprint/aws-blueprint.yaml...
 aws-blueprint.yaml |##################################################| 100.0%
Blueprint uploaded. The blueprint's id is aws
Creating new deployment from blueprint aws...
Deployment created. The deployment's id is aws
Executing workflow install on deployment aws [timeout=900 seconds]
Deployment environment creation is in progress...
2017-05-30 11:35:20.609  CFY <simple-kubernetes-blueprint> Starting 'create_deployment_environment' workflow execution
2017-05-30 11:35:20.941  CFY <simple-kubernetes-blueprint> Installing deployment plugins
2017-05-30 11:35:21.028  CFY <simple-kubernetes-blueprint> [,] Sending task 'cloudify_agent.operations.install_plugins'
2017-05-30 11:35:21.067  CFY <simple-kubernetes-blueprint> [,] Task started 'cloudify_agent.operations.install_plugins'
2017-05-30 11:35:21.094  LOG <simple-kubernetes-blueprint> [,] INFO: Installing plugin: aws
2017-05-30 11:35:21.688  LOG <simple-kubernetes-blueprint> [,] INFO: Using existing installation of managed plugin: 444f7f27-6508-45fe-8d18-a0b2da729538 [package_name: cloudify-aws-plugin, package_version: 1.4.9, supported_platform: linux_x86_64, distribution: centos, distribution_release: core]
2017-05-30 11:35:21.713  CFY <simple-kubernetes-blueprint> [,] Task succeeded 'cloudify_agent.operations.install_plugins'
2017-05-30 11:35:21.866  CFY <simple-kubernetes-blueprint> Starting deployment policy engine core
2017-05-30 11:35:22.053  CFY <simple-kubernetes-blueprint> [,] Sending task 'riemann_controller.tasks.create'
2017-05-30 11:35:22.069  CFY <simple-kubernetes-blueprint> [,] Task started 'riemann_controller.tasks.create'
2017-05-30 11:35:23.093  CFY <simple-kubernetes-blueprint> [,] Task succeeded 'riemann_controller.tasks.create'
2017-05-30 11:35:23.344  CFY <simple-kubernetes-blueprint> Creating deployment work directory
2017-05-30 11:35:23.670  CFY <simple-kubernetes-blueprint> 'create_deployment_environment' workflow execution succeeded
2017-05-30 11:35:26.137  CFY <simple-kubernetes-blueprint> Starting 'install' workflow execution
```


### Step 2: Verify the demo installed and started.

Once the workflow execution is complete, get your configuration file contents from your Kubernetes master:


```shell
$ cfy node-instances list
Listing all instances...

Node-instances:
+-----------------------------------+---------------------------------------+-------------------------------+----------------------------+---------------+------------+----------------+------------+
|                 id                | deployment_id                         |            host_id            |          node_id           |     state     | permission |  tenant_name   | created_by |
+-----------------------------------+---------------------------------------+-------------------------------+----------------------------+---------------+------------+----------------+------------+
| cloudify_host_cloud_config_ff84al |      simple-kubernetes-blueprint      |                               | cloudify_host_cloud_config |    started    |  creator   | default_tenant |   admin    |
|      kubernetes_master_rzob7x     |      simple-kubernetes-blueprint      | kubernetes_master_host_5puozx |     kubernetes_master      |    started    |  creator   | default_tenant |   admin    |
|   kubernetes_master_host_5puozx   |      simple-kubernetes-blueprint      | kubernetes_master_host_5puozx |   kubernetes_master_host   |    started    |  creator   | default_tenant |   admin    |
|    kubernetes_master_ip_zn18sp    |      simple-kubernetes-blueprint      |                               |    kubernetes_master_ip    |    started    |  creator   | default_tenant |   admin    |
|       kubernetes_node_sq215s      |      simple-kubernetes-blueprint      |  kubernetes_node_host_j4zbdi  |      kubernetes_node       |    started    |  creator   | default_tenant |   admin    |
|    kubernetes_node_host_j4zbdi    |      simple-kubernetes-blueprint      |  kubernetes_node_host_j4zbdi  |    kubernetes_node_host    |    started    |  creator   | default_tenant |   admin    |
|  kubernetes_security_group_qmlgu1 |      simple-kubernetes-blueprint      |                               | kubernetes_security_group  |    started    |  creator   | default_tenant |   admin    |
|       private_subnet_wms6tb       |      simple-kubernetes-blueprint      |                               |       private_subnet       |    started    |  creator   | default_tenant |   admin    |
|        public_subnet_nfl134       |      simple-kubernetes-blueprint      |                               |       public_subnet        |    started    |  creator   | default_tenant |   admin    |
|          ssh_group_ov2gy2         |      simple-kubernetes-blueprint      |                               |         ssh_group          |    started    |  creator   | default_tenant |   admin    |
|             vpc_wwpkx7            |      simple-kubernetes-blueprint      |                               |            vpc             |    started    |  creator   | default_tenant |   admin    |
+-----------------------------------+---------------+-------------------------------+----------------------------+---------------+------------+----------------+------------+


$ cfy node-i get kubernetes_master_rzob7x
Retrieving node instance kubernetes_master_rzob7x

Node-instance:
+--------------------------+---------------------------------------+-------------------------------+-------------------+---------+------------+----------------+------------+
|            id            | deployment_id                         |            host_id            |      node_id      |  state  | permission |  tenant_name   | created_by |
+--------------------------+---------------------------------------+-------------------------------+-------------------+---------+------------+----------------+------------+
| kubernetes_master_rzob7x |      simple-kubernetes-blueprint      | kubernetes_master_host_5puozx | kubernetes_master | started |  creator   | default_tenant |   admin    |
+--------------------------+---------------------------------------+-------------------------------+-------------------+---------+------------+----------------+------------+

Instance runtime properties:
	join_command: kubeadm join --token 163f7e.2be3d0fcf46a7f5d 10.10.0.153:6443
	configuration_file_content: apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUN5RENDQWJDZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRFM01EVXpNREV4TXpreE9Gb1hEVEkzTURVeU9ERXhNemt4T0Zvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBT1d6Cjg0WUQ5UjlMdURLc1NTeVlHTjFZQUNpUE1XSVgvTVJoYzN4emdIbzhQbGZmSitZQ0xGUjhqSy9oZUhtdnV6NXkKcVI0bWpuakpyWFJrc3A4VE1QckhQODB4dXVuWGg2K0dad05WR3pOckpZUVBKcFlXVmo4NkE4MDQzZ1NmNStrVgp5dnFhYVJwd1JZVEMxYkhQOTE0MXZITG9OTUNtaWdheXhmemJJOVFETjFwN2FpMmNFbEp3WmN0S3luK2ltd3UvCkJXbm5WK1NOWEYycXU5cnhpVGtEcWdJOVlXcUFjRFNFcHhmY0RuR0VkVjdFNWxEWDRtaks0Q0Exbk10dE8rUWcKQ3dQWEJmSW52RjVRU2c1dzIxb2tzU0k5Yk9GdWRxeWhOVUlUck1VdURaV0Z2MXZTT1JmU1ZuS2I5YzZMaTBNZwpuNHRzd3FTaFRrajlwS3JhZ1hNQ0F3RUFBYU1qTUNFd0RnWURWUjBQQVFIL0JBUURBZ0trTUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dFQkFLRTRxdWxBbWdUcWFZWFJNSzZDTmhveGpTYXAKeVZlNFRCd0VzN1IzK214ZWxieEsxYjNJTEVyU1lmYkFGVFNWQTlJbEhNTnp5aStKZGNMVm1vUFFVQjZKN2hrbQpkYTBvSWM2Q1prWElCZk9Ccm1lT3JrWFlxYUdvYWNpV0xzcnV4MElIdnFTbWRhZ3JCeWR6M3dqOU0xR0J4MGVGClBIUllpTDY2TEpzVTk4aVNrTzBEeW1maEdadnRHRTgvY0lpRlk4YmYyWDNwb2dBWlJLTlhTb3BxWGx2SklsdU8KR0FWQlhHMTdGNDRpbjRYWGpVTUpVUjQwVUZoWjBPcWt6Z2NRay9yWDN4TUZhK1BmSXhZK2dTVHN3UjBUcDRmdwoyUVpqdWNzdk5XMHFSV1BqTDA5WHdPZUdWbnpGYVBvRHZLOGVkMGVGMUFIdnNZQTlhMWNSdGlSc3VLcz0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
    server: https://10.10.0.153:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
kind: Config
preferences: {}
users:
- name: kubernetes-admin
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUM4akNDQWRxZ0F3SUJBZ0lJUkVZL3VnNnJZQXN3RFFZSktvWklodmNOQVFFTEJRQXdGVEVUTUJFR0ExVUUKQXhNS2EzVmlaWEp1WlhSbGN6QWVGdzB4TnpBMU16QXhNVE01TVRoYUZ3MHhPREExTXpBeE1UTTVNakJhTURReApGekFWQmdOVkJBb1REbk41YzNSbGJUcHRZWE4wWlhKek1Sa3dGd1lEVlFRREV4QnJkV0psY201bGRHVnpMV0ZrCmJXbHVNSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQTVENFBBdXZLYjBER0l3QjAKd1Z4US9VUHorR1N4U2V1L2E0MDY4M0ZuV0JiSEtWWGNLMnFpcGMrZTFaKzM5OWhFTHpaVnh2OFI2RHRLUHA1VApHdkR2aTRneUdnckJpQWZGdFlUc1JuT0JFTnZPMEVMdUhXV09XRHFZeldIYk1sTFRINDZ0VzMwYUsvRFRzcC9JClA2TUNwSWpYd3luQkV4NjVXL2hzUlFiNUlRZ3BmQ25TMmYrQnZqd1dDUkNPOEU3YUpxMXB6TlBIWHdQVDgzQncKcklSS0ZxbUdXeFYvOGVCd2RXODN3Mm0xcHREUWxCdVZiVUNvMGF4R0lPQXVpOFNPbHJ2aGFkL2J3NUZxRWJGTQovVDZOcVduc1ZPaWlKZU56RjZrUkpiUHppc0FuWVpxNUl1eG5HaWdLYnFNY2xJdjk3NUNGQmhISTRGUG1aT1FqCkRhVUk5UUlEQVFBQm95Y3dKVEFPQmdOVkhROEJBZjhFQkFNQ0JhQXdFd1lEVlIwbEJBd3dDZ1lJS3dZQkJRVUgKQXdJd0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dFQkFLR2g3RnNMM1BhOTBORVhRRFlTd0EwQTNPTnlKcWEvb0g5Ygp6R2JIMDB3UkVLUis3UVVpNkdQbUJIdG1GSWRReXR3cWpMcENjYm9rS0IyTkYvRUF3VnZPN3VubFZ6Tmk0QjBBCmpSR3c0QWswSTVEc0Z0UU0yaUo2SmpRTzRGYmlxcldTZkNXMU9DaEViei9RbmdMQ0pRN1FteHhxcjNsWVVqeDYKTXBKRmd6OVNmVGVFNUNpQjVhT3QvU0pWSVJYU3hGNWtVc3c0K1FjcWRHeWFRa2hRRERERUZyZEplcWczRkFFcwpmbmR5RmNOOExnYURJcWFDSUp0MFYzSWFNbUFvMS9XVElrVHVJQmxOZzdJZG1wUTl4dGwvSjJLY3pGR1FKMFZWCnVxbG40ajJvOWk2b1o3ZmExTThwUUFlOWpicGdNRW9lNld3ckpDWkxUSVRCRjF1MVp1Zz0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBNUQ0UEF1dktiMERHSXdCMHdWeFEvVVB6K0dTeFNldS9hNDA2ODNGbldCYkhLVlhjCksycWlwYytlMVorMzk5aEVMelpWeHY4UjZEdEtQcDVUR3ZEdmk0Z3lHZ3JCaUFmRnRZVHNSbk9CRU52TzBFTHUKSFdXT1dEcVl6V0hiTWxMVEg0NnRXMzBhSy9EVHNwL0lQNk1DcElqWHd5bkJFeDY1Vy9oc1JRYjVJUWdwZkNuUwoyZitCdmp3V0NSQ084RTdhSnExcHpOUEhYd1BUODNCd3JJUktGcW1HV3hWLzhlQndkVzgzdzJtMXB0RFFsQnVWCmJVQ28wYXhHSU9BdWk4U09scnZoYWQvYnc1RnFFYkZNL1Q2TnFXbnNWT2lpSmVOekY2a1JKYlB6aXNBbllacTUKSXV4bkdpZ0ticU1jbEl2OTc1Q0ZCaEhJNEZQbVpPUWpEYVVJOVFJREFRQUJBb0lCQVFDeCtqSjZkS05HWFp3agpieGVjTUFCM2ZhV2c2K1BUWUtIRG5EMTcxOUplUG1UUE5zU1lsbTUrSFlnZHpJNElGZndWVktsT28xZXpYNGhsCmk5QUNFaDY1RDFzQ002RDJFaGw1a2swc0lxVmlJQVVGSVN2TWdJU2ZDQkpmRlE5NERsM1RIYzdRcUp6ZjVzc3QKWHFzbjlGVDdPRG9IVldmWklQd3BXMjRSNVg0ZTRtVGp5SmJoTm84NUhhZGxZMHoyTVAxRTdvaThNS1BvRWMxdwpXL0tZcHQyNTdIZzJ1TSsrOE9aaG1sYkRzOHptWTlScEtKRVpBMXpscGFZVDdvVE0xK0RjYU5xTTNqelczbGJ5CjdmNjhxQ3lqWU1KWUFrNy8rTUtTcEk0Mk5OVXh5SXo4cWw0K0tGSjJyNDE3U0lsc2paT2wrcmczZG13N2FKbkUKNFY3dmV3dUJBb0dCQVAra3g3TFBrbE02N3NkdXArTzNkZ3hnZlRla2xjOVVuVHE3NXBsQ2J2bll1YkFQeDZwSgo4U2I2V3FBSDFHZFdGazdWVzhDekVkMUlDNC9aSVprbXRjSVdZUm43d2FJcHk5a3J3UFRJeFk4UHFTSTVMVnd0ClYzcGcrL0lOaGdFU0hDSk8vaXo0L0Z5OWY0UmRpa3ZKOHFJeE9IUUx3bUJJWjAza3hTeXBUS1B6QW9HQkFPU1AKZ0VuVWY0aXUvK0VhUm03U1E4bC9IYkZoMHJvemZVRGhhUGNNK3p1UEtINGM1Rk1OWnRnM1JRcXRsWXNaTGtVVwpJTmR4eU9UNjhwRWZaK1c2ZzcvbGRLSDRwMlRHcmhmSTVsRkNPVThEZS8zcjhFdzJFRFR0OGJuUGpFNmNaaVpqCm0wcGwyM0JSYlZvWEUvdWxkRlB6ZmVnQ2tvNVZ4cWlma0crbnM2RjNBb0dCQVBPdUdJVURnMUUremJqZ2E3eU8KZGtJWi80SDRxcXgwMVdMVkZWeGxqTzh2Zk9Dc1NnQ3lkdUpXcGVnQlRxQXAyUjNRRnFPNmpYN0dXKzhFWkJoZQpZOGJjR2pid1dZVEFIb1dtUlVtUHozRXMxbVcrNXRRRWpHd2s0a082VEUvYytXQml0N29hcEVPcWhsQ2Y4V0dJCjRIVm1RWStzWGQzMVpqTkRyQWVFWVgrdEFvR0FYaTRYZ2RTelBLSkh3L3pzdXV1ZmpSNzVJRWViNnFnZTI2WkcKZDA1OUU1eTQ1Y2FIK3dVUnROU0plWTN2aWlLMUl6aXNEYnJRT2pLQjAzVHFmZ291RWR1K0JLUU9iZ05FWjM2YwpFUzNGcVo1WThGZlJhOFgzUmFncXJCTXUwSkczc2VmbmJHK3VUWWp3RTJoaERwZXQ2STN6K3E5Y3JwUC95U24rCi9WTlFQSjhDZ1lBNXh2UnN3eEYwU016M2c3NHdvSEV0N2dwcmRLc1RMaStIV0NFRTlPVm4vUzVEc0hJc3hFZ2IKR1lSQkhvNTFldnY4Vm1xV1BISkU3emhzZ055TnphN1lnNGlUZVl5U04zTnM3VU5nRjN4bmx6ZThLdE5pVU1xZwo4S3dGekVTSHVKQzhJZWpDWlJ4OUhQK0w0cmViaTlqY2NzTHBQUUpucEQrcittQUVzc3o2Vnc9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo=
```

Take that content and store it somewhere. Then you can run the [example NGINX application](https://github.com/cloudify-incubator/cloudify-kubernetes-plugin/blob/master/examples/simple-example-blueprint.yaml).
