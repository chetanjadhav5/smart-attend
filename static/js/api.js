// RaiSakshya API Client

const API = {
  async getCurrentUser() {
    try {
      const res = await fetch('/api/auth/current-user');
      return await res.json();
    } catch (e) {
      console.error(e);
      return { logged_in: false };
    }
  },

  async switchUser(role, userId = null) {
    const res = await fetch('/api/auth/switch-user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role, user_id: userId })
    });
    return await res.json();
  },

  async sendOtp(email, purpose = 'Account Verification') {
    const res = await fetch('/api/auth/send-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, purpose })
    });
    return await res.json();
  },

  async verifyOtp(email, otp) {
    const res = await fetch('/api/auth/verify-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, otp })
    });
    return await res.json();
  },

  async registerStudent(data) {
    const res = await fetch('/api/auth/register-student', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await res.json();
  },

  async registerTeacher(data) {
    const res = await fetch('/api/auth/register-teacher', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await res.json();
  },

  async login(email, password, role) {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, role })
    });
    return await res.json();
  },

  async faceLogin(faceImage) {
    const res = await fetch('/api/auth/face-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ face_image: faceImage })
    });
    return await res.json();
  },

  async selectFaceAccount(userId, role) {
    const res = await fetch('/api/auth/select-face-account', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, role: role })
    });
    return await res.json();
  },

  async getSession() {
    const res = await fetch('/api/attendance/session');
    return await res.json();
  },

  async verifyTeacher(data) {
    const res = await fetch('/api/attendance/verify-teacher', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await res.json();
  },

  async verifyStudent(studentId, faceImage = null, classCode = null, subject = null) {
    const payload = { student_id: studentId, face_image: faceImage };
    if (classCode) payload.class_code = classCode;
    if (subject) payload.subject = subject;
    const res = await fetch('/api/attendance/verify-student', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return await res.json();
  },

  async completeAttendanceSession(payload) {
    const res = await fetch('/api/attendance/complete-session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return await res.json();
  },

  async startNewPeriodSession() {
    const res = await fetch('/api/attendance/new-period', { method: 'POST' });
    return await res.json();
  },

  async getTeacherDashboardData() {
    const res = await fetch('/api/teacher/dashboard-data');
    return await res.json();
  },

  async getTeacherStatus() {
    const res = await fetch('/api/teachers/status');
    return await res.json();
  },

  async getAdminTeacherRequests() {
    const res = await fetch('/api/admin/teacher-requests');
    return await res.json();
  },

  async approveTeacher(teacherId) {
    const res = await fetch(`/api/admin/teacher-requests/${teacherId}/approve`, { method: 'POST' });
    return await res.json();
  },

  async rejectTeacher(teacherId) {
    const res = await fetch(`/api/admin/teacher-requests/${teacherId}/reject`, { method: 'POST' });
    return await res.json();
  },

  async getTeacherStudentRequests(teacherId = null) {
    const url = teacherId ? `/api/teacher/student-requests?teacher_id=${teacherId}` : '/api/teacher/student-requests';
    const res = await fetch(url);
    return await res.json();
  },

  async getStudentRequestsForTeacher(teacherId = null) {
    return await this.getTeacherStudentRequests(teacherId);
  },

  async approveStudent(studentId) {
    const res = await fetch(`/api/teacher/student-requests/${studentId}/approve`, { method: 'POST' });
    return await res.json();
  },

  async rejectStudent(studentId) {
    const res = await fetch(`/api/teacher/student-requests/${studentId}/reject`, { method: 'POST' });
    return await res.json();
  },

  async getMyProfile() {
    const res = await fetch('/api/user/my-profile');
    return await res.json();
  },

  async updateStudentProfile(payload) {
    const res = await fetch('/api/student/update-profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return await res.json();
  },

  async updateTeacherProfile(payload) {
    const res = await fetch('/api/teacher/update-profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return await res.json();
  },

  async getSettings() {
    const res = await fetch('/api/settings');
    return await res.json();
  },

  async saveSettings(settings) {
    const res = await fetch('/api/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings)
    });
    return await res.json();
  },

  async testAws(config = {}) {
    const res = await fetch('/api/settings/test-aws', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config || {})
    });
    return await res.json();
  },

  async testSmtp(email = null) {
    const res = await fetch('/api/settings/test-smtp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email })
    });
    return await res.json();
  },

  async getStudentDashboard() {
    const res = await fetch('/api/student/dashboard');
    return await res.json();
  },

  async getStudentSubjects() {
    const res = await fetch('/api/student/subjects');
    return await res.json();
  },

  async getTeachersList(dept = null, q = null) {
    const params = new URLSearchParams();
    if (dept) params.append('dept', dept);
    if (q) params.append('q', q);
    const res = await fetch(`/api/teachers?${params.toString()}`);
    return await res.json();
  },

  async getTeacherStudentsAttendance(classCode = null, date = null, subject = null, q = null) {
    const params = new URLSearchParams();
    if (classCode) params.append('class_code', classCode);
    if (date) params.append('date', date);
    if (subject) params.append('subject', subject);
    if (q) params.append('q', q);
    const res = await fetch(`/api/teacher/students-attendance?${params.toString()}`);
    return await res.json();
  },

  async getTeacherStudentProfile(studentId = null) {
    const params = new URLSearchParams();
    if (studentId) params.append('student_id', studentId);
    const res = await fetch(`/api/teacher/student-profile?${params.toString()}`);
    return await res.json();
  },

  async getTeacherProfile(teacherId = null) {
    const params = new URLSearchParams();
    if (teacherId) params.append('teacher_id', teacherId);
    const res = await fetch(`/api/student/teacher-profile?${params.toString()}`);
    return await res.json();
  },

  async getAdminDashboardData() {
    const res = await fetch('/api/admin/dashboard-data');
    return await res.json();
  },

  async getAdminTeachersAttendance(dept = null, date = null, q = null) {
    const params = new URLSearchParams();
    if (dept) params.append('dept', dept);
    if (date) params.append('date', date);
    if (q) params.append('q', q);
    const res = await fetch(`/api/admin/teachers-attendance-data?${params.toString()}`);
    return await res.json();
  },

  async getMyProfile() {
    const res = await fetch('/api/user/my-profile');
    return await res.json();
  },

  async updateStudentProfile(data) {
    const res = await fetch('/api/student/update-profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await res.json();
  },

  async updateTeacherProfile(data) {
    const res = await fetch('/api/teacher/update-profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await res.json();
  },

  showToast(message, type = 'success') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'fixed bottom-5 right-5 z-[9999] flex flex-col gap-2 pointer-events-none';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    const isSuccess = type === 'success';
    const isError = type === 'error';
    const bgClass = isSuccess ? 'bg-[#00C48C] text-white' : (isError ? 'bg-rose-600 text-white' : 'bg-slate-900 text-white');
    toast.className = `${bgClass} px-5 py-3 rounded-2xl shadow-2xl flex items-center gap-3 text-sm font-bold pointer-events-auto transition-all duration-300 transform translate-y-4 opacity-0`;
    toast.innerHTML = `
      <span>${isSuccess ? '✓' : (isError ? '✕' : 'ℹ')}</span>
      <span>${message}</span>
    `;
    container.appendChild(toast);
    requestAnimationFrame(() => {
      toast.classList.remove('translate-y-4', 'opacity-0');
    });
    setTimeout(() => {
      toast.classList.add('opacity-0', 'translate-y-2');
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }
};
