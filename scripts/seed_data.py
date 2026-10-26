import json
import os

data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "app_data.json")

# 17 avatars available
student_avatars = [
    "/static/student_faces/268e4791-61db-45cb-b948-2a40ce6e5374.png",
    "/static/student_faces/29bac66d-53a6-427f-ad43-218c61800bd0.png",
    "/static/student_faces/2ac23b8c-d2b7-488e-8d82-857ac5bd303f.png",
    "/static/student_faces/3a22b1b0-99d8-41c1-95df-f95875b8e106.png",
    "/static/student_faces/3c5d25d1-efa0-4b65-b75c-c0183af3b6bb.png",
    "/static/student_faces/6712253c-b43e-4ac7-9fd6-01af9b0832b4.png",
    "/static/student_faces/78b0db68-c0f1-4716-abee-5015a092e16f.png",
    "/static/student_faces/8f5264db-09a9-4ca1-9a76-dfc527fe9962.png",
    "/static/student_faces/9536da0a-9542-45fa-954a-672668592846.png"
]

teacher_avatars = [
    "/static/teacher_faces/20bb28b4-f54a-4a3c-9630-e75ad391e672.png",
    "/static/teacher_faces/22ea68d3-8b39-4b21-86f5-524d563ceee4.png",
    "/static/teacher_faces/308cb046-f220-4dba-a871-63cdef5a258c.png",
    "/static/teacher_faces/33768a7e-c518-4ba6-bc46-b6cc06c36aa5.png",
    "/static/teacher_faces/70a23d6a-ee5f-422b-b85e-a43ed14cab66.png",
    "/static/teacher_faces/9dbcd861-2ee5-4022-a40b-b36af3d8f553.png",
    "/static/teacher_faces/aaa3d5cf-fec2-4f08-ad68-c02cc114500b.png",
    "/static/teacher_faces/c3cde75f-4cea-4624-9e4c-d235c397916c.png"
]

settings = {
    "institution_name": "RaiSakshya College of Engineering",
    "academic_year": "2026 - 2027",
    "address": "Campus Ground, Sector 4, Nashik, MH, India",
    "timezone": "(GMT+05:30) India Standard Time",
    "biometric_threshold": 80,
    "aws_region": "ap-south-1",
    "rekognition_collection_id": "raisakshya-attendance",
    "aws_access_key": os.getenv("AWS_ACCESS_KEY_ID", ""),
    "aws_secret_key": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
    "allow_manual_attendance": True,
    "require_face_verification": True,
    "auto_mark_absent": True,
    "attendance_window_from": "08:30 AM",
    "attendance_window_to": "10:30 AM"
}

admins = [
    {
        "id": "admin_1",
        "name": "Dr. Rajesh Kulkarni",
        "email": "admin@college.edu",
        "password": "password123",
        "designation": "Principal & Dean",
        "avatar": teacher_avatars[7]
    }
]

