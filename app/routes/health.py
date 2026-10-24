from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health/live")
def liveness():
    return jsonify({"status": "ok"}), 200


@health_bp.get("/health/ready")
def readiness():
    # Add database and dependency checks here when applicable.
    return jsonify({"status": "ok"}), 200
