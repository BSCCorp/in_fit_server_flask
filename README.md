in_fit_server_flask
===================

The API for the InFit Android application.

# Setup

Configure:

```
cp .env.example .env
```

Activate environment:

```
source .venv/bin/activate
```

Install dependencies:

```
pip install -e ".[dev]"
```

# Test

```
pytest --cov=app --cov-report=term-missing
```

# Development

Run server:

```
flask --app app run --debug
```


## Formatting, delinting

Run checks:

```
ruff check .
ruff format --check .
ruff check --fix .
mypy
pytest --cov=app --cov-branch --cov-report=term-missing
```

## Local Docker

```
docker compose up --build -d
```

Test the endpoints:

```
curl -i http://127.0.0.1:8000/health/live
curl -i http://127.0.0.1:8000/health/ready
```

# Production

Deploy to AWS

## Install Terraform

Add HashiCorp's signing key:

```
wget -O- https://apt.releases.hashicorp.com/gpg \
  | sudo gpg --dearmor \
  -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
```

Add repository:

```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/hashicorp.list
```

Install:

```
sudo apt update
sudo apt install -y terraform
```

## Install AWS CLI

Architecture dependent:

```
uname -r
```

Download installer:

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" \
  -o "awscliv2.zip"
```

Extract:

```
unzip awscliv2.zip
```

Execute:

```
sudo ./aws/install
```

### AWS Credentials

Open the AWS Console and go to the IAM dashboard.

1. Create a user. E.g., `terraform-dev`
2. Go to _Security Credentials_ -> _Create access key_
3. Copy access key to a secure location

Configure credentials:

```
aws configure --profile terraform-dev
```

Enter the access key ID, secret access key, default region (for example, us-west-2), and output format (json).

Verify:

```
aws sts get-caller-identity --profile terraform-dev
```

## Setup Terraform for AWS

Create a key pair:

```
ssh-keygen -t ed25519 -f ~/.ssh/flask-terraform -C "flask-terraform"
```

Get public IP:

```
curl -4 https://checkip.amazonaws.com
```

Configure:

```
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

## Test Terraform with AWS

Initialize:

```
cd terraform
terraform init
terraform fmt
terraform validate
```

Try this as well:

```
terraform plan
```

If this checks out:

```
terraform apply
```

Get instance details:

```
terraform output
```

Get `ssh` command:

```
terraform output -raw ssh_command
```






Protect the `.env` file:

```
chmod 600 /opt/flask-infit-api/.env
```

Upload videos:

```
rsync -a --progress --delete --update ./videos app@api.0yy.ca:/opt/flask-infit-api
```

## GitHub Secrets

### Application Configuration

For creating a `.env` on the EC2 instance.

In the GitHub repository:

1. Go to **Settings → Environments → production**.
2. Under Environment variables, add and set these variables:

```
VIRTUAL_HOST
LETSENCRYPT_EMAIL
BASE_URL
TITLE
```

### Actions SSH

Create a key on the local machine:

```
ssh-keygen -t ed25519 \
  -C "github-actions-flask-deploy" \
  -f ~/.ssh/flask-deploy \
  -N ""
```

This creates two files:

- `~/.ssh/flask-deploy` — private key.
- `~/.ssh/flask-deploy.pub` — public key.

The private key will be used by GitHub Actions. The public key will be installed on EC2.

#### Add the private key to GitHub Actions

Copy the private key to the clipboard:

```
xclip -selection clipboard <  ~/.ssh/flask-deploy
```

In the GitHub repository, navigate to:

**Settings → Environments → production → Environment secrets**

Create or update this secret with the private key:

```
DEPLOY_SSH_KEY
```

Then add:

```
SERVER_USER = ubuntu
SERVER_HOST = ec2.0yy.ca
```

`ubuntu` is the default user provided on EC2 instantiation. The server host DNS needs to be configured after Amazon spits out an IP address.

#### Add the public key to `terraform.tsvars`

Copy the public key to the clipboard:

```
xclip -selection clipboard <  ~/.ssh/flask-deploy.pub
```

Paste the value `terraform.tsvars`. E.g.:

```
github_actions_public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... github-actions-flask-deploy"
```

## Create a GitHub token for the server

Go to GitHub:

**Settings → Developer settings → Personal access tokens → Tokens (classic)**

Create a classic token with:

```
read:packages
```

You only need package read access for the server.

Don't use the GitHub Actions SSH key for this—this is a separate credential.


### Set environment variables

The access token is sensitive. We don't want anything sensitive falling into a `*.tfstate` file or similar.

From the Terraform directory, run:

```
export TF_VAR_ghcr_username="your-github-username"
export TF_VAR_ghcr_token="your-github-token"
```

Terraform automatically recognizes these variables.

### Run Terraform

When it comes time to provision the resources, execute:

```
terraform init
terraform plan
terraform apply
```

### Remove the environment variables afterward

When everything is deployed, smoke the exported variables.

```
unset TF_VAR_ghcr_username
unset TF_VAR_ghcr_token
```

## Automate deployment over SSH

The deployment occurs only after the tests pass and the image is published.

Basic workflow:

1. GitHub Actions builds and publishes the image.
2. GitHub Actions connects to the Ubuntu server over SSH.
3. The server pulls the exact image associated with the commit.
4. Docker Compose starts the new container.
5. A health check confirms the application is responding.
6. If deployment fails, the previous image is restored.

### Prepare SSH access

#### `DEPLOY_SSH_KEY`

Create a dedicated deployment SSH key pair.

```
ssh-keygen -t ed25519 -C "github-actions-flask-infit-api-deploy"
```

When prompted, name it:

```
~/.ssh/github-actions-flask-infit-api-deploy
```

Copy the public key to the clipboard:

```
xclip -selection clipboard <  ~/.ssh/github-actions-flask-infit-api-deploy.pub
```

Login to the host machine:

```
vim ~/.ssh/authorized_keys
```

Paste the public key as one line.

Test the key from the local machine:

```
ssh -i ~/.ssh/github-actions-flask-infit-api-deploy deploy@YOUR_SERVER_IP
```

This will provide the value for the `DEPLOY_SSH_KEY` Action value.

#### `DEPLOY_KNOWN_HOSTS`

`DEPLOY_KNOWN_HOSTS` is a GitHub Actions secret containing the SSH host key for the Ubuntu server. It lets GitHub Actions verify that it's connecting to the actual server when deploying, rather than an impostor. This requires logging into the EC2 instance.

On the server, retrieve the public host key:

```
sudo cat /etc/ssh/ssh_host_ed25519_key.pub
```

Format the key. The `known_hosts` file needs the hostname or IP address followed by the public host key.


For example, if the server is 3.150.24.167, the entry would look like:

```
3.150.24.167 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExamplePublicKeyData
```

Paste this value into the `DEPLOY_KNOWN_HOSTS` secret.


## Deploy via push

```
git push
```