teachers = [
    {
        "id": "teacher_1",
        "name": "Prof. Priya Sharma",
        "email": "priya.sharma@college.edu",
        "password": "password123",
        "employee_id": "EMP-3041",
        "department": "Computer Engineering",
        "designation": "Assistant Professor",
        "cabin": "Room 401 - IT Block",
        "status_college": "PRESENT",
        "check_in_time": "08:45 AM",
        "attendance_rate": 96,
        "is_class_teacher": True,
        "class_assigned": "SE Computer - Div A",
        "subjects": ["Operating Systems", "Computer Networks"],
        "avatar": teacher_avatars[0],
        "face_registered": True,
        "status": "APPROVED",
        "created_at": "2026-08-10"
    },
    {
        "id": "teacher_2",
        "name": "Prof. Rajesh Verma",
        "email": "rajesh.verma@college.edu",
        "password": "password123",
        "employee_id": "EMP-2105",
        "department": "Computer Engineering",
        "designation": "Associate Professor",
        "cabin": "Room 402 - Main Wing",
        "status_college": "PRESENT",
        "check_in_time": "09:05 AM",
        "attendance_rate": 92,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Data Structures"],
        "avatar": teacher_avatars[1],
        "face_registered": True,
        "status": "APPROVED",
        "created_at": "2026-08-10"
    },
    {
        "id": "teacher_3",
        "name": "Dr. Ananya Iyer",
        "email": "ananya.iyer@college.edu",
        "password": "password123",
        "employee_id": "EMP-1089",
        "department": "Computer Engineering",
        "designation": "Head of Department",
        "cabin": "Lab 3B - AI Center",
        "status_college": "PRESENT",
        "check_in_time": "08:30 AM",
        "attendance_rate": 98,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Database Management"],
        "avatar": teacher_avatars[2],
        "face_registered": True,
        "status": "APPROVED",
        "created_at": "2026-08-10"
    },
    {
        "id": "teacher_4",
        "name": "Prof. Sameer Deshmukh",
        "email": "sameer.d@college.edu",
        "password": "password123",
        "employee_id": "EMP-4102",
        "department": "Computer Engineering",
        "designation": "Assistant Professor",
        "cabin": "Room 405 - North Block",
        "status_college": "ABSENT",
        "check_in_time": "--",
        "attendance_rate": 78,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Computer Networks"],
        "avatar": teacher_avatars[3],
        "face_registered": True,
        "status": "APPROVED",
        "created_at": "2026-08-10"
    },
    {
        "id": "teacher_5",
        "name": "Prof. Kavita Nair",
        "email": "kavita.nair@college.edu",
        "password": "password123",
        "employee_id": "EMP-3890",
        "department": "Computer Engineering",
        "designation": "Lecturer",
        "cabin": "Room 410 - South Wing",
        "status_college": "PRESENT",
        "check_in_time": "09:15 AM",
        "attendance_rate": 94,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Software Engineering"],
        "avatar": teacher_avatars[4],
        "face_registered": True,
        "status": "APPROVED",
        "created_at": "2026-08-10"
    },
    {
        "id": "teacher_6",
        "name": "Prof. Amit Patil",
        "email": "amit.patil@college.edu",
        "password": "password123",
        "employee_id": "EMP-3011",
        "department": "Computer Engineering",
        "designation": "Assistant Professor",
        "cabin": "Room 412 - IT Block",
        "status_college": "PRESENT",
        "check_in_time": "08:45 AM",
        "attendance_rate": 95,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Computer Networks"],
        "avatar": teacher_avatars[0],
        "face_registered": True,
        "status": "APPROVED",
        "created_at": "2026-08-10"
    },
    {
        "id": "teacher_7",
        "name": "Prof. Neha Joshi",
        "email": "neha.joshi@college.edu",
        "password": "password123",
        "employee_id": "EMP-3012",
        "department": "Computer Engineering",
        "designation": "Assistant Professor",
        "cabin": "Room 414 - Tech Block",
        "status_college": "ABSENT",
        "check_in_time": "--",
        "attendance_rate": 88,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Database Management"],
        "avatar": teacher_avatars[1],
        "face_registered": True,
        "status": "APPROVED",
        "created_at": "2026-08-10"
    },
    {
        "id": "teacher_8",
        "name": "Prof. Vikram Sane",
        "email": "vikram.sane@college.edu",
        "password": "password123",
        "employee_id": "EMP-3013",
        "department": "Computer Engineering",
        "designation": "Associate Professor",
        "cabin": "Room 416 - Main Wing",
        "status_college": "PRESENT",
        "check_in_time": "08:50 AM",
        "attendance_rate": 92,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Operating Systems"],
        "avatar": teacher_avatars[2],
        "face_registered": True,
        "status": "APPROVED",
        "created_at": "2026-08-10"
    },
    {
        "id": "teacher_9",
        "name": "Prof. Pooja Deshmukh",
        "email": "pooja.d@college.edu",
        "password": "password123",
        "employee_id": "EMP-3014",
        "department": "Information Technology",
        "designation": "Assistant Professor",
        "cabin": "Room 201 - IT Wing",
        "status_college": "PRESENT",
        "check_in_time": "09:00 AM",
        "attendance_rate": 97,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Data Communication"],
        "avatar": teacher_avatars[3],
        "face_registered": True,
        "status": "APPROVED",
        "created_at": "2026-08-10"
    },
    {
        "id": "teacher_10",
        "name": "Prof. Karan Mehta",
        "email": "karan.mehta@college.edu",
        "password": "password123",
        "employee_id": "EMP-3015",
        "department": "Information Technology",
        "designation": "Assistant Professor",
        "cabin": "Room 205 - IT Wing",
        "status_college": "ABSENT",
        "check_in_time": "--",
        "attendance_rate": 80,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Advanced Networking"],
        "avatar": teacher_avatars[4],
        "face_registered": True,
        "status": "APPROVED",
        "created_at": "2026-08-10"
    },
    {
        "id": "teacher_11",
        "name": "Prof. Sneha Kulkarni",
        "email": "sneha.k@college.edu",
        "password": "password123",
        "employee_id": "EMP-3016",
        "department": "Information Technology",
        "designation": "Associate Professor",
        "cabin": "Room 208 - IT Wing",
        "status_college": "PRESENT",
        "check_in_time": "08:35 AM",
        "attendance_rate": 94,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Network Security"],
        "avatar": teacher_avatars[5],
        "face_registered": True,
        "status": "APPROVED",
        "created_at": "2026-08-10"
    },
    {
        "id": "teacher_12",
        "name": "Prof. Rahul Shinde",
        "email": "rahul.shinde@college.edu",
        "password": "password123",
        "employee_id": "EMP-3017",
        "department": "AI & Data Science",
        "designation": "Assistant Professor",
        "cabin": "Lab 102 - AI Hub",
        "status_college": "PRESENT",
        "check_in_time": "09:10 AM",
        "attendance_rate": 91,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Machine Learning"],
        "avatar": teacher_avatars[6],
        "face_registered": True,
        "status": "APPROVED",
        "created_at": "2026-08-10"
    },
    {
        "id": "teacher_req_1",
        "name": "Dr. Vikramaditya Rao",
        "email": "vikram.rao@college.edu",
        "password": "password123",
        "employee_id": "EMP-5012",
        "department": "AI & Data Science",
        "designation": "Professor",
        "cabin": "Room 204 - Tech Hub",
        "status_college": "ABSENT",
        "check_in_time": "--",
        "attendance_rate": 0,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Artificial Intelligence", "Deep Learning"],
        "avatar": teacher_avatars[5],
        "face_registered": True,
        "status": "PENDING_APPROVAL",
        "created_at": "2026-10-21"
    },
    {
        "id": "teacher_req_2",
        "name": "Prof. Sunita Kulkarni",
        "email": "sunita.k@college.edu",
        "password": "password123",
        "employee_id": "EMP-5019",
        "department": "Information Technology",
        "designation": "Assistant Professor",
        "cabin": "Room 302 - IT Block",
        "status_college": "ABSENT",
        "check_in_time": "--",
        "attendance_rate": 0,
        "is_class_teacher": False,
        "class_assigned": "",
        "subjects": ["Cloud Computing"],
        "avatar": teacher_avatars[6],
        "face_registered": True,
        "status": "PENDING_APPROVAL",
        "created_at": "2026-10-22"
    }
]

