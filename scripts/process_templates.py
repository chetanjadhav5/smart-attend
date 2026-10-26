import os
import re

STUDENT_FACES = [
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

TEACHER_FACES = [
    "/static/teacher_faces/20bb28b4-f54a-4a3c-9630-e75ad391e672.png",
    "/static/teacher_faces/22ea68d3-8b39-4b21-86f5-524d563ceee4.png",
    "/static/teacher_faces/308cb046-f220-4dba-a871-63cdef5a258c.png",
    "/static/teacher_faces/33768a7e-c518-4ba6-bc46-b6cc06c36aa5.png",
    "/static/teacher_faces/70a23d6a-ee5f-422b-b85e-a43ed14cab66.png",
    "/static/teacher_faces/9dbcd861-2ee5-4022-a40b-b36af3d8f553.png",
    "/static/teacher_faces/aaa3d5cf-fec2-4f08-ad68-c02cc114500b.png",
    "/static/teacher_faces/c3cde75f-4cea-4624-9e4c-d235c397916c.png"
]

CONFIG = {
    "student_dashboard.html": ("student", "dashboard", "student"),
    "student_teachers.html": ("student", "teachers", "teacher"),
    "student_subject.html": ("student", "subjects", "student"),
    "teacher_attendance_specific_day.html": ("teacher", "daily_attendance", "student"),
    "teacher_students_all_days.html": ("teacher", "all_days", "student"),
    "teacher_student_profile.html": ("teacher", "student_profile", "student"),
    "admin_dashboard.html": ("admin", "dashboard", "teacher"),
    "admin_teachers_attendance.html": ("admin", "teachers_attendance", "teacher"),
    "admin_teacher_requests.html": ("admin", "teacher_requests", "teacher"),
    "admin_settings.html": ("admin", "settings", "teacher")
}

IN_DIR = r"d:\project\stitch_extracted_pages"
OUT_DIR = r"d:\project\templates"

for fname, (portal, tab, face_type) in CONFIG.items():
    src_file = os.path.join(IN_DIR, fname)
    if not os.path.exists(src_file):
        print(f"Skipping {fname}, does not exist")
        continue

    with open(src_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ensure Font Awesome
    fa_tag = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'
    if "font-awesome" not in content:
        content = content.replace("</head>", f"{fa_tag}\n</head>")

    # 2. Replace Header with Unified Navbar Container
    # Match <header ...>...</header>
    content = re.sub(r'<header[\s\S]*?</header>', '<div id="global-navbar"></div>', content, count=1)

    # 3. Replace External Images with local faces
    faces_pool = TEACHER_FACES if face_type == "teacher" else STUDENT_FACES
    img_counter = [0]
    def repl_img(m):
        idx = img_counter[0] % len(faces_pool)
        img_counter[0] += 1
        return f'src="{faces_pool[idx]}"'

    content = re.sub(r'src=[\x22\x27]https://lh3\.googleusercontent\.com/[^\x22\x27]+[\x22\x27]', repl_img, content)

    # 4. Inject Bottom Scripts
    scripts = f"""
<script src="/static/js/api.js"></script>
<script src="/static/js/navbar.js"></script>
<script>
  renderGlobalNavbar('{portal}', '{tab}');
</script>
</body>
"""
    content = content.replace("</body>", scripts)

    dst_file = os.path.join(OUT_DIR, fname)
    with open(dst_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated {fname} for {portal}:{tab}")
