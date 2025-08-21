#!/bin/bash

# EKS Bootstrap
/etc/eks/bootstrap.sh example-eks-cluster

# Wait for initial setup
sleep 30

# Stop containerd
systemctl stop containerd

# Backup original binary
mv /usr/bin/containerd /usr/bin/containerd.bak

# Download and install containerd 2.0.5
cd /tmp
wget https://github.com/containerd/containerd/releases/download/v2.0.5/containerd-2.0.5-linux-amd64.tar.gz
tar -xzf containerd-2.0.5-linux-amd64.tar.gz
cp bin/containerd /usr/bin/containerd
chmod +x /usr/bin/containerd

# Restart services
systemctl start containerd
systemctl restart kubelet

# Log success
echo "containerd 2.0.5 installed successfully" >> /var/log/containerd-upgrade.log
containerd --version >> /var/log/containerd-upgrade.log