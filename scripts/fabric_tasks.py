from fabric.api import run, put
from cloudify.exceptions import NonRecoverableError
from cloudify import ctx
import os


def start_master_bmc(**kwargs):
    stable = run("curl -s https://storage.googleapis.com"
                 "/kubernetes-release/release/stable.txt")
    run("curl -LO https://storage.googleapis.com"
        "/kubernetes-release/release/{}"
        "/bin/linux/amd64/kubectl".format(stable))
    run("chmod +x kubectl")
    run("sudo setenforce 0")
    run("sudo systemctl disable firewalld")
    run("sudo systemctl stop firewalld")
    f = ctx.download_resource("resources/kube-deploy.tgz")
    put(f, "/tmp/kube-deploy.tgz")
    os.remove(f)
    run("rm -rf kube-deploy")
    run("tar xzf /tmp/kube-deploy.tgz")
    k8s_version = (kwargs['k8s_settings']['k8s_version']
                   if 'k8s_version' in kwargs['k8s_settings'] else 'v1.3.0')
    etcd_version = (kwargs['k8s_settings']['etcd_version']
                    if 'etcd_version' in kwargs['k8s_settings'] else '2.2.5')
    flannel_version = (kwargs['k8s_settings']['flannel_version']
                       if 'flannel_version' in kwargs['k8s_settings']
                       else 'v0.6.2')
    flannel_network = (kwargs['k8s_settings']['flannel_network']
                       if 'flannel_network' in kwargs['k8s_settings']
                       else '10.1.0.0/16')
    flannel_ipmasq = (kwargs['k8s_settings']['flannel_ipmasq']
                      if 'flannel_ipmasq' in kwargs['k8s_settings']
                      else 'true')
    flannel_backend = (kwargs['k8s_settings']['flannel_backend']
                       if 'flannel_backend' in kwargs['k8s_settings']
                       else 'udp')
    restart_policy = (kwargs['k8s_settings']['restart_policy']
                      if 'restart_policy' in kwargs['k8s_settings']
                      else 'unless-stopped')
    arch = (kwargs['k8s_settings']['arch']
            if 'arch' in kwargs['k8s_settings'] else 'amd64')
    net_interface = (kwargs['k8s_settings']['net_interface']
                     if 'net_interface' in kwargs['k8s_settings'] else 'eth0')

    cluster_args = ''
    cluster_args = (cluster_args + "--etcd-name {}".format(kwargs['etcd_name'])
                    if 'etcd_name' in kwargs else '')
    cluster_args = (cluster_args + "--etcd-initial-cluster {}".
                    format(kwargs['etcd_initial_cluster'])
                    if 'etcd_initial_cluster' in kwargs else '')
    cluster_args = (cluster_args + "--etcd-initial-cluster-state {}".
                    format(kwargs['etcd_initial_cluster_state'])
                    if 'etcd_initial_cluster_state' in kwargs else '')
    cluster_args = (cluster_args + "--etcd-initial-advertise-peer-urls {}".
                    format(kwargs['etcd_initial_advertise_peer_urls'])
                    if 'etcd_initial_advertise_peer_urls' in kwargs else '')
    cluster_args = (cluster_args + "--etcd-advertise-client-urls {}".
                    format(kwargs['etcd_advertise_client_urls'])
                    if 'etcd_initial_advertise_peer_urls' in kwargs else '')
    cluster_args = (cluster_args + "--etcd-listen-peer-urls {}".
                    format(kwargs['etcd_listen_peer_urls'])
                    if 'etcd_listen_peer_urls' in kwargs else '')
    cluster_args = (cluster_args + "--etcd-listen-client-urls {}".
                    format(kwargs['etcd_listen_client_urls'])
                    if 'etcd_listen_client_urls' in kwargs else '')

    run("cd kube-deploy/docker-multinode;sudo ./master.sh"
        " --k8s-version {}"
        " --etcd-version {}"
        " --flannel-version {}"
        " --flannel-network {}"
        " --flannel-ipmasq {}"
        " --flannel-backend {}"
        " --restart-policy {}"
        " --arch {}"
        " --net-interface {}"
        " {}".format(
            k8s_version,
            etcd_version,
            flannel_version,
            flannel_network,
            flannel_ipmasq,
            flannel_backend,
            restart_policy,
            arch,
            net_interface,
            cluster_args
            ))