# Multiple Classes Students
students = [
    # SE Computer - Div A
    {
        "id": "student_1",
        "name": "Aarav Sharma",
        "email": "aarav.sharma@college.edu",
        "password": "password123",
        "roll_no": "01",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div A",
        "class_code": "SE Computer - Div A",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[0],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 91,
        "present_count": 109,
        "absent_count": 10,
        "not_marked": 1,
        "rank": 2,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_2",
        "name": "Michael Kopfler",
        "email": "michael.k@college.edu",
        "password": "password123",
        "roll_no": "02",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div A",
        "class_code": "SE Computer - Div A",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[1],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 85,
        "present_count": 102,
        "absent_count": 15,
        "not_marked": 3,
        "rank": 5,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_3",
        "name": "Alice Koller",
        "email": "alice.koller@college.edu",
        "password": "password123",
        "roll_no": "03",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div A",
        "class_code": "SE Computer - Div A",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[2],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 92,
        "present_count": 110,
        "absent_count": 6,
        "not_marked": 4,
        "rank": 1,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_4",
        "name": "Peter Dinklage",
        "email": "peter.d@college.edu",
        "password": "password123",
        "roll_no": "04",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div A",
        "class_code": "SE Computer - Div A",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[3],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 76,
        "present_count": 91,
        "absent_count": 25,
        "not_marked": 4,
        "rank": 8,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_5",
        "name": "Julia Berger",
        "email": "julia.b@college.edu",
        "password": "password123",
        "roll_no": "05",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div A",
        "class_code": "SE Computer - Div A",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[4],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 95,
        "present_count": 114,
        "absent_count": 2,
        "not_marked": 4,
        "rank": 1,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_6",
        "name": "John Wick",
        "email": "john.wick@college.edu",
        "password": "password123",
        "roll_no": "06",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div A",
        "class_code": "SE Computer - Div A",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[5],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 69,
        "present_count": 83,
        "absent_count": 34,
        "not_marked": 3,
        "rank": 9,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_7",
        "name": "George Limbaf",
        "email": "george.l@college.edu",
        "password": "password123",
        "roll_no": "07",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div A",
        "class_code": "SE Computer - Div A",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[6],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 82,
        "present_count": 98,
        "absent_count": 18,
        "not_marked": 4,
        "rank": 6,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_8",
        "name": "Dave Johnson",
        "email": "dave.j@college.edu",
        "password": "password123",
        "roll_no": "08",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div A",
        "class_code": "SE Computer - Div A",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[7],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 79,
        "present_count": 95,
        "absent_count": 21,
        "not_marked": 4,
        "rank": 7,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_9",
        "name": "Rohan Gupta",
        "email": "rohan.gupta@college.edu",
        "password": "password123",
        "roll_no": "09",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div A",
        "class_code": "SE Computer - Div A",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[8],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 87,
        "present_count": 104,
        "absent_count": 12,
        "not_marked": 4,
        "rank": 4,
        "created_at": "2026-08-15"
    },

    # SE Computer - Div B
    {
        "id": "student_b1",
        "name": "Kameron Porter",
        "email": "kameron.p@college.edu",
        "password": "password123",
        "roll_no": "01",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div B",
        "class_code": "SE Computer - Div B",
        "class_teacher_id": "teacher_2",
        "avatar": student_avatars[1],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 94,
        "present_count": 112,
        "absent_count": 5,
        "not_marked": 3,
        "rank": 1,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_b2",
        "name": "Sarah Jenkins",
        "email": "sarah.j@college.edu",
        "password": "password123",
        "roll_no": "02",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div B",
        "class_code": "SE Computer - Div B",
        "class_teacher_id": "teacher_2",
        "avatar": student_avatars[2],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 88,
        "present_count": 105,
        "absent_count": 12,
        "not_marked": 3,
        "rank": 2,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_b3",
        "name": "Liam Smith",
        "email": "liam.s@college.edu",
        "password": "password123",
        "roll_no": "03",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div B",
        "class_code": "SE Computer - Div B",
        "class_teacher_id": "teacher_2",
        "avatar": student_avatars[3],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 78,
        "present_count": 93,
        "absent_count": 24,
        "not_marked": 3,
        "rank": 4,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_b4",
        "name": "Emma Watson",
        "email": "emma.w@college.edu",
        "password": "password123",
        "roll_no": "04",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div B",
        "class_code": "SE Computer - Div B",
        "class_teacher_id": "teacher_2",
        "avatar": student_avatars[4],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 86,
        "present_count": 103,
        "absent_count": 14,
        "not_marked": 3,
        "rank": 3,
        "created_at": "2026-08-15"
    },

    # TE Computer - Div A
    {
        "id": "student_te1",
        "name": "Ravi Kumar",
        "email": "ravi.k@college.edu",
        "password": "password123",
        "roll_no": "01",
        "department": "Computer Engineering",
        "year": "Third Year",
        "division": "Div A",
        "class_code": "TE Computer - Div A",
        "class_teacher_id": "teacher_3",
        "avatar": student_avatars[5],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 89,
        "present_count": 107,
        "absent_count": 11,
        "not_marked": 2,
        "rank": 2,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_te2",
        "name": "Priya Patel",
        "email": "priya.p@college.edu",
        "password": "password123",
        "roll_no": "02",
        "department": "Computer Engineering",
        "year": "Third Year",
        "division": "Div A",
        "class_code": "TE Computer - Div A",
        "class_teacher_id": "teacher_3",
        "avatar": student_avatars[6],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 93,
        "present_count": 112,
        "absent_count": 6,
        "not_marked": 2,
        "rank": 1,
        "created_at": "2026-08-15"
    },

    # BE - Computer
    {
        "id": "student_be1",
        "name": "Aditya Rao",
        "email": "aditya.rao@college.edu",
        "password": "password123",
        "roll_no": "01",
        "department": "Computer Engineering",
        "year": "Final Year",
        "division": "Div A",
        "class_code": "BE - Computer",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[7],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 92,
        "present_count": 110,
        "absent_count": 8,
        "not_marked": 2,
        "rank": 1,
        "created_at": "2026-08-15"
    },
    {
        "id": "student_be2",
        "name": "Tanya Sen",
        "email": "tanya.sen@college.edu",
        "password": "password123",
        "roll_no": "02",
        "department": "Computer Engineering",
        "year": "Final Year",
        "division": "Div A",
        "class_code": "BE - Computer",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[8],
        "face_registered": True,
        "status": "APPROVED",
        "overall_attendance": 84,
        "present_count": 100,
        "absent_count": 16,
        "not_marked": 4,
        "rank": 2,
        "created_at": "2026-08-15"
    },

    # Pending registration requests for Class Teacher approval
    {
        "id": "student_req_1",
        "name": "Ishaan Trivedi",
        "email": "ishaan.t@college.edu",
        "password": "password123",
        "roll_no": "10",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div A",
        "class_code": "SE Computer - Div A",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[1],
        "face_registered": True,
        "status": "PENDING_APPROVAL",
        "overall_attendance": 0,
        "present_count": 0,
        "absent_count": 0,
        "not_marked": 0,
        "created_at": "2026-10-21"
    },
    {
        "id": "student_req_2",
        "name": "Tanvi Merchant",
        "email": "tanvi.m@college.edu",
        "password": "password123",
        "roll_no": "11",
        "department": "Computer Engineering",
        "year": "Second Year",
        "division": "Div A",
        "class_code": "SE Computer - Div A",
        "class_teacher_id": "teacher_1",
        "avatar": student_avatars[4],
        "face_registered": True,
        "status": "PENDING_APPROVAL",
        "overall_attendance": 0,
        "present_count": 0,
        "absent_count": 0,
        "not_marked": 0,
        "created_at": "2026-10-22"
    }
]

