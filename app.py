import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, send_from_directory, redirect, url_for, request
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from backend.routes import api_bp

# EC2 and Server Network Configuration from .env
EC2_PUBLIC_IP = os.getenv("EC2_PUBLIC_IP", "3.110.208.141").strip()
HOST = os.getenv("HOST", "0.0.0.0").strip()
PORT = int(os.getenv("PORT", 5000))
ENABLE_HTTPS = os.getenv("ENABLE_HTTPS", "true").strip().lower() == "true"
SSL_CERT = os.getenv("SSL_CERT", "cert.pem").strip()
SSL_KEY = os.getenv("SSL_KEY", "key.pem").strip()

# Build dynamic allowed origins list from .env
raw_origins = os.getenv("ALLOWED_ORIGINS", "")
if "${EC2_PUBLIC_IP}" in raw_origins:
    raw_origins = raw_origins.replace("${EC2_PUBLIC_IP}", EC2_PUBLIC_IP)
if "$EC2_PUBLIC_IP" in raw_origins:
    raw_origins = raw_origins.replace("$EC2_PUBLIC_IP", EC2_PUBLIC_IP)
if "${PORT}" in raw_origins:
    raw_origins = raw_origins.replace("${PORT}", str(PORT))
if "$PORT" in raw_origins:
    raw_origins = raw_origins.replace("$PORT", str(PORT))
allowed_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

# Guarantee EC2 IP and standard development ports are present
for candidate in [
    f"http://{EC2_PUBLIC_IP}",
    f"http://{EC2_PUBLIC_IP}:{PORT}",
    f"https://{EC2_PUBLIC_IP}",
    f"https://{EC2_PUBLIC_IP}:{PORT}",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]:
    if candidate and candidate not in allowed_origins:
        allowed_origins.append(candidate)

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static"
)
app.secret_key = os.getenv("SECRET_KEY", "raisakshya_super_secret_session_key_2026")

# Enable ProxyFix so Flask recognizes EC2 reverse proxy headers (Nginx/ALB)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Session cookie settings friendly to EC2 HTTP & IP access
app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True
)

# Initialize Flask-CORS
allow_all = os.getenv("ALLOW_ALL_CORS", "true").lower() == "true"
CORS(
    app,
    resources={r"/*": {"origins": "*" if allow_all else allowed_origins}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
)

# Comprehensive CORS and Security Header Middleware
@app.after_request
def apply_cors_and_security_headers(response):
    origin = request.headers.get("Origin")
    if origin and (allow_all or origin in allowed_origins or EC2_PUBLIC_IP in origin):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept, Origin"
    elif allow_all:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept, Origin"
    return response

# Register API Blueprint
app.register_blueprint(api_bp)

# Root redirect to Login
@app.route("/")
def index():
    return redirect("/login")

# --- AUTH ROUTES ---
@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register/student")
def register_student_page():
    return render_template("register_student.html")

@app.route("/register/teacher")
def register_teacher_page():
    return render_template("register_teacher.html")

# --- STUDENT PORTAL ROUTES ---
@app.route("/student/dashboard")
def student_dashboard():
    return render_template("student_dashboard.html")

@app.route("/student/teachers")
def student_teachers():
    return render_template("student_teachers.html")

@app.route("/student/teacher-profile")
def student_teacher_profile():
    return render_template("student_teacher_profile.html")

@app.route("/student/profile")
def student_my_profile():
    return render_template("student_my_profile.html")

@app.route("/student/subjects")
def student_subjects():
    return render_template("student_subject.html")

# --- TEACHER PORTAL ROUTES ---
@app.route("/teacher/dashboard")
def teacher_dashboard():
    return render_template("teacher_dashboard.html")

@app.route("/teacher/take-attendance")
def teacher_take_attendance():
    return render_template("teacher_take_attendance.html")

@app.route("/teacher/students")
@app.route("/teacher/daily-attendance")
def teacher_daily_attendance():
    return render_template("teacher_attendance_specific_day.html")

@app.route("/teacher/all-days")
def teacher_all_days():
    return render_template("teacher_students_all_days.html")

@app.route("/teacher/student-profile")
def teacher_student_profile():
    return render_template("teacher_student_profile.html")

@app.route("/teacher/student-requests")
def teacher_student_requests():
    return render_template("teacher_student_requests.html")

@app.route("/teacher/profile")
def teacher_my_profile():
    return render_template("teacher_my_profile.html")

# --- ADMIN PORTAL ROUTES ---
@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/admin/teachers")
@app.route("/admin/teachers-attendance")
def admin_teachers_attendance():
    return render_template("admin_teachers_attendance.html")

@app.route("/admin/teacher-requests")
def admin_teacher_requests():
    return redirect("/admin/teachers")

@app.route("/admin/settings")
def admin_settings():
    return render_template("admin_settings.html")

if __name__ == "__main__":
    ssl_context = None
    scheme = "http"
    if ENABLE_HTTPS:
        # Check if certificate and key exist, or generate them automatically
        if not (os.path.exists(SSL_CERT) and os.path.exists(SSL_KEY)):
            try:
                from scripts.generate_ssl import generate_self_signed_cert
                generate_self_signed_cert(cert_path=SSL_CERT, key_path=SSL_KEY, ip_address=EC2_PUBLIC_IP)
            except Exception as e:
                print(f"[!] Could not auto-generate SSL certificate: {e}")

        if os.path.exists(SSL_CERT) and os.path.exists(SSL_KEY):
            ssl_context = (SSL_CERT, SSL_KEY)
            scheme = "https"

    print("=" * 60)
    print(" RaiSakshya Smart Attendance Intelligence System")
    print(f" Server starting on: {scheme}://{HOST}:{PORT}")
    if EC2_PUBLIC_IP:
        print(f" Public EC2 Access: {scheme}://{EC2_PUBLIC_IP}:{PORT}")
    if ssl_context:
        print(" [SSL/HTTPS Active] WebRTC MediaDevices & Camera Enabled!")
        print(f" Browser Tip: Click 'Advanced' -> 'Proceed to {EC2_PUBLIC_IP}' to accept cert.")
    else:
        print(" [HTTP Mode] Set ENABLE_HTTPS=true in .env to enable SSL & Camera.")
    print("=" * 60)

    if ssl_context:
        app.run(host=HOST, port=PORT, ssl_context=ssl_context, debug=True)
    else:
        app.run(host=HOST, port=PORT, debug=True)