def start_master(**kwargs):
    stable = run("curl -s https://storage.googleapis.com"
                 "/kubernetes-release/release/stable.txt")
    run("curl -LO https://storage.googleapis.com"
        "/kubernetes-release/release/{}"
        "/bin/linux/amd64/kubectl".format(stable))
    run("chmod +x kubectl")
    f = ctx.download_resource("resources/kube-deploy.tgz")
    put(f, "/tmp/kube-deploy.tgz")
    os.remove(f)
    run("rm -rf kube-deploy")
    run("tar xzf /tmp/kube-deploy.tgz")
    k8s_version = (kwargs['k8s_settings']['k8s_version']
                   if 'k8s_version' in kwargs['k8s_settings'] else 'v1.3.0')
    etcd_version = (kwargs['k8s_settings']['etcd_version']
                    if 'etcd_version' in kwargs['k8s_settings'] else '2.2.5')
    flannel_version = (kwargs['k8s_settings']['flannel_version']
                       if 'flannel_version' in kwargs['k8s_settings']
                       else 'v0.6.2')
    flannel_network = (kwargs['k8s_settings']['flannel_network']
                       if 'flannel_network' in kwargs['k8s_settings']
                       else '10.1.0.0/16')
    flannel_ipmasq = (kwargs['k8s_settings']['flannel_ipmasq']
                      if 'flannel_ipmasq' in kwargs['k8s_settings']
                      else 'true')
    flannel_backend = (kwargs['k8s_settings']['flannel_backend']
                       if 'flannel_backend' in kwargs['k8s_settings']
                       else 'udp')
    restart_policy = (kwargs['k8s_settings']['restart_policy']
                      if 'restart_policy' in kwargs['k8s_settings']
                      else 'unless-stopped')
    arch = (kwargs['k8s_settings']['arch']
            if 'arch' in kwargs['k8s_settings'] else 'amd64')
    net_interface = (kwargs['k8s_settings']['net_interface']
                     if 'net_interface' in kwargs['k8s_settings'] else 'eth0')

    cluster_args = ''
    cluster_args = (cluster_args + "--etcd-name {}".format(kwargs['etcd_name'])
                    if 'etcd_name' in kwargs else '')
    cluster_args = (cluster_args + "--etcd-initial-cluster {}".
                    format(kwargs['etcd_initial_cluster'])
                    if 'etcd_initial_cluster' in kwargs else '')
    cluster_args = (cluster_args + "--etcd-initial-cluster-state {}".
                    format(kwargs['etcd_initial_cluster_state'])
                    if 'etcd_initial_cluster_state' in kwargs else '')
    cluster_args = (cluster_args + "--etcd-initial-advertise-peer-urls {}".
                    format(kwargs['etcd_initial_advertise_peer_urls'])
                    if 'etcd_initial_advertise_peer_urls' in kwargs else '')
    cluster_args = (cluster_args + "--etcd-advertise-client-urls {}".
                    format(kwargs['etcd_advertise_client_urls'])
                    if 'etcd_initial_advertise_peer_urls' in kwargs else '')
    cluster_args = (cluster_args + "--etcd-listen-peer-urls {}".
                    format(kwargs['etcd_listen_peer_urls'])
                    if 'etcd_listen_peer_urls' in kwargs else '')
    cluster_args = (cluster_args + "--etcd-listen-client-urls {}".
                    format(kwargs['etcd_listen_client_urls'])
                    if 'etcd_listen_client_urls' in kwargs else '')

    run("cd kube-deploy/docker-multinode;sudo ./master.sh"
        " --k8s-version {}"
        " --etcd-version {}"
        " --flannel-version {}"
        " --flannel-network {}"
        " --flannel-ipmasq {}"
        " --flannel-backend {}"
        " --restart-policy {}"
        " --arch {}"
        " --net-interface {}"
        " {}".format(
            k8s_version,
            etcd_version,
            flannel_version,
            flannel_network,
            flannel_ipmasq,
            flannel_backend,
            restart_policy,
            arch,
            net_interface,
            cluster_args
            ))