# Daily Attendance Sessions Records per Date & Subject
attendance_history = {
    "2026-10-23": {
        "SE Computer - Div A": {
            "Operating Systems": {
                "present": ["student_1", "student_3", "student_5", "student_7", "student_9"],
                "absent": ["student_2", "student_4", "student_6"],
                "not_marked": ["student_8"]
            },
            "Computer Networks": {
                "present": ["student_1", "student_2", "student_3", "student_5", "student_8", "student_9"],
                "absent": ["student_4", "student_6"],
                "not_marked": ["student_7"]
            }
        },
        "SE Computer - Div B": {
            "Data Structures": {
                "present": ["student_b1", "student_b2", "student_b4"],
                "absent": ["student_b3"],
                "not_marked": []
            }
        },
        "BE - Computer": {
            "Cloud Computing": {
                "present": ["student_be1"],
                "absent": ["student_be2"],
                "not_marked": []
            }
        }
    },
    "2026-10-22": {
        "SE Computer - Div A": {
            "Operating Systems": {
                "present": ["student_1", "student_2", "student_3", "student_4", "student_5", "student_8"],
                "absent": ["student_6", "student_7"],
                "not_marked": ["student_9"]
            },
            "Database Management": {
                "present": ["student_1", "student_3", "student_5", "student_7", "student_8", "student_9"],
                "absent": ["student_2", "student_4", "student_6"],
                "not_marked": []
            }
        },
        "SE Computer - Div B": {
            "Data Structures": {
                "present": ["student_b1", "student_b3", "student_b4"],
                "absent": ["student_b2"],
                "not_marked": []
            }
        }
    },
    "2026-10-21": {
        "SE Computer - Div A": {
            "Operating Systems": {
                "present": ["student_1", "student_2", "student_5", "student_6", "student_7", "student_9"],
                "absent": ["student_3", "student_4", "student_8"],
                "not_marked": []
            }
        }
    }
}

