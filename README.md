# RaiSakshya — Smart Biometric Attendance Intelligence System

A full-stack, AI-powered educational attendance platform replicating pixel-perfect designs from the **Pixel Perfect UI Replica** Stitch project with AWS Rekognition facial biometric verification, multi-portal architecture, and multi-tier approval workflows.

---

## 🌟 Architecture & Portals

### 1. 🎓 Student Portal
- **Student Dashboard** (`/student/dashboard`): Overall attendance metrics (88%), donut breakdown (106 Present, 10 Absent, 4 Not Marked), weekly trend curve (W1–W8), subject-wise progress bars, risk alerts, and consistency targets.
- **Teachers' College Presence** (`/student/teachers`): Live faculty presence status (Present / Absent), cabins, departments, and direct reachout.
- **Subject Attendance & Syllabus Insights** (`/student/subjects`): Detailed breakdown for individual subjects (e.g. Operating Systems: 78%), lecture-by-lecture audit trails, and status filters.

### 2. 👩‍🏫 Teacher Portal
- **Take Attendance with Biometric Lock** (`/teacher/take-attendance`):
  - **Academic Selectors**: Academic Year, Class & Division, Subject, Date.
  - **Step 1 — Teacher Face Verification**: The teacher verifies their face via the webcam viewfinder before attendance unlocks.
  - **Step 2 — Student Facial Biometric Verification**: Students click their name on the right-hand roll list, click **"Verify Face"**, the camera captures their face, verifies via **AWS Rekognition**, and marks them **PRESENT** with green celebratory badges.
- **Daily Student Attendance** (`/teacher/daily-attendance`): Specific day breakdown of present, absent, and late students with date filters.
- **All Days Attendance Analytics** (`/teacher/all-days`): Multi-session cumulative attendance percentage, student rankings, and export tools.
- **Student Profile Insights** (`/teacher/student-profile`): Deep-dive biometric attendance profile for individual students with monthly trends, subject distribution, and recent activity logs.
- **Class Teacher Approval Section** (`/teacher/student-requests`):
  - Dedicated view accessible to Class Teachers.
  - Review incoming student registration requests with their registered face snapshot, OTP verification badge, and academic credentials.
  - One-click **Approve Student** or **Reject Request**. Only approved students are permitted to log in.

### 3. 🏛️ Admin Portal
- **Institutional Analytics Dashboard** (`/admin/dashboard`): Cross-departmental attendance health, low attendance alerts, and student performance metrics.
- **Faculty Attendance Audit** (`/admin/teachers-attendance`): Complete tracking of all college professors, daily check-in timestamps, and monthly attendance percentages.
- **Teacher Sign-up Requests** (`/admin/teacher-requests`): Review faculty registration applications, evaluate verified face profiles, and **Approve/Decline** access to the teacher portal.
- **Settings & AWS Rekognition Management** (`/admin/settings`):
  - Institution details, academic years, and biometric thresholds.
  - **Live AWS Rekognition Control Panel**: Input AWS Access Key, Secret Key, Region, and Collection ID. Includes live connection tests and one-click collection creation.

---

## 🔐 Authentication & Two-Phase Registration

- **Unified Login** (`/login`): Single entry point for Students, Teachers, and Admins with role selectors, quick 1-click demo fillers, password visibility toggle, biometric face recognition login, and automatic detection of pending approval status.
- **Student Two-Phase Sign-up** (`/register/student`):
  1. *Phase 1*: College Email (`.edu`), password creation, and 6-digit OTP verification.
  2. *Phase 2*: Student academic details (Year, Department, Roll No, Class Division, Assigned Class Teacher), Avatar selection from animated student faces, and live webcam face registration via AWS Rekognition. Submits request to assigned Class Teacher.
- **Teacher Two-Phase Sign-up** (`/register/teacher`):
  1. *Phase 1*: Faculty Email, password creation, and OTP verification.
  2. *Phase 2*: Faculty information (Employee ID, Department, Designation, Cabin, Subjects taught, Class Teacher appointment toggle), Avatar selection from animated teacher faces, and live webcam face enrollment. Submits request to College Administrator.

---

## 🚀 Running the Application

1. **Start the Server**:
   ```powershell
   python app.py
   ```
2. **Access in Your Browser**:
   Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔑 Demo Accounts & Quick Access

You can log in directly at `http://127.0.0.1:5000/login` or use the 1-click role switcher buttons on the login page:

| Role | Name | Email | Password | Permissions & Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Student** | Aarav Sharma | `aarav.sharma@college.edu` | `password123` | View attendance metrics, faculty presence, OS logs |
| **Teacher** | Prof. Priya Sharma | `priya.sharma@college.edu` | `password123` | **Class Teacher** (Can approve student registration requests & take attendance) |
| **Admin** | Dr. Rajesh Kulkarni | `admin@college.edu` | `password123` | **Principal / Dean** (Can approve teacher requests, institutional analytics, AWS settings) |

---

## 🎨 Design System & Assets
- **Branding**: RaiSakshya ("Smart Attendance for Brighter Futures")
- **Typography**: Google Fonts — Plus Jakarta Sans & Caveat
- **Avatars**: 17 transparent animated 3D character avatars stored in `static/student_faces/` and `static/teacher_faces/`.
- **Top Navigation Bar**: Consistent capsule design across all portals (`#0B1522`), dynamic active tab indicators, portal switcher, profile details, and role switcher.
- **AWS Rekognition**: Connected to AWS collection `raisakshya-attendance` (`ap-south-1`) with automated fallback for offline resilience.