def start_worker_bmc(**kwargs):
    run("sudo setenforce 0")
    run("sudo systemctl disable firewalld")
    run("sudo systemctl stop firewalld")
    run("rm -rf kube-deploy")
    f = ctx.download_resource("resources/kube-deploy.tgz")
    put(f, "/tmp/kube-deploy.tgz")
    run("tar xzf /tmp/kube-deploy.tgz")
    os.remove(f)

    if 'master_ip' not in kwargs or 'k8s_settings' not in kwargs:
        raise NonRecoverableError("master_ip and k8s_settings required")

    master_ip = kwargs['master_ip']
    k8s_version = (kwargs['k8s_settings']['k8s_version']
                   if 'k8s_version' in kwargs['k8s_settings'] else 'v1.3.0')
    etcd_version = (kwargs['k8s_settings']['etcd_version']
                    if 'etcd_version' in kwargs['k8s_settings'] else '2.2.5')
    flannel_version = (kwargs['k8s_settings']['flannel_version']
                       if 'flannel_version' in kwargs['k8s_settings']
                       else 'v0.6.2')
    flannel_network = (kwargs['k8s_settings']['flannel_network']
                       if 'flannel_network' in kwargs['k8s_settings']
                       else '10.1.0.0/16')
    flannel_ipmasq = (kwargs['k8s_settings']['flannel_ipmasq']
                      if 'flannel_ipmasq' in kwargs['k8s_settings']
                      else 'true')
    flannel_backend = (kwargs['k8s_settings']['flannel_backend']
                       if 'flannel_backend' in kwargs['k8s_settings']
                       else 'udp')
    restart_policy = (kwargs['k8s_settings']['restart_policy']
                      if 'restart_policy' in kwargs['k8s_settings']
                      else 'unless-stopped')
    arch = (kwargs['k8s_settings']['arch']
            if 'arch' in kwargs['k8s_settings'] else 'amd64')
    net_interface = (kwargs['k8s_settings']['net_interface']
                     if 'net_interface' in kwargs['k8s_settings'] else 'eth0')

    run("cd kube-deploy/docker-multinode;sudo ./worker.sh"
        " --master-ip {} "
        " --k8s-version {}"
        " --etcd-version {}"
        " --flannel-version {}"
        " --flannel-network {}"
        " --flannel-ipmasq {}"
        " --flannel-backend {}"
        " --restart-policy {}"
        " --arch {}"
        " --net-interface {}".format(
            master_ip,
            k8s_version,
            etcd_version,
            flannel_version,
            flannel_network,
            flannel_ipmasq,
            flannel_backend,
            restart_policy,
            arch,
            net_interface
            ))

def start_worker(**kwargs):
    run("rm -rf kube-deploy")
    f = ctx.download_resource("resources/kube-deploy.tgz")
    put(f, "/tmp/kube-deploy.tgz")
    run("tar xzf /tmp/kube-deploy.tgz")
    os.remove(f)

    if 'master_ip' not in kwargs or 'k8s_settings' not in kwargs:
        raise NonRecoverableError("master_ip and k8s_settings required")

    master_ip = kwargs['master_ip']
    k8s_version = (kwargs['k8s_settings']['k8s_version']
                   if 'k8s_version' in kwargs['k8s_settings'] else 'v1.3.0')
    etcd_version = (kwargs['k8s_settings']['etcd_version']
                    if 'etcd_version' in kwargs['k8s_settings'] else '2.2.5')
    flannel_version = (kwargs['k8s_settings']['flannel_version']
                       if 'flannel_version' in kwargs['k8s_settings']
                       else 'v0.6.2')
    flannel_network = (kwargs['k8s_settings']['flannel_network']
                       if 'flannel_network' in kwargs['k8s_settings']
                       else '10.1.0.0/16')
    flannel_ipmasq = (kwargs['k8s_settings']['flannel_ipmasq']
                      if 'flannel_ipmasq' in kwargs['k8s_settings']
                      else 'true')
    flannel_backend = (kwargs['k8s_settings']['flannel_backend']
                       if 'flannel_backend' in kwargs['k8s_settings']
                       else 'udp')
    restart_policy = (kwargs['k8s_settings']['restart_policy']
                      if 'restart_policy' in kwargs['k8s_settings']
                      else 'unless-stopped')
    arch = (kwargs['k8s_settings']['arch']
            if 'arch' in kwargs['k8s_settings'] else 'amd64')
    net_interface = (kwargs['k8s_settings']['net_interface']
                     if 'net_interface' in kwargs['k8s_settings'] else 'eth0')

    run("cd kube-deploy/docker-multinode;sudo ./worker.sh"
        " --master-ip {} "
        " --k8s-version {}"
        " --etcd-version {}"
        " --flannel-version {}"
        " --flannel-network {}"
        " --flannel-ipmasq {}"
        " --flannel-backend {}"
        " --restart-policy {}"
        " --arch {}"
        " --net-interface {}".format(
            master_ip,
            k8s_version,
            etcd_version,
            flannel_version,
            flannel_network,
            flannel_ipmasq,
            flannel_backend,
            restart_policy,
            arch,
            net_interface
            ))

