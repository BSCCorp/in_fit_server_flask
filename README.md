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

# Production

Deployed to Ubuntu server:

```
sudo mkdir -p /opt/flask-api
sudo chown "$USER":"$USER" /opt/flask-api
```

Create /opt/flask-api/app.env:

```
SECRET_KEY=replace-with-a-cryptographically-random-secret
```

Protect the file:

```
chmod 600 /opt/flask-api/app.env
```

## Automate deployment over SSH

The deployment should occur only after the tests pass and the image is published.

A straightforward setup is:

1. GitHub Actions builds and publishes the image.
2. GitHub Actions connects to your Ubuntu server over SSH.
3. The server pulls the exact image associated with the commit.
4. Docker Compose starts the new container.
5. A health check confirms the application is responding.
6. If deployment fails, the previous image is restored.

### Prepare SSH access

Create a dedicated deployment SSH key pair. Add its public key to the deployment user's `~/.ssh/authorized_keys` on the Ubuntu server.

In your GitHub repository, open **Settings → Secrets and variables → Actions** and configure these repository or environment secrets:

- DEPLOY_HOST: Server hostname or IP address
- DEPLOY_USER: SSH deployment username
- DEPLOY_SSH_KEY: Private deployment key
- DEPLOY_KNOWN_HOSTS: Verified SSH host-key entry

