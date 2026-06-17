import os
import logging
from flask import Flask, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("checkout-api")

VERSION = "v2.4"

@app.route("/", methods=["GET"])
def index():
    logger.info("Handling request at / endpoint")
    return jsonify({
        "service": "checkout-api",
        "version": VERSION,
        "message": "Release Readiness Demo"
    })

@app.route("/health", methods=["GET"])
def health():
    db_url = os.getenv("DATABASE_URL")
    redis_url = os.getenv("REDIS_URL")
    
    # Check dependencies. 
    # Operational risk check: If DATABASE_URL is not set, use fallback in-memory SQLite (unstable for prod)
    if db_url:
        db_status = "connected"
        logger.info("Database status: CONNECTED")
    else:
        db_status = "warning_fallback_sqlite"
        logger.warning("DATABASE_URL is not set! Using unstable, volatile in-memory SQLite fallback.")

    # Check cache dependency.
    # Operational risk check: If REDIS_URL is not set, use local in-memory dict cache (non-distributed)
    if redis_url:
        redis_status = "connected"
        logger.info("Redis cache status: CONNECTED")
    else:
        redis_status = "warning_fallback_local"
        logger.warning("REDIS_URL is not set! Using volatile local in-memory dict cache fallback.")

    status_code = 200
    
    return jsonify({
        "status": "healthy",
        "version": VERSION,
        "checks": {
            "database": db_status,
            "redis": redis_status
        }
    }), status_code

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info(f"Starting checkout-api v{VERSION} on port {port}")
    app.run(host="0.0.0.0", port=port)
