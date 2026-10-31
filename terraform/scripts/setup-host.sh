#!/bin/bash

set -euxo pipefail

# Log output for troubleshooting.
exec > >(tee -a /var/log/user-data.log) 2>&1

# Update packages.
apt-get update
apt-get install -y ca-certificates curl

# Configure Docker's official repository.
install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc

chmod a+r /etc/apt/keyrings/docker.asc

. /etc/os-release

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $${VERSION_CODENAME} stable" \
  > /etc/apt/sources.list.d/docker.list

# Install Docker Engine and Docker Compose.
apt-get update

apt-get install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin

# Start Docker automatically at boot.
systemctl enable --now docker

# Allow the default Ubuntu user to use Docker.
usermod -aG docker ubuntu

echo "Docker installation completed successfully."

# Create the application directories.
mkdir -p /opt/flask-infit-api/videos

# Set ownership to the Ubuntu user.
chown -R ubuntu:ubuntu /opt/flask-infit-api

echo "Application directories created successfully."

#
# Configure SSH access for administration and deployment.
#

# Ensure the Ubuntu user's SSH directory exists.
install -d -m 700 -o ubuntu -g ubuntu /home/ubuntu/.ssh

# Create authorized_keys if it doesn't exist.
touch /home/ubuntu/.ssh/authorized_keys

# Add public key without removing existing authorized keys.
cat <<'SSH_KEYS' >> /home/ubuntu/.ssh/authorized_keys
${admin_public_key}
SSH_KEYS

# Set correct ownership and permissions.
chown ubuntu:ubuntu /home/ubuntu/.ssh/authorized_keys
chmod 600 /home/ubuntu/.ssh/authorized_keys

echo "SSH access for administration and deployment configured."