# Subjects with Syllabus & Lecture History
subjects = [
    {
        "code": "CS203",
        "name": "Operating Systems",
        "full_code": "SE-CSE-301",
        "teacher": "Prof. Priya Sharma",
        "teacher_cabin": "Room 401 - IT Block",
        "attendance": 88,
        "rank": "#2",
        "held": 28,
        "attended": 25,
        "description": "Exploration of process management, multithreading, concurrency control, virtual memory management, deadlock handling, and file system architecture.",
        "syllabus": [
            {"title": "1. OS Fundamentals & Architectures", "progress": 100, "status": "Completed"},
            {"title": "2. Process Control, Threads & IPC", "progress": 100, "status": "Completed"},
            {"title": "3. CPU Scheduling & Real-time Tasks", "progress": 85, "status": "In Progress"},
            {"title": "4. Memory Management & Paging", "progress": 60, "status": "In Progress"},
            {"title": "5. File Systems & Virtualization", "progress": 25, "status": "Upcoming"}
        ],
        "lectures": [
            {"id": "L28", "title": "Virtual Memory & Page Replacement", "date": "23 Oct 2026", "time": "09:00 - 10:00 AM", "room": "LH-302", "status": "PRESENT", "type": "Lecture"},
            {"id": "L27", "title": "Segmentation & Swapping Architecture", "date": "22 Oct 2026", "time": "09:00 - 10:00 AM", "room": "LH-302", "status": "PRESENT", "type": "Lecture"},
            {"id": "L26", "title": "Semaphores & Classical IPC Problems", "date": "20 Oct 2026", "time": "11:15 - 12:15 PM", "room": "LH-302", "status": "ABSENT", "type": "Lecture"},
            {"id": "L25", "title": "Process Synchronization & Mutex Locks", "date": "18 Oct 2026", "time": "09:00 - 10:00 AM", "room": "LH-302", "status": "PRESENT", "type": "Lecture"},
            {"id": "L24", "title": "CPU Scheduling Algorithms (Round Robin)", "date": "16 Oct 2026", "time": "02:00 - 03:00 PM", "room": "LH-302", "status": "PRESENT", "type": "Lecture"},
            {"id": "L23", "title": "Multithreading Models & POSIX Threads", "date": "14 Oct 2026", "time": "09:00 - 10:00 AM", "room": "LH-302", "status": "PRESENT", "type": "Lecture"},
            {"id": "L22", "title": "Inter-Process Communication & Pipes", "date": "11 Oct 2026", "time": "11:15 - 12:15 PM", "room": "LH-302", "status": "PRESENT", "type": "Lecture"}
        ]
    },
    {
        "code": "CS202",
        "name": "Database Management",
        "full_code": "SE-CSE-302",
        "teacher": "Dr. Ananya Iyer",
        "teacher_cabin": "Lab 3B - AI Center",
        "attendance": 82,
        "rank": "#4",
        "held": 26,
        "attended": 21,
        "description": "Relational schema design, normalization, ACID properties, indexing structures (B+ trees), query optimization, and distributed database models.",
        "syllabus": [
            {"title": "1. Relational Model & ER Modeling", "progress": 100, "status": "Completed"},
            {"title": "2. Relational Algebra & Advanced SQL", "progress": 95, "status": "Completed"},
            {"title": "3. Normalization (1NF through BCNF)", "progress": 80, "status": "In Progress"},
            {"title": "4. Transaction Processing & Concurrency", "progress": 50, "status": "In Progress"},
            {"title": "5. Query Optimization & Indexing", "progress": 20, "status": "Upcoming"}
        ],
        "lectures": [
            {"id": "L26", "title": "Transaction Concurrency & Strict 2PL", "date": "22 Oct 2026", "time": "10:15 - 11:15 AM", "room": "LH-304", "status": "PRESENT", "type": "Lecture"},
            {"id": "L25", "title": "Serializability & Recovery Techniques", "date": "21 Oct 2026", "time": "10:15 - 11:15 AM", "room": "LH-304", "status": "PRESENT", "type": "Lecture"},
            {"id": "L24", "title": "Multivalued Dependencies & 4NF", "date": "19 Oct 2026", "time": "01:00 - 02:00 PM", "room": "LH-304", "status": "ABSENT", "type": "Lecture"},
            {"id": "L23", "title": "Third Normal Form & BCNF Decomposition", "date": "17 Oct 2026", "time": "10:15 - 11:15 AM", "room": "LH-304", "status": "PRESENT", "type": "Lecture"}
        ]
    },
    {
        "code": "CS201",
        "name": "Data Structures",
        "full_code": "SE-CSE-303",
        "teacher": "Prof. Rajesh Verma",
        "teacher_cabin": "Room 402 - Main Wing",
        "attendance": 92,
        "rank": "#1",
        "held": 28,
        "attended": 26,
        "description": "Linear and hierarchical data organizations including AVL trees, Red-Black trees, Heaps, Graph algorithms, Dynamic Programming, and complexity analysis.",
        "syllabus": [
            {"title": "1. Arrays, Stacks, Queues & Applications", "progress": 100, "status": "Completed"},
            {"title": "2. Linked Lists & Doubly Linked Variants", "progress": 100, "status": "Completed"},
            {"title": "3. Balanced Trees & Priority Queues", "progress": 90, "status": "In Progress"},
            {"title": "4. Graph Traversals & Minimum Spanning Trees", "progress": 70, "status": "In Progress"},
            {"title": "5. Hashing & Disjoint Set Union", "progress": 30, "status": "Upcoming"}
        ],
        "lectures": [
            {"id": "L28", "title": "Dijkstra Algorithm & Shortest Paths", "date": "23 Oct 2026", "time": "11:30 - 12:30 PM", "room": "LH-301", "status": "PRESENT", "type": "Lecture"},
            {"id": "L27", "title": "Kruskal & Prim MST Implementations", "date": "21 Oct 2026", "time": "11:30 - 12:30 PM", "room": "LH-301", "status": "PRESENT", "type": "Lecture"},
            {"id": "L26", "title": "AVL Tree Rotations & Balance Factors", "date": "19 Oct 2026", "time": "02:00 - 03:00 PM", "room": "LH-301", "status": "PRESENT", "type": "Lecture"}
        ]
    },
    {
        "code": "CS204",
        "name": "Computer Networks",
        "full_code": "SE-CSE-304",
        "teacher": "Prof. Sameer Deshmukh",
        "teacher_cabin": "Room 405 - North Block",
        "attendance": 78,
        "rank": "#5",
        "held": 25,
        "attended": 20,
        "description": "OSI & TCP/IP layered architecture, framing, sliding window flow control, routing algorithms (OSPF, BGP), congestion control, socket programming.",
        "syllabus": [
            {"title": "1. Physical Layer & Encoding Schemes", "progress": 100, "status": "Completed"},
            {"title": "2. Data Link Layer & MAC Protocols", "progress": 90, "status": "Completed"},
            {"title": "3. Network Layer & IP Addressing (IPv4/v6)", "progress": 75, "status": "In Progress"},
            {"title": "4. Transport Layer (TCP Flow & Congestion)", "progress": 55, "status": "In Progress"},
            {"title": "5. Application Layer (DNS, HTTP, TLS)", "progress": 15, "status": "Upcoming"}
        ],
        "lectures": [
            {"id": "L25", "title": "TCP Congestion Control (Reno, Tahoe)", "date": "23 Oct 2026", "time": "01:30 - 02:30 PM", "room": "LH-303", "status": "PRESENT", "type": "Lecture"},
            {"id": "L24", "title": "Subnetting, CIDR & NAT Mechanisms", "date": "20 Oct 2026", "time": "01:30 - 02:30 PM", "room": "LH-303", "status": "ABSENT", "type": "Lecture"},
            {"id": "L23", "title": "Distance Vector Routing & Split Horizon", "date": "18 Oct 2026", "time": "01:30 - 02:30 PM", "room": "LH-303", "status": "PRESENT", "type": "Lecture"}
        ]
    },
    {
        "code": "CS205",
        "name": "Software Engineering",
        "full_code": "SE-CSE-305",
        "teacher": "Prof. Kavita Nair",
        "teacher_cabin": "Room 410 - South Wing",
        "attendance": 91,
        "rank": "#3",
        "held": 24,
        "attended": 22,
        "description": "Agile Scrum methodologies, software requirements specification, architectural design patterns, unit/integration testing strategies, CI/CD pipelines.",
        "syllabus": [
            {"title": "1. Software Process Models & SDLC", "progress": 100, "status": "Completed"},
            {"title": "2. Agile Scrum, User Stories & Sprints", "progress": 100, "status": "Completed"},
            {"title": "3. Design Patterns & SOLID Principles", "progress": 85, "status": "In Progress"},
            {"title": "4. Automated Testing & Code Quality", "progress": 65, "status": "In Progress"},
            {"title": "5. DevOps, Microservices & Monitoring", "progress": 30, "status": "Upcoming"}
        ],
        "lectures": [
            {"id": "L24", "title": "Automated Unit Testing & Mocking", "date": "22 Oct 2026", "time": "02:45 - 03:45 PM", "room": "LH-305", "status": "PRESENT", "type": "Lecture"},
            {"id": "L23", "title": "Factory & Observer Design Patterns", "date": "21 Oct 2026", "time": "02:45 - 03:45 PM", "room": "LH-305", "status": "PRESENT", "type": "Lecture"}
        ]
    }
]

