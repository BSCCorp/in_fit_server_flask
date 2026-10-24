"""Video file serving routes."""

from flask import Blueprint, current_app, send_from_directory

videos_bp = Blueprint("videos", __name__)


@videos_bp.route(
    "/videos/<path:filename>",
    methods=["GET", "HEAD"],
)
def serve_video(filename: str):
    """Serve video files, manifests, and thumbnails."""
    return send_from_directory(
        current_app.config["VIDEO_DIR"],
        filename,
        conditional=True,
    )
