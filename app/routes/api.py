"""Routes migrated from the legacy Express API."""


from flask import Blueprint, abort, current_app, jsonify, request, send_from_directory

from app.data import KEYS, get_catalog

api_bp = Blueprint("api", __name__)


@api_bp.get("/")
def index():
    """Return the legacy video catalogue."""
    return jsonify(get_catalog(current_app.config["BASE_URL"]))


@api_bp.get("/key/<video_id>")
def get_key(video_id: str):
    """Return the Clear Key response for a video."""
    key = KEYS.get(video_id)

    if key is None:
        abort(404)

    return jsonify(
        {
            "keys": [
                {
                    "kty": "oct",
                    "k": key["k"],
                    "kid": key["kid"],
                }
            ],
            "type": "temporary",
        }
    )

@api_bp.post("/log")
def log_message():
    log_file = current_app.config["LOG_FILE"]

    payload = request.get_json(silent=True)

    if isinstance(payload, dict):
        message = payload.get("message")
    else:
        message = request.form.get("message")

    if not isinstance(message, str):
      return {"error": "A string 'message' field is required"}, 400

    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)

        with log_file.open("a", encoding="utf-8") as file:
            file.write(message + "\n")

    except OSError:
        current_app.logger.exception("Failed to append to log file")
        return {"error": "Failed to write log message"}, 400

    return "", 201

@api_bp.route("/videos/<path:filename>", methods=["GET", "HEAD"])
def serve_video(filename: str):
    """Serve video assets, including support for HTTP range requests."""
    return send_from_directory(
        current_app.config["VIDEO_DIR"],
        filename,
        conditional=True,
    )