weekly_trends = [
    {"week": "W1", "rate": 82},
    {"week": "W2", "rate": 85},
    {"week": "W3", "rate": 78},
    {"week": "W4", "rate": 91},
    {"week": "W5", "rate": 87},
    {"week": "W6", "rate": 89},
    {"week": "W7", "rate": 86},
    {"week": "W8", "rate": 92}
]

admin_14day_trends = [
    {"date": "10 Oct", "rate": 82},
    {"date": "11 Oct", "rate": 84},
    {"date": "12 Oct", "rate": 86},
    {"date": "13 Oct", "rate": 83},
    {"date": "14 Oct", "rate": 87},
    {"date": "15 Oct", "rate": 89},
    {"date": "16 Oct", "rate": 91},
    {"date": "17 Oct", "rate": 88},
    {"date": "18 Oct", "rate": 95},
    {"date": "19 Oct", "rate": 85},
    {"date": "20 Oct", "rate": 89},
    {"date": "21 Oct", "rate": 87},
    {"date": "22 Oct", "rate": 88},
    {"date": "23 Oct", "rate": 92}
]

app_data = {
    "settings": settings,
    "admins": admins,
    "teachers": teachers,
    "students": students,
    "subjects": subjects,
    "weekly_trends": weekly_trends,
    "admin_14day_trends": admin_14day_trends,
    "attendance_history": attendance_history,
    "active_session": {
        "is_active": True,
        "teacher_id": "teacher_1",
        "teacher_verified": True,
        "class_code": "SE Computer - Div A",
        "year": "Second Year",
        "subject": "Operating Systems",
        "date": "2026-10-23",
        "started_at": "09:00 AM",
        "verified_students": ["student_1", "student_3", "student_5", "student_7", "student_9"]
    },
    "otps": {}
}

with open(data_path, "w", encoding="utf-8") as f:
    json.dump(app_data, f, indent=2)

print("Seed data written successfully to", data_path)
