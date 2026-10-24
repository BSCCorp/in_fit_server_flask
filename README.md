in_fit_server_flask
===================

The API for the InFit Android application.

# Setup

Configure:

```
cp .env.example .env
```

# Development

Activate environment:

```
source .venv/bin/activate
```

## Formatting, delinting

Run checks:

```
ruff check .
ruff format --check .
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

Deployed to Ubuntu server:

```
sudo mkdir -p /opt/flask-infit-api
sudo chown "$USER":"$USER" /opt/flask-infit-api
```

Put the `docker-compose.prod.yml` and `.env` in the new directory:

```
/opt/flask-infit-api/
├── docker-compose.prod.yml
└── .env
```

`.env` needs to contain production secrets. Consult `.env.example`.

Protect the `.env` file:

```
chmod 600 /opt/flask-infit-api/.env
```

## GitHub Secrets

Create a key on the local machine:

```
ssh-keygen -t ed25519 -C "github-actions-flask-infit-api-deploy"                                                                                                                        ```

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

Add the private key to GitHub. Go to the repository:

**Settings → Secrets and variables → Actions → New repository secret**

Create:

```
Name:
SERVER_SSH_KEY
```

Then get your private key:

```
xclip -selection clipboard <  ~/.ssh/github-actions-flask-infit-api-deploy
```

Paste it into the GitHub secret.


Then add:

```
SERVER_HOST = 203.0.113.10
```

And,

```
SERVER_USER = deploy
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


Log Docker into GHCR on Ubuntu. On the server, run:

```
docker login ghcr.io
```

When prompted:

```
Username:
```

enter your GitHub username.

For:

```
Password:
```

paste the GitHub token.

You should get:

```
Login Succeeded
```

Then test:

```
docker pull ghcr.io/bsccorp/flask-infit-api:latest
```

and:

```
docker pull ghcr.io/bsccorp/flask-infit-api-web:latest
```

If both work, your authentication is set up.

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

`DEPLOY_KNOWN_HOSTS` is a GitHub Actions secret containing the SSH host key for the Ubuntu server. It lets GitHub Actions verify that it's connecting to the actual server when deploying, rather than an impostor.

On the server, execute:

```
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Retrieve the public host key:

```
sudo cat /etc/ssh/ssh_host_ed25519_key.pub
```

Format the key. The known_hosts file needs the hostname or IP address followed by the public host key.

For example, if the server is 203.0.113.10, the entry would look like:

```
203.0.113.10 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExamplePublicKeyData
```

#### Set Action Secrets

In the GitHub repository, open **Settings → Secrets and variables → Actions** and configure these repository or environment secrets:

- DEPLOY_HOST: Server hostname or IP address
- DEPLOY_USER: SSH deployment username
- DEPLOY_SSH_KEY: Private deployment key
- DEPLOY_KNOWN_HOSTS: Verified SSH host-key entry

## Require CI to pass before merging

In your GitHub repository:

1. Open **Settings → Rulesets.**
2. Create a branch ruleset targeting main.
3. Require pull requests before merging.
4. Require the status checks to pass.
5. Block force pushes and deletion of main.
6. Require review if your workflow calls for it.

This prevents ordinary changes from bypassing the automated checks.

The CI job is named `test`, so that is the status check to select.


