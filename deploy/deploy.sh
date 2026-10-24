#!/usr/bin/env bash

set -Eeuo pipefail

APP_DIR="/opt/flask-infit-api"
COMPOSE_FILE="${APP_DIR}/docker-compose.prod.yml"
CURRENT_IMAGE_FILE="${APP_DIR}/current-image"

NEW_IMAGE="${1:?Usage: deploy.sh <image-reference>}"

cd "$APP_DIR"

if [[ ! -f "$COMPOSE_FILE" ]]; then
    echo "Production Compose file not found."
    exit 1
fi

PREVIOUS_IMAGE=""

if [[ -f "$CURRENT_IMAGE_FILE" ]]; then
    PREVIOUS_IMAGE="$(cat "$CURRENT_IMAGE_FILE")"
fi

export IMAGE_REF="$NEW_IMAGE"

rollback() {
    echo "Deployment failed; attempting rollback."

    if [[ -n "$PREVIOUS_IMAGE" ]]; then
        export IMAGE_REF="$PREVIOUS_IMAGE"

        if docker compose -f "$COMPOSE_FILE" up -d; then
            echo "Previous image restored."
        else
            echo "WARNING: Automatic rollback failed."
        fi
    else
        docker compose -f "$COMPOSE_FILE" down || true
        echo "No previous image was recorded."
    fi
}

docker pull "$NEW_IMAGE"

if ! docker compose -f "$COMPOSE_FILE" up -d; then
    rollback
    exit 1
fi

HEALTHY=false

for attempt in $(seq 1 30); do
    STATUS="$(
        docker inspect \
            --format '{{.State.Health.Status}}' \
            flask-infit-api 2>/dev/null || true
    )"

    if [[ "$STATUS" == "healthy" ]]; then
        HEALTHY=true
        break
    fi

    sleep 2
done

if [[ "$HEALTHY" != "true" ]]; then
    docker compose -f "$COMPOSE_FILE" logs --tail=100 || true
    rollback
    exit 1
fi

printf '%s\n' "$NEW_IMAGE" > "${CURRENT_IMAGE_FILE}.tmp"
mv "${CURRENT_IMAGE_FILE}.tmp" "$CURRENT_IMAGE_FILE"

echo "Deployment successful: $NEW_IMAGE"

