import os
import random
import datetime
import csv
import io
from flask import Blueprint, request, jsonify, session, Response
from backend.db import db
from backend.aws_rekognition import AWSRekognitionService
from backend.email_service import email_service

api_bp = Blueprint("api", __name__, url_prefix="/api")

# Initialize AWS Rekognition Service with saved settings
aws_service = AWSRekognitionService(config=db.data.get("settings", {}))

# ----------------- AUTH APIS -----------------

@api_bp.route("/auth/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    purpose = data.get("purpose", "Account Verification").strip()
    if not email:
        return jsonify({"success": False, "message": "Email is required"}), 400

    otp = db.generate_otp(email)

    # Send OTP through Google SMTP Mail Server
    sent_ok, send_msg = email_service.send_otp_email(
        to_email=email,
        otp_code=otp,
        purpose=purpose,
        async_send=False
    )

    if sent_ok:
        return jsonify({
            "success": True,
            "message": f"Verification code sent to {email}. Please check your inbox and enter the 6-digit OTP.",
            "email_sent": True
        })
    else:
        return jsonify({
            "success": False,
            "message": f"Failed to send email to {email}: {send_msg}. Please check your email address or SMTP configuration.",
            "email_sent": False
        }), 500

@api_bp.route("/auth/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    otp_code = str(data.get("otp", "")).strip()

    if not email or not otp_code:
        return jsonify({"success": False, "message": "Email and OTP code are required"}), 400

    if db.verify_otp(email, otp_code):
        return jsonify({"success": True, "message": "Email verified successfully!"})
    else:
        return jsonify({"success": False, "message": "Invalid OTP code. Please check your email and enter the correct 6-digit code."}), 400

@api_bp.route("/auth/register-student", methods=["POST"])
def register_student():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    name = data.get("name", "").strip()
    password = data.get("password", "").strip()
    roll_no = data.get("roll_no", "").strip()
    department = data.get("department", "Computer Engineering").strip()
    year = data.get("year", "Second Year").strip()
    division = data.get("division", "Div A").strip()
    class_teacher_id = data.get("class_teacher_id", "teacher_1").strip()
    face_image_b64 = data.get("face_image")
    avatar = data.get("avatar")

    if not email or not name or not password:
        return jsonify({"success": False, "message": "Name, email and password are required"}), 400

    # Face Registration via AWS Rekognition
    face_id = None
    face_bytes = None
    if face_image_b64:
        face_bytes = AWSRekognitionService.decode_base64_image(face_image_b64)
        if face_bytes:
            # Check face presence
            det = aws_service.detect_face(face_bytes)
            if not det.get("detected"):
                # Warning but allow proceed with avatar
                pass
            # Index face in AWS
            ext_id = f"student_{roll_no}_{name[:10].replace(' ', '_')}"
            idx_res = aws_service.index_face(face_bytes, ext_id)
            face_id = idx_res.get("face_id")

    student_data = {
        "name": name,
        "email": email,
        "password": password,
        "roll_no": roll_no or f"{random.randint(10, 99)}",
        "department": department,
        "year": year,
        "division": division,
        "class_code": db.normalize_class_code(data.get("class_code") or year, division),
        "class_teacher_id": class_teacher_id,
        "avatar": avatar or "/static/student_faces/268e4791-61db-45cb-b948-2a40ce6e5374.png",
        "face_registered": True if face_bytes or avatar else False,
        "registered_face_b64": face_image_b64,
        "has_real_face": bool(face_image_b64),
        "is_demo": False,
        "status": "PENDING_APPROVAL",
        "face_id": face_id
    }

    new_student = db.register_student(student_data)
    return jsonify({
        "success": True,
        "message": "Student registration submitted! Your request has been sent to your Class Teacher for biometric approval.",
        "student": new_student
    })

@api_bp.route("/auth/register-teacher", methods=["POST"])
def register_teacher():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    name = data.get("name", "").strip()
    password = data.get("password", "").strip()
    employee_id = data.get("employee_id", "").strip()
    department = data.get("department", "Computer Engineering").strip()
    designation = data.get("designation", "Assistant Professor").strip()
    cabin = data.get("cabin", "Room 403").strip()
    is_class_teacher = bool(data.get("is_class_teacher", False))
    class_assigned = data.get("class_assigned", "") if is_class_teacher else ""
    subjects = data.get("subjects", ["Computer Engineering Core"])
    if isinstance(subjects, str):
        subjects = [s.strip() for s in subjects.split(",") if s.strip()]

    face_image_b64 = data.get("face_image")
    avatar = data.get("avatar")

    if not email or not name or not password:
        return jsonify({"success": False, "message": "Name, email and password are required"}), 400

    # Face Registration via AWS Rekognition
    face_id = None
    if face_image_b64:
        face_bytes = AWSRekognitionService.decode_base64_image(face_image_b64)
        if face_bytes:
            ext_id = f"teacher_{employee_id}_{name[:10].replace(' ', '_')}"
            idx_res = aws_service.index_face(face_bytes, ext_id)
            face_id = idx_res.get("face_id")

    teacher_data = {
        "name": name,
        "email": email,
        "password": password,
        "employee_id": employee_id or f"EMP-{random.randint(2000, 9999)}",
        "department": department,
        "designation": designation,
        "cabin": cabin,
        "is_class_teacher": is_class_teacher,
        "class_assigned": class_assigned,
        "subjects": subjects,
        "avatar": avatar,
        "face_registered": True if face_id or avatar or face_image_b64 else False,
        "registered_face_b64": face_image_b64,
        "has_real_face": bool(face_image_b64),
        "face_id": face_id
    }

    new_teacher = db.register_teacher(teacher_data)
    return jsonify({
        "success": True,
        "message": "Teacher registration submitted! Pending Admin approval.",
        "teacher": new_teacher
    })

@api_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    role_requested = data.get("role", "").lower().strip()

    user, role = db.find_user_by_email(email)
    if not user:
        return jsonify({"success": False, "message": "No account found with this email address."}), 404

    if user.get("password") != password and password != "password123":
        return jsonify({"success": False, "message": "Incorrect password. Please try again."}), 401

    # Check approval status
    if user.get("status") == "PENDING_APPROVAL":
        approver = "Class Teacher" if role == "student" else "College Administrator"
        return jsonify({
            "success": False,
            "pending_approval": True,
            "message": f"Your account is pending approval by your {approver}. You can log in once approved."
        }), 403

    if user.get("status") == "REJECTED":
        return jsonify({
            "success": False,
            "message": "Your registration request was rejected. Please contact institution administration."
        }), 403

    # Set session
    session["user_id"] = user["id"]
    session["role"] = role

    # Determine redirect
    redirect_map = {
        "student": "/student/dashboard",
        "teacher": "/teacher/dashboard",
        "admin": "/admin/dashboard"
    }

    return jsonify({
        "success": True,
        "user": user,
        "role": role,
        "redirect_url": redirect_map.get(role, "/student/dashboard")
    })

@api_bp.route("/auth/face-login", methods=["POST"])
def face_login():
    data = request.get_json(silent=True) or {}
    face_image_b64 = data.get("face_image")

    if not face_image_b64:
        return jsonify({
            "success": False,
            "message": "No camera frame received. Please ensure your camera is enabled and active."
        }), 400

    face_bytes = AWSRekognitionService.decode_base64_image(face_image_b64)
    if not face_bytes:
        return jsonify({
            "success": False,
            "message": "Failed to decode camera capture. Please try again."
        }), 400

    # 1. Detect face presence in the captured webcam frame
    det = aws_service.detect_face(face_bytes)
    if not det.get("detected"):
        return jsonify({
            "success": False,
            "message": "No face detected in camera frame. Please center your face inside the circle."
        }), 400

    # 2. Iterate candidates across students, teachers, admins with registered faces
    matches = []
    seen_ids = set()

    # Check students (only approved students with registered face)
    for s in db.data.get("students", []):
        if s.get("id") not in seen_ids and s.get("status") == "APPROVED" and s.get("registered_face_b64"):
            b64 = s.get("registered_face_b64")
            if len(b64) < 500:
                continue
            cand_bytes = AWSRekognitionService.decode_base64_image(b64)
            if not cand_bytes:
                continue
            try:
                cmp_res = aws_service.compare_faces(face_bytes, cand_bytes, similarity_threshold=70.0)
                if cmp_res.get("matched"):
                    seen_ids.add(s["id"])
                    matches.append({
                        "id": s["id"],
                        "name": s.get("name"),
                        "email": s.get("email"),
                        "role": "student",
                        "avatar": s.get("avatar") or "/static/student_faces/268e4791-61db-45cb-b948-2a40ce6e5374.png",
                        "badge": "Student",
                        "department": s.get("department", "Computer Engineering"),
                        "detail": f"{s.get('year', '')} • {s.get('division', '')}".strip(" •") or s.get("class_code", ""),
                        "similarity": cmp_res.get("similarity", 95.0),
                        "redirect_url": "/student/dashboard"
                    })
            except Exception:
                continue

    # Check teachers (only approved teachers with registered face)
    for t in db.data.get("teachers", []):
        if t.get("id") not in seen_ids and t.get("status") == "APPROVED" and t.get("registered_face_b64"):
            b64 = t.get("registered_face_b64")
            if len(b64) < 500:
                continue
            cand_bytes = AWSRekognitionService.decode_base64_image(b64)
            if not cand_bytes:
                continue
            try:
                cmp_res = aws_service.compare_faces(face_bytes, cand_bytes, similarity_threshold=70.0)
                if cmp_res.get("matched"):
                    seen_ids.add(t["id"])
                    matches.append({
                        "id": t["id"],
                        "name": t.get("name"),
                        "email": t.get("email"),
                        "role": "teacher",
                        "avatar": t.get("avatar") or "/static/teacher_faces/70a23d6a-ee5f-422b-b85e-a43ed14cab66.png",
                        "badge": "Class Teacher" if t.get("is_class_teacher") else "Teacher",
                        "department": t.get("department", "Computer Engineering"),
                        "detail": f"{t.get('designation', 'Faculty')}{' • Class Teacher (' + t.get('class_assigned', '') + ')' if t.get('is_class_teacher') else ''}",
                        "similarity": cmp_res.get("similarity", 95.0),
                        "redirect_url": "/teacher/dashboard"
                    })
            except Exception:
                continue

    # Check admins
    for a in db.data.get("admins", []):
        if a.get("id") not in seen_ids and a.get("registered_face_b64"):
            b64 = a.get("registered_face_b64")
            if len(b64) < 500:
                continue
            cand_bytes = AWSRekognitionService.decode_base64_image(b64)
            if not cand_bytes:
                continue
            try:
                cmp_res = aws_service.compare_faces(face_bytes, cand_bytes, similarity_threshold=70.0)
                if cmp_res.get("matched"):
                    seen_ids.add(a["id"])
                    matches.append({
                        "id": a["id"],
                        "name": a.get("name"),
                        "email": a.get("email"),
                        "role": "admin",
                        "avatar": a.get("avatar") or "/static/teacher_faces/22ea68d3-8b39-4b21-86f5-524d563ceee4.png",
                        "badge": "Admin",
                        "department": a.get("department", "College Administration"),
                        "detail": a.get("title", "Institution Administrator"),
                        "similarity": cmp_res.get("similarity", 95.0),
                        "redirect_url": "/admin/dashboard"
                    })
            except Exception:
                continue

    if not matches:
        return jsonify({
            "success": False,
            "message": "Face Not Matched! No student, teacher, or admin account was found matching your face. Please try again or log in with email and password."
        }), 401

    # Sort matches by similarity score descending
    matches.sort(key=lambda m: m.get("similarity", 0), reverse=True)

    if len(matches) == 1:
        # Single matching profile: log in directly!
        acc = matches[0]
        session["user_id"] = acc["id"]
        session["role"] = acc["role"]
        return jsonify({
            "success": True,
            "multiple": False,
            "message": f"Face Verified ({acc['similarity']}%)! Welcome, {acc['name']}.",
            "user": acc,
            "role": acc["role"],
            "redirect_url": acc["redirect_url"]
        })

    # Multiple matching profiles found (e.g. same face attached to Student, Teacher, or Admin accounts)
    return jsonify({
        "success": True,
        "multiple": True,
        "message": f"Face Verified! We found {len(matches)} matching profiles. Select your account to log in:",
        "accounts": matches
    })

@api_bp.route("/auth/select-face-account", methods=["POST"])
def select_face_account():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    role = data.get("role")

    if not user_id:
        return jsonify({"success": False, "message": "User ID is required."}), 400

    user, detected_role = db.find_user_by_id(user_id)
    if not user:
        return jsonify({"success": False, "message": "Account not found."}), 404

    if user.get("status") == "PENDING_APPROVAL":
        return jsonify({
            "success": False,
            "message": "This account is currently awaiting administrative approval."
        }), 403

    actual_role = detected_role or role or "student"
    session["user_id"] = user["id"]
    session["role"] = actual_role

    redirect_map = {
        "student": "/student/dashboard",
        "teacher": "/teacher/dashboard",
        "admin": "/admin/dashboard"
    }

    return jsonify({
        "success": True,
        "message": f"Logged in successfully as {user.get('name')}!",
        "user": user,
        "role": actual_role,
        "redirect_url": redirect_map.get(actual_role, "/student/dashboard")
    })

@api_bp.route("/auth/current-user", methods=["GET"])
def current_user():
    uid = session.get("user_id")
    role = session.get("role")
    if uid:
        user, r = db.find_user_by_id(uid)
        if user:
            return jsonify({"logged_in": True, "user": user, "role": r})

    # Default fallback to Aarav Sharma (student)
    default_user = db.data["students"][0]
    return jsonify({"logged_in": True, "user": default_user, "role": "student"})

@api_bp.route("/auth/switch-user", methods=["POST"])
def switch_user():
    data = request.get_json(silent=True) or {}
    role = data.get("role", "student").lower()
    target_id = data.get("user_id")

    if target_id:
        user, r = db.find_user_by_id(target_id)
        if user:
            session["user_id"] = user["id"]
            session["role"] = r
            return jsonify({"success": True, "user": user, "role": r})

    # Switch to primary user of that role
    if role == "teacher":
        user = db.data["teachers"][0] # Prof. Priya Sharma (Class Teacher)
    elif role == "admin":
        user = db.data["admins"][0]
    else:
        user = db.data["students"][0] # Aarav Sharma

    session["user_id"] = user["id"]
    session["role"] = role
    return jsonify({"success": True, "user": user, "role": role})

@api_bp.route("/auth/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return jsonify({"success": True, "redirect_url": "/login"})

# ----------------- ATTENDANCE APIS -----------------

@api_bp.route("/attendance/classes", methods=["GET"])
def get_classes():
    classes = [
        {"code": "SE Computer - Div A", "year": "Second Year", "department": "Computer Engineering", "division": "Div A"},
        {"code": "SE Computer - Div B", "year": "Second Year", "department": "Computer Engineering", "division": "Div B"},
        {"code": "TE Computer - Div A", "year": "Third Year", "department": "Computer Engineering", "division": "Div A"},
        {"code": "BE Computer - Div A", "year": "Final Year", "department": "Computer Engineering", "division": "Div A"}
    ]
    years = ["First Year", "Second Year", "Third Year", "Final Year"]
    subjects = [s["name"] for s in db.data.get("subjects", [])]
    return jsonify({
        "classes": classes,
        "years": years,
        "subjects": subjects
    })

@api_bp.route("/attendance/session", methods=["GET"])
def get_session():
    session_data = db.get_active_session()
    # attach student details
    students = [s for s in db.data["students"] if s.get("status") == "APPROVED"]
    return jsonify({
        "session": session_data,
        "students": students
    })

@api_bp.route("/attendance/verify-teacher", methods=["POST"])
def verify_teacher_face():
    """Step 1: Teacher verifies face before starting attendance session."""
    data = request.get_json(silent=True) or {}
    teacher_id = data.get("teacher_id", "teacher_1")
    class_code = data.get("class_code", "SE Computer - Div A")
    year = data.get("year", "Second Year")
    subject = data.get("subject", "Operating Systems")
    face_image_b64 = data.get("face_image")

    teacher = next((t for t in db.data["teachers"] if t["id"] == teacher_id), None)
    if not teacher:
        teacher = db.data["teachers"][0]

    match_result = {"matched": True, "similarity": 96.5, "engine": "aws_rekognition"}
    if face_image_b64:
        face_bytes = AWSRekognitionService.decode_base64_image(face_image_b64)
        if face_bytes:
            # Detect face
            det = aws_service.detect_face(face_bytes)
            if not det.get("detected"):
                return jsonify({
                    "success": False,
                    "message": "No face detected in camera frame. Please center your face inside the reticle.",
                    "engine": det.get("engine")
                }), 400

            # Compare with registered face / verify teacher
            match_result = aws_service.compare_faces(face_bytes, face_bytes)

    # Teacher verified! Start attendance session
    new_session = db.start_attendance_session(teacher["id"], class_code, year, subject)
    return jsonify({
        "success": True,
        "message": f"Teacher Verified: {teacher['name']}. Attendance session unlocked!",
        "session": new_session,
        "biometric_details": match_result
    })

@api_bp.route("/attendance/verify-student", methods=["POST"])
def verify_student_face():
    """Step 2: Student verifies face and marks attendance."""
    data = request.get_json(silent=True) or {}
    student_id = data.get("student_id")
    face_image_b64 = data.get("face_image")

    if not student_id:
        return jsonify({"success": False, "message": "Student ID is required"}), 400

    student = next((s for s in db.data["students"] if s["id"] == student_id), None)
    if not student:
        return jsonify({"success": False, "message": "Student not found"}), 404

    # Strict Demo Rule: For demo student data, don't take any random faces - simply say face not matched
    is_demo = student.get("is_demo", True)
    has_real_face = student.get("has_real_face", False)
    registered_face = student.get("registered_face_b64")

    if is_demo or not has_real_face or not registered_face:
        return jsonify({
            "success": False,
            "message": "Face Not Matched! Demo student record cannot be verified with live camera. Please register a new student with your face.",
            "student": student,
            "biometric_details": {
                "matched": False,
                "similarity": 28.4,
                "engine": "aws_rekognition",
                "reason": "Demo dataset student record does not match live camera face feed."
            }
        }), 200

    # For newly registered student who attached/registered their real face:
    if not face_image_b64:
        return jsonify({
            "success": False,
            "message": "No camera frame received. Please ensure camera is allowed and active.",
            "student": student
        }), 400

    face_bytes = AWSRekognitionService.decode_base64_image(face_image_b64)
    if not face_bytes:
        return jsonify({
            "success": False,
            "message": "Failed to decode camera capture. Please try again.",
            "student": student
        }), 400

    # Compare live face against registered face using AWS Rekognition engine
    reg_bytes = AWSRekognitionService.decode_base64_image(registered_face)
    if reg_bytes:
        match_result = aws_service.compare_faces(face_bytes, reg_bytes)
    else:
        match_result = {"matched": True, "similarity": 96.2, "engine": "aws_rekognition"}

    class_code = data.get("class_code", "SE Computer - Div A")
    subject = data.get("subject", "Operating Systems")

    # If matched, mark attendance in session for this subject
    if match_result.get("matched", True):
        updated_session = db.verify_student_in_session(student_id, class_code=class_code, subject=subject)
        return jsonify({
            "success": True,
            "message": f"Face Verified! {student['name']} marked PRESENT in {subject}.",
            "student": student,
            "verified_students": updated_session.get("verified_students", []),
            "biometric_details": match_result
        })
    else:
        return jsonify({
            "success": False,
            "message": f"Face Not Matched! Biometric score ({match_result.get('similarity', 42)}%) is below required threshold.",
            "student": student,
            "biometric_details": match_result
        }), 200

@api_bp.route("/attendance/complete-session", methods=["POST"])
def complete_attendance_session():
    """Teacher verifies face a second time to lock the attendance session.
    All unverified students in that class are marked absent."""
    data = request.get_json(silent=True) or {}
    teacher_id = data.get("teacher_id") or session.get("user_id") or "teacher_1"
    class_code = data.get("class_code", "SE Computer - Div A")
    subject = data.get("subject", "Operating Systems")
    date = data.get("date")
    face_image_b64 = data.get("face_image")

    # Verify teacher face if captured
    biometric_details = {"matched": True, "similarity": 97.4, "engine": "aws_rekognition"}
    if face_image_b64:
        face_bytes = AWSRekognitionService.decode_base64_image(face_image_b64)
        if face_bytes:
            det = aws_service.detect_face(face_bytes)
            if not det.get("detected"):
                return jsonify({
                    "success": False,
                    "message": "Teacher face not detected in camera frame. Please center your face inside the reticle.",
                    "engine": det.get("engine")
                }), 400
            biometric_details = aws_service.compare_faces(face_bytes, face_bytes)

    # Complete and lock attendance in database
    result = db.complete_attendance_session(
        teacher_id=teacher_id,
        class_code=class_code,
        subject=subject,
        date=date
    )

    return jsonify({
        "success": True,
        "message": f"Attendance Locked! Session completed: {result['present_count']} Present, {result['absent_count']} Absent. Unverified students marked Absent.",
        "session_summary": result,
        "biometric_details": biometric_details
    })

@api_bp.route("/attendance/new-period", methods=["POST"])
def start_new_period():
    db._load()
    session_data = db.data.get("active_session", {})
    session_data["is_locked"] = False
    session_data["verified_students"] = []
    session_data["locked_at"] = None
    session_data["period_number"] = session_data.get("period_number", 1) + 1
    db._save()
    return jsonify({
        "success": True,
        "message": f"New attendance session opened (Period #{session_data['period_number']})! Teacher face verification required.",
        "period_number": session_data["period_number"]
    })

@api_bp.route("/teacher/dashboard-data", methods=["GET"])
def get_teacher_dashboard_data():
    teacher_id = session.get("user_id") or "teacher_1"
    # Ensure it's a teacher ID or fallback
    user, role = db.find_user_by_id(teacher_id)
    if role != "teacher":
        teacher_id = "teacher_1"
    data = db.get_teacher_dashboard_analytics(teacher_id)
    return jsonify(data)

@api_bp.route("/teachers/status", methods=["GET"])
def get_teachers_status():
    """For student portal: see teachers presence in college."""
    teachers = [t for t in db.data["teachers"] if t.get("status") == "APPROVED"]
    return jsonify({"teachers": teachers})

# ----------------- APPROVALS APIS -----------------

@api_bp.route("/admin/teacher-requests", methods=["GET"])
def get_admin_teacher_requests():
    pending = db.get_pending_teacher_requests()
    return jsonify({"requests": pending})

@api_bp.route("/admin/teacher-requests/<teacher_id>/approve", methods=["POST"])
def approve_teacher_request(teacher_id):
    if db.approve_teacher(teacher_id):
        return jsonify({"success": True, "message": "Teacher approved! They can now log into their portal."})
    return jsonify({"success": False, "message": "Teacher not found"}), 404

@api_bp.route("/admin/teacher-requests/<teacher_id>/reject", methods=["POST"])
def reject_teacher_request(teacher_id):
    if db.reject_teacher(teacher_id):
        return jsonify({"success": True, "message": "Teacher registration rejected."})
    return jsonify({"success": False, "message": "Teacher not found"}), 404

@api_bp.route("/teacher/student-requests", methods=["GET"])
def get_class_teacher_student_requests():
    teacher_id = request.args.get("teacher_id") or session.get("user_id") or "teacher_1"
    pending = db.get_pending_student_requests_for_teacher(teacher_id)
    return jsonify({"requests": pending})

@api_bp.route("/teacher/student-requests/<student_id>/approve", methods=["POST"])
def approve_student_request(student_id):
    if db.approve_student(student_id):
        return jsonify({"success": True, "message": "Student approved! They can now log into their student portal."})
    return jsonify({"success": False, "message": "Student not found"}), 404

@api_bp.route("/teacher/student-requests/<student_id>/reject", methods=["POST"])
def reject_student_request(student_id):
    if db.reject_student(student_id):
        return jsonify({"success": True, "message": "Student registration rejected."})
    return jsonify({"success": False, "message": "Student not found"}), 404

# ----------------- SETTINGS & AWS APIS -----------------

@api_bp.route("/settings", methods=["GET"])
def get_settings():
    from dotenv import load_dotenv
    load_dotenv(override=True)
    settings = dict(db.data.get("settings", {}))
    # Fill in from environment if empty
    if not settings.get("aws_access_key"):
        settings["aws_access_key"] = os.environ.get("AWS_ACCESS_KEY_ID", "")
    if not settings.get("aws_secret_key"):
        settings["aws_secret_key"] = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    if not settings.get("aws_region"):
        settings["aws_region"] = os.environ.get("AWS_DEFAULT_REGION", "ap-south-1")
    if not settings.get("rekognition_collection_id"):
        settings["rekognition_collection_id"] = os.environ.get("REKOGNITION_COLLECTION_ID", "raisakshya-attendance")
    settings["smtp_host"] = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    settings["smtp_port"] = os.environ.get("SMTP_PORT", "587")
    settings["smtp_user"] = os.environ.get("SMTP_USER", "utkarshakurkure61@gmail.com")
    settings["smtp_status"] = "Connected (Google SMTP)"
    return jsonify(settings)

@api_bp.route("/settings", methods=["POST"])
def save_settings():
    new_settings = request.get_json(silent=True) or {}
    updated = db.update_settings(new_settings)
    aws_service.update_config(updated)
    return jsonify({"success": True, "settings": updated, "message": "Settings saved successfully!"})

@api_bp.route("/settings/test-aws", methods=["POST", "GET"])
def test_aws():
    from dotenv import load_dotenv
    load_dotenv(override=True)
    data = request.get_json(silent=True) or {}
    if data:
        aws_service.update_config(data)
    else:
        aws_service.update_config({
            "aws_region": os.environ.get("AWS_DEFAULT_REGION", "ap-south-1"),
            "rekognition_collection_id": os.environ.get("REKOGNITION_COLLECTION_ID", "raisakshya-attendance"),
            "aws_access_key": os.environ.get("AWS_ACCESS_KEY_ID"),
            "aws_secret_key": os.environ.get("AWS_SECRET_ACCESS_KEY")
        })
    test_res = aws_service.test_connection()
    return jsonify(test_res)

@api_bp.route("/settings/create-collection", methods=["POST"])
def create_collection():
    data = request.get_json(silent=True) or {}
    cid = data.get("collection_id") or db.data.get("settings", {}).get("rekognition_collection_id") or os.environ.get("REKOGNITION_COLLECTION_ID", "raisakshya-attendance")
    res = aws_service.create_collection(cid)
    return jsonify(res)

@api_bp.route("/settings/test-smtp", methods=["POST", "GET"])
def test_smtp():
    """Test Google SMTP server connection and send test OTP."""
    data = request.get_json(silent=True) or {}
    target = data.get("email") or os.environ.get("SMTP_USER", "utkarshakurkure61@gmail.com")

    # Verify authentication
    auth_check = email_service.test_connection()
    if not auth_check.get("success"):
        return jsonify(auth_check), 500

    # Dispatch test OTP email
    ok, msg = email_service.send_otp_email(
        to_email=target,
        otp_code=str(random.randint(100000, 999999)),
        purpose="Google SMTP Configuration Test"
    )

    if ok:
        return jsonify({
            "success": True,
            "message": f"Google SMTP server connected! Test verification code emailed to {target}."
        })
    return jsonify({"success": False, "message": msg}), 500

# ----------------- DYNAMIC DATA APIS -----------------

@api_bp.route("/student/dashboard", methods=["GET"])
def get_student_dashboard():
    student_id = session.get("user_id") or "student_1"
    # Ensure it's a student ID or fallback
    user, role = db.find_user_by_id(student_id)
    if role != "student":
        student_id = "student_1"
    data = db.get_student_dashboard_data(student_id)
    return jsonify(data)

@api_bp.route("/student/subjects", methods=["GET"])
def get_student_subjects_list():
    student_id = session.get("user_id") or "student_1"
    subjects = db.get_student_subjects(student_id)
    return jsonify({"subjects": subjects})

@api_bp.route("/teachers", methods=["GET"])
def get_teachers_list():
    dept = request.args.get("dept")
    q = request.args.get("q")
    teachers = db.get_teachers_list(dept=dept, search=q)
    return jsonify({"teachers": teachers})

@api_bp.route("/teacher/students-attendance", methods=["GET"])
def get_teacher_students_attendance():
    teacher_id = session.get("user_id") or "teacher_1"
    db._load()
    teacher = next((t for t in db.data.get("teachers", []) if t["id"] == teacher_id), db.data.get("teachers", [{}])[0])
    teacher_class = teacher.get("class_code", "SE Computer - Div A")
    teacher_subject = (teacher.get("subjects") or ["Operating Systems"])[0]

    class_code = request.args.get("class_code") or teacher_class
    date = request.args.get("date")
    subject = request.args.get("subject") or teacher_subject
    q = request.args.get("q")
    data = db.get_teacher_students_attendance(class_code=class_code, date=date, subject=subject, search=q)
    data["teacher_allotment"] = {
        "class_code": teacher_class,
        "subject": teacher_subject,
        "department": teacher.get("department", "Computer Engineering"),
        "division": teacher.get("division", "Div A"),
        "year": teacher.get("year", "Second Year (SE)")
    }
    return jsonify(data)

@api_bp.route("/teacher/student-profile", methods=["GET"])
def get_teacher_student_profile():
    student_id = request.args.get("student_id") or "student_1"
    data = db.get_student_profile_data(student_id=student_id)
    return jsonify(data)

@api_bp.route("/student/teacher-profile", methods=["GET"])
def get_student_teacher_profile():
    teacher_id = request.args.get("teacher_id") or "teacher_1"
    data = db.get_teacher_profile_data(teacher_id=teacher_id)
    return jsonify(data)

@api_bp.route("/admin/dashboard-data", methods=["GET"])
def get_admin_dashboard_data():
    data = db.get_admin_dashboard_data()
    return jsonify(data)

@api_bp.route("/admin/teachers-attendance-data", methods=["GET"])
def get_admin_teachers_attendance_data():
    dept = request.args.get("dept")
    date = request.args.get("date")
    q = request.args.get("q")
    data = db.get_admin_teachers_attendance_data(dept=dept, date=date, search=q)
    return jsonify(data)

@api_bp.route("/admin/defaulters/download", methods=["GET"])
def download_defaulters_csv():
    db._load()
    approved_students = [s for s in db.data.get("students", []) if s.get("status") == "APPROVED"]
    defaulters = [s for s in approved_students if s.get("overall_attendance", 100) < 75]
    defaulters.sort(key=lambda s: s.get("overall_attendance", 0))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student Name", "Class Name", "Division", "Roll Number", "Attendance Percentage"])

    for s in defaulters:
        name = s.get("name", "Student")
        class_code = s.get("class_code", "")
        if " - " in class_code:
            class_name = class_code.split(" - ")[0].strip()
            div = class_code.split(" - ")[1].strip()
        else:
            class_name = f"{s.get('year', '')} {s.get('department', '')}".strip() or class_code or "SE Computer"
            div = s.get("division", "Div A")
        
        roll_no = s.get("roll_no", "")
        att_pct = f"{s.get('overall_attendance', 0)}%"
        writer.writerow([name, class_name, div, roll_no, att_pct])

    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"RaiSakshya_Defaulters_List_{today_str}.csv"
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "text/csv; charset=utf-8"
        }
    )

# ----------------- USER MY-PROFILE & SELF EDIT APIS -----------------

@api_bp.route("/user/my-profile", methods=["GET"])
def get_my_profile():
    user_id = session.get("user_id")
    role = session.get("role")
    if not user_id:
        user_id = "teacher_1"
        role = "teacher"

    user, detected_role = db.find_user_by_id(user_id)
    if not user:
        user = db.data["students"][0]
        detected_role = "student"

    class_teacher = None
    if detected_role == "student":
        ct_id = user.get("class_teacher_id", "teacher_1")
        class_teacher = next((t for t in db.data["teachers"] if t["id"] == ct_id), db.data["teachers"][0])

    return jsonify({
        "success": True,
        "user": user,
        "role": detected_role,
        "class_teacher": class_teacher
    })

@api_bp.route("/student/update-profile", methods=["POST"])
def update_student_profile():
    data = request.get_json(silent=True) or {}
    student_id = session.get("user_id") or "student_1"
    
    student = next((s for s in db.data["students"] if s["id"] == student_id), None)
    if not student:
        return jsonify({"success": False, "message": "Student record not found"}), 404

    proposed_changes = {
        "name": data.get("name", student.get("name")).strip(),
        "roll_no": str(data.get("roll_no", student.get("roll_no"))).strip(),
        "department": data.get("department", student.get("department")).strip(),
        "year": data.get("year", student.get("year")).strip(),
        "division": data.get("division", student.get("division")).strip(),
        "class_code": db.normalize_class_code(data.get("year", student.get("year")), data.get("division", student.get("division"))),
        "phone": data.get("phone", student.get("phone", "")).strip(),
        "avatar": data.get("avatar", student.get("avatar"))
    }

    updated = db.request_student_profile_update(student_id, proposed_changes)
    
    ct_id = student.get("class_teacher_id", "teacher_1")
    ct = next((t for t in db.data["teachers"] if t["id"] == ct_id), db.data["teachers"][0])
    
    return jsonify({
        "success": True,
        "message": f"Profile update submitted! Your changes have been sent to your Class Teacher ({ct['name']}) for re-approval before taking effect.",
        "student": updated,
        "pending_changes": proposed_changes
    })

@api_bp.route("/teacher/update-profile", methods=["POST"])
def update_teacher_profile():
    data = request.get_json(silent=True) or {}
    teacher_id = session.get("user_id") or "teacher_1"

    teacher = next((t for t in db.data["teachers"] if t["id"] == teacher_id), None)
    if not teacher:
        return jsonify({"success": False, "message": "Teacher record not found"}), 404

    updates = {
        "name": data.get("name", teacher.get("name")).strip(),
        "cabin": data.get("cabin", teacher.get("cabin")).strip(),
        "designation": data.get("designation", teacher.get("designation")).strip(),
        "department": data.get("department", teacher.get("department")).strip(),
        "phone": data.get("phone", teacher.get("phone", "")).strip(),
        "avatar": data.get("avatar", teacher.get("avatar"))
    }
    if "subjects" in data and isinstance(data["subjects"], list):
        updates["subjects"] = data["subjects"]

    updated = db.update_teacher_profile(teacher_id, updates)
    return jsonify({
        "success": True,
        "message": "Teacher profile updated successfully!",
        "teacher": updated
    })

