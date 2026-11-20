import os
import time
import socket
import sqlite3
import logging
import json
from flask import Flask, request, jsonify, render_template_string, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Configure Structured Logging
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "hostname": socket.gethostname()
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

logger = logging.getLogger("secureops-app")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__)

# Application Metadata
APP_VERSION = os.getenv("APP_VERSION", "v1.0.0")
APP_ENV = os.getenv("APP_ENV", "production")
HOSTNAME = socket.gethostname()
DB_FILE = os.getenv("DATABASE_PATH", "tasks.db")

# Prometheus Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status_code"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Latency in Seconds",
    ["endpoint"]
)

# Database Setup
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.before_request
def start_timer():
    request._start_time = time.time()

@app.after_request
def record_metrics(response):
    if hasattr(request, "_start_time"):
        latency = time.time() - request._start_time
        REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status_code=response.status_code
    ).inc()
    return response

# HTML Dashboard Template
HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureOps Delivery Platform</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
            --accent-green: #22c55e;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: var(--bg-color); color: var(--text-main); padding: 2rem; }
        .container { max-width: 900px; margin: 0 auto; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 1rem; margin-bottom: 2rem; }
        .logo { font-size: 1.5rem; font-weight: 700; color: var(--accent); }
        .badge { background: #0284c7; color: white; padding: 0.35rem 0.75rem; border-radius: 9999px; font-size: 0.85rem; font-weight: 600; }
        .badge-green { background: var(--accent-green); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
        .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem; }
        .card h4 { color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase; margin-bottom: 0.5rem; }
        .card p { font-size: 1.25rem; font-weight: 600; }
        .section-title { font-size: 1.2rem; margin-bottom: 1rem; color: var(--accent); }
        .table-container { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th, td { padding: 0.85rem 1.25rem; border-bottom: 1px solid var(--border); }
        th { background: #111827; color: var(--text-muted); font-size: 0.85rem; }
        .btn { background: var(--accent); color: #0f172a; border: none; padding: 0.5rem 1rem; border-radius: 6px; font-weight: 600; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text-main); margin-left: 0.5rem; }
        .form-row { display: flex; gap: 0.5rem; margin-top: 1rem; }
        input[type="text"] { flex: 1; padding: 0.6rem 1rem; background: #0f172a; border: 1px solid var(--border); color: white; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <div class="logo">🚀 SecureOps Automation Platform</div>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 0.25rem;">End-to-End GitOps, CI/CD, Containerization & Kubernetes Platform</p>
            </div>
            <div>
                <span class="badge badge-green">{{ env }}</span>
                <span class="badge">{{ version }}</span>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h4>Pod / Hostname</h4>
                <p style="font-family: monospace; font-size: 1rem;">{{ hostname }}</p>
            </div>
            <div class="card">
                <h4>Health Status</h4>
                <p style="color: var(--accent-green);">● Healthy (200 OK)</p>
            </div>
            <div class="card">
                <h4>Active Deployment</h4>
                <p>{{ version }}</p>
            </div>
            <div class="card">
                <h4>Observability</h4>
                <p><a href="/metrics" style="color: var(--accent); text-decoration: none;" target="_blank">View Prometheus &rarr;</a></p>
            </div>
        </div>

        <div class="card" style="margin-bottom: 2rem;">
            <div class="section-title">📝 Workload Task Manager</div>
            <p style="color: var(--text-muted); font-size: 0.9rem;">Stateful operational tasks stored in SQLite database to verify data persistence & readiness.</p>
            <form action="/api/v1/tasks" method="POST" class="form-row">
                <input type="text" name="title" placeholder="Enter new deployment or operational task..." required>
                <button type="submit" class="btn">+ Add Task</button>
            </form>
        </div>

        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Task Name</th>
                        <th>Status</th>
                        <th>Created At</th>
                    </tr>
                </thead>
                <tbody>
                    {% for task in tasks %}
                    <tr>
                        <td>#{{ task[0] }}</td>
                        <td>{{ task[1] }}</td>
                        <td><span class="badge badge-green">{{ task[2] }}</span></td>
                        <td style="color: var(--text-muted);">{{ task[3] }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="4" style="text-align: center; color: var(--text-muted); padding: 2rem;">No tasks recorded yet. Add one above!</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div style="margin-top: 2rem; display: flex; justify-content: space-between; align-items: center; color: var(--text-muted); font-size: 0.85rem;">
            <span>Endpoints: <a href="/health/live" style="color: var(--accent);">/health/live</a> | <a href="/health/ready" style="color: var(--accent);">/health/ready</a> | <a href="/metrics" style="color: var(--accent);">/metrics</a></span>
            <span>B.Tech Final Year Capstone Project</span>
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status, created_at FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    conn.close()
    return render_template_string(
        HTML_DASHBOARD,
        version=APP_VERSION,
        env=APP_ENV,
        hostname=HOSTNAME,
        tasks=tasks
    )

@app.route("/api/v1/tasks", methods=["GET", "POST"])
def manage_tasks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if request.method == "POST":
        title = request.form.get("title") or (request.json and request.json.get("title"))
        if not title:
            return jsonify({"error": "Task title is required"}), 400
        cursor.execute("INSERT INTO tasks (title, status) VALUES (?, ?)", (title, "Active"))
        conn.commit()
        conn.close()
        logger.info(f"Task created: {title}")
        if request.form:
            return home()
        return jsonify({"message": "Task created successfully", "title": title}), 201
    else:
        cursor.execute("SELECT id, title, status, created_at FROM tasks ORDER BY id DESC")
        tasks = [{"id": r[0], "title": r[1], "status": r[2], "created_at": r[3]} for r in cursor.fetchall()]
        conn.close()
        return jsonify({"tasks": tasks, "count": len(tasks)})

# Kubernetes Liveness Probe
@app.route("/health/live", methods=["GET"])
def liveness():
    return jsonify({
        "status": "UP",
        "probe": "liveness",
        "timestamp": time.time(),
        "hostname": HOSTNAME
    }), 200

# Kubernetes Readiness Probe (verifies database connectivity)
@app.route("/health/ready", methods=["GET"])
def readiness():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return jsonify({
            "status": "READY",
            "probe": "readiness",
            "database": "connected",
            "version": APP_VERSION
        }), 200
    except Exception as e:
        logger.error(f"Readiness probe failed: {str(e)}")
        return jsonify({"status": "DOWN", "error": str(e)}), 503

# CPU Load Simulator (Used to demonstrate Kubernetes Horizontal Pod Autoscaler HPA)
@app.route("/api/v1/simulate-load", methods=["POST", "GET"])
def simulate_load():
    duration = float(request.args.get("seconds", 2))
    start = time.time()
    while time.time() - start < duration:
        _ = [x * x for x in range(1000)]
    logger.info(f"Simulated CPU load for {duration} seconds")
    return jsonify({"message": f"Simulated CPU load for {duration}s", "hostname": HOSTNAME})

# Prometheus Metrics Exporter Endpoint
@app.route("/metrics", methods=["GET"])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    logger.info(f"Starting SecureOps Application v{APP_VERSION} on port 5000")
    app.run(host="0.0.0.0", port=5000)
