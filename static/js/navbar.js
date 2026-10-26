// RaiSakshya Unified Navbar Component
// Warm Pastel Navbar (#DFBEB0) with Non-Straight Curved Bottom Wave
// Optical illusion: Upper wave matches navbar (#DFBEB0), lower wave matches page body (#E8EEF5)
// Only circular profile avatar shown, clicking it navigates to the user's profile section
// Perfectly aligned with global max-w-[1480px] layout

function renderGlobalNavbar(activePortal, activeTab) {
  const container = document.getElementById('global-navbar');
  if (!container) return;

  // Configuration for portals and their tabs
  const portalConfigs = {
    student: {
      name: "Student Portal",
      badgeText: "STUDENT",
      profileUrl: "/student/profile",
      tabs: [
        { id: "dashboard", label: "Dashboard", href: "/student/dashboard", icon: "fa-solid fa-chart-pie" },
        { id: "teachers", label: "Teachers", href: "/student/teachers", icon: "fa-solid fa-chalkboard-user" },
        { id: "subjects", label: "Subjects", href: "/student/subjects", icon: "fa-solid fa-book-open" }
      ]
    },
    teacher: {
      name: "Teacher Portal",
      badgeText: "TEACHER",
      profileUrl: "/teacher/profile",
      tabs: [
        { id: "dashboard", label: "Dashboard", href: "/teacher/dashboard", icon: "fa-solid fa-chart-pie" },
        { id: "take_attendance", label: "Take Attendance", href: "/teacher/take-attendance", icon: "fa-solid fa-camera" },
        { id: "students", label: "Students", href: "/teacher/daily-attendance", icon: "fa-solid fa-users" }
      ]
    },
    admin: {
      name: "Admin Portal",
      badgeText: "ADMIN",
      profileUrl: "/admin/settings",
      tabs: [
        { id: "dashboard", label: "Dashboard", href: "/admin/dashboard", icon: "fa-solid fa-chart-simple" },
        { id: "teachers", label: "Teachers", href: "/admin/teachers", icon: "fa-solid fa-users-rectangle" },
        { id: "settings", label: "Settings", href: "/admin/settings", icon: "fa-solid fa-gear" }
      ]
    }
  };

  const portalHomeUrls = {
    student: '/student/dashboard',
    teacher: '/teacher/dashboard',
    admin: '/admin/dashboard'
  };
  const homeUrl = portalHomeUrls[activePortal] || '/login';
  const currentConfig = portalConfigs[activePortal] || portalConfigs.teacher;
  const profileUrl = currentConfig.profileUrl || '/teacher/profile';

  // Check for custom institution logo
  let customLogo = null;
  try {
    if (typeof localStorage !== 'undefined') {
      customLogo = localStorage.getItem('custom_app_logo');
    }
  } catch(e) {}

  const logoIconHtml = customLogo 
    ? `<img src="${customLogo}" alt="Institution Logo" class="w-8 h-8 rounded-xl object-contain shadow-sm border border-black/10 bg-white/40">`
    : `<svg class="w-8 h-8 fill-current" viewBox="0 0 24 24"><path d="M12 3L1 9L12 15L21 10.09V17H23V9M5 13.18V17.18L12 21L19 17.18V13.18L12 17L5 13.18Z"></path></svg>`;

  // Container stays sticky at the very top of the window, spanning 100% width
  container.className = "sticky top-0 z-[99999] w-full block";

  container.innerHTML = `
    <header class="w-full select-none bg-transparent relative">
      
      <!-- Top Warm Pastel Sand/Clay Bar (Aligned with page content max-w-[1480px]) -->
      <div class="w-full relative z-30" style="background-color: #DFBEB0;">
        
        <!-- Corner Leaves Wrapper (overflow-hidden ONLY on decorative leaves, so dropdowns can overflow freely) -->
        <div class="absolute inset-0 overflow-hidden pointer-events-none z-10">
          <!-- Left Botanical Leaf Silhouette -->
          <div class="absolute left-0 top-0 h-full opacity-75 hidden sm:block">
            <svg class="h-full w-auto max-w-[130px]" viewBox="0 0 160 90" fill="#3D4A40">
              <path d="M0,0 C15,20 35,45 60,65 C70,72 85,78 100,82 C92,75 80,68 70,60 C50,42 25,18 0,0 Z"/>
              <path d="M18,12 C28,10 40,16 42,26 C43,35 32,40 22,35 C15,30 14,18 18,12 Z"/>
              <path d="M35,28 C48,25 60,32 62,42 C64,52 52,58 40,53 C32,48 30,34 35,28 Z"/>
              <path d="M55,45 C70,42 82,50 84,60 C85,69 74,75 62,70 C53,65 50,52 55,45 Z"/>
              <path d="M28,35 C24,46 16,55 8,56 C2,56 0,48 4,38 C8,28 20,28 28,35 Z"/>
              <path d="M48,52 C42,64 34,72 26,73 C20,73 18,65 22,55 C26,46 38,45 48,52 Z"/>
              <path d="M85,68 C102,68 115,76 116,84 C117,90 108,93 96,89 C86,85 82,74 85,68 Z"/>
            </svg>
          </div>

          <!-- Right Botanical Leaf Silhouette -->
          <div class="absolute right-0 top-0 h-full opacity-75 hidden sm:block">
            <svg class="h-full w-auto max-w-[130px] scale-x-[-1]" viewBox="0 0 160 90" fill="#3D4A40">
              <path d="M0,0 C15,20 35,45 60,65 C70,72 85,78 100,82 C92,75 80,68 70,60 C50,42 25,18 0,0 Z"/>
              <path d="M18,12 C28,10 40,16 42,26 C43,35 32,40 22,35 C15,30 14,18 18,12 Z"/>
              <path d="M35,28 C48,25 60,32 62,42 C64,52 52,58 40,53 C32,48 30,34 35,28 Z"/>
              <path d="M55,45 C70,42 82,50 84,60 C85,69 74,75 62,70 C53,65 50,52 55,45 Z"/>
              <path d="M28,35 C24,46 16,55 8,56 C2,56 0,48 4,38 C8,28 20,28 28,35 Z"/>
              <path d="M48,52 C42,64 34,72 26,73 C20,73 18,65 22,55 C26,46 38,45 48,52 Z"/>
              <path d="M85,68 C102,68 115,76 116,84 C117,90 108,93 96,89 C86,85 82,74 85,68 Z"/>
            </svg>
          </div>
        </div>

        <div class="w-full max-w-[1480px] mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between relative z-20">
          
          <!-- Left: Brand Logo & Title -->
          <a href="${homeUrl}" class="flex items-center gap-3 group cursor-pointer select-none shrink-0 outline-none focus:outline-none">
            <div id="nav-brand-logo-container" class="text-[#1E1E1E] text-2xl shrink-0 flex items-center justify-center group-hover:scale-105 transition-transform">
              ${logoIconHtml}
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h1 class="text-lg md:text-xl font-black tracking-tight text-[#1E1E1E] leading-none">RaiSakshya</h1>
                <span class="text-[10px] font-black text-white tracking-widest uppercase leading-none px-2.5 py-0.5 rounded-full bg-[#38332E] shadow-sm">
                  ${currentConfig.badgeText || activePortal}
                </span>
              </div>
              <p class="text-[11px] text-[#544D46] font-semibold leading-none mt-1 tracking-tight">Smart Attendance for Brighter Futures</p>
            </div>
          </a>

          <!-- Center: Dynamic Navigation Tabs (NO round shapes, illuminated text) -->
          <nav class="hidden lg:flex items-center gap-8 relative" data-purpose="main-navigation">
            ${currentConfig.tabs.map(tab => {
              const isActive = 
                (tab.id === activeTab) ||
                (activePortal === 'admin' && tab.id === 'teachers' && ['teachers', 'teachers_attendance', 'teacher_requests'].includes(activeTab)) ||
                (activePortal === 'teacher' && tab.id === 'students' && ['students', 'daily_attendance', 'all_days', 'student_profile', 'student_requests'].includes(activeTab)) ||
                (activePortal === 'student' && tab.id === 'teachers' && ['teachers', 'teacher_profile'].includes(activeTab));

              if (isActive) {
                return `
                  <a href="${tab.href}" class="flex items-center gap-2 text-xs md:text-sm font-black text-[#111111] py-1 px-1 transition-all outline-none focus:outline-none drop-shadow-[0_1px_1px_rgba(255,255,255,0.7)]">
                    <i class="${tab.icon} text-sm text-[#111111]"></i>
                    <span class="tracking-wide">${tab.label}</span>
                  </a>
                `;
              } else {
                return `
                  <a href="${tab.href}" class="flex items-center gap-2 text-xs md:text-sm font-bold text-[#453D37] hover:text-[#111111] py-1 px-1 transition-colors group outline-none focus:outline-none">
                    <i class="${tab.icon} text-sm text-[#61574F] group-hover:text-[#111111] transition-colors"></i>
                    <span class="tracking-wide">${tab.label}</span>
                  </a>
                `;
              }
            }).join('')}
          </nav>

          <!-- Right: Switch Portal, Notifications, Pure Profile Avatar, and Logout Symbol -->
          <div class="flex items-center gap-5 sm:gap-6 shrink-0 relative z-30">
            
            <!-- Switch Portal Dropdown -->
            <div class="relative" id="portal-switcher-dropdown">
              <button onclick="togglePortalMenu(event)" type="button" class="flex items-center gap-2 text-xs md:text-sm font-bold text-[#2E2722] hover:text-[#111111] transition-colors cursor-pointer py-1 px-1 bg-transparent border-none outline-none focus:outline-none">
                <i class="fa-solid fa-arrows-split-up-and-left text-sm text-[#38332E]"></i>
                <span class="hidden md:inline">Switch Portal</span>
                <i class="fa-solid fa-chevron-down text-[10px] text-[#544D46]"></i>
              </button>
              
              <!-- Floating Portal Menu (with high z-index and clear positioning) -->
              <div id="portal-menu" class="hidden absolute right-0 mt-3 w-64 bg-[#141B22] border border-slate-700 shadow-2xl p-2.5 z-[999999] flex flex-col gap-1 ring-1 ring-black/80 backdrop-blur-xl rounded-2xl">
                <div class="text-[10px] font-extrabold text-slate-400 px-3 py-1.5 uppercase tracking-wider">Select Portal View</div>
                <button type="button" onclick="handlePortalSwitch('student', '/student/dashboard')" class="w-full flex items-center justify-between px-3 py-2 text-xs font-bold text-slate-200 hover:text-[#00DFBA] hover:bg-white/5 rounded-xl transition-colors text-left cursor-pointer">
                  <span class="flex items-center gap-2.5"><i class="fa-solid fa-user-graduate text-[#00DFBA]"></i> Student Portal</span>
                  ${activePortal === 'student' ? '<i class="fa-solid fa-check text-[#00DFBA] text-xs"></i>' : ''}
                </button>
                <button type="button" onclick="handlePortalSwitch('teacher', '/teacher/dashboard')" class="w-full flex items-center justify-between px-3 py-2 text-xs font-bold text-slate-200 hover:text-indigo-400 hover:bg-white/5 rounded-xl transition-colors text-left cursor-pointer">
                  <span class="flex items-center gap-2.5"><i class="fa-solid fa-chalkboard-user text-indigo-400"></i> Teacher Portal</span>
                  ${activePortal === 'teacher' ? '<i class="fa-solid fa-check text-indigo-400 text-xs"></i>' : ''}
                </button>
                <button type="button" onclick="handlePortalSwitch('admin', '/admin/dashboard')" class="w-full flex items-center justify-between px-3 py-2 text-xs font-bold text-slate-200 hover:text-rose-400 hover:bg-white/5 rounded-xl transition-colors text-left cursor-pointer">
                  <span class="flex items-center gap-2.5"><i class="fa-solid fa-shield-halved text-rose-400"></i> Admin Portal</span>
                  ${activePortal === 'admin' ? '<i class="fa-solid fa-check text-rose-400 text-xs"></i>' : ''}
                </button>
                <div class="border-t border-white/10 my-1"></div>
                <a href="/login" onclick="closeAllMenus()" class="flex items-center gap-2.5 px-3 py-2 text-xs font-bold text-amber-300 hover:text-amber-200 hover:bg-white/5 rounded-xl transition-colors">
                  <i class="fa-solid fa-right-to-bracket text-amber-400"></i> Login & Register Pages
                </a>
              </div>
            </div>

            <!-- Notification Bell with Red Badge -->
            <button onclick="API.showToast('1 new attendance notification: Live session active', 'info')" aria-label="Notifications" class="relative text-[#2E2722] hover:text-[#111111] transition-colors cursor-pointer p-1 bg-transparent border-none outline-none focus:outline-none" type="button">
              <i class="fa-regular fa-bell text-lg"></i>
              <span class="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-[#EF4444] text-white text-[9px] font-black flex items-center justify-center ring-2 ring-[#DFBEB0] shadow-sm">1</span>
            </button>

            <!-- User Profile Avatar Button (ONLY profile picture shown, click navigates to user's profile section) -->
            <a href="${profileUrl}" id="navbar-profile-btn" title="View & Edit My Profile" class="relative group cursor-pointer select-none inline-block outline-none focus:outline-none transition-transform hover:scale-105 active:scale-95 shrink-0">
              <img id="nav-user-avatar" alt="My Profile Avatar" class="w-9 h-9 sm:w-10 sm:h-10 rounded-full object-cover ring-2 ring-white/90 shadow-md group-hover:ring-[#1E1E1E] transition-all" src="/static/teacher_faces/308cb046-f220-4dba-a871-63cdef5a258c.png">
              <span class="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full bg-emerald-500 ring-2 ring-[#DFBEB0]"></span>
            </a>

            <!-- Logout Symbol (ONLY the symbol at the end of the navbar) -->
            <a href="/login" onclick="logoutSession(event)" title="Sign Out / Logout" class="text-[#2E2722] hover:text-rose-600 transition-colors p-1 flex items-center justify-center outline-none focus:outline-none shrink-0 cursor-pointer" aria-label="Sign Out">
              <i class="fa-solid fa-arrow-right-from-bracket text-base"></i>
            </a>

            <!-- Mobile & Tablet Navigation Hamburger Button -->
            <button onclick="toggleMobileNav(event)" type="button" class="lg:hidden flex items-center justify-center w-8 h-8 rounded-xl bg-black/10 hover:bg-black/15 text-[#1E1E1E] transition cursor-pointer outline-none focus:outline-none ml-1" aria-label="Toggle Navigation Menu">
              <i id="mobile-nav-icon" class="fa-solid fa-bars text-sm"></i>
            </button>

          </div>
        </div>

        <!-- Mobile & Tablet Navigation Tray -->
        <div id="mobile-nav-drawer" class="hidden lg:hidden w-full px-4 sm:px-6 py-3 border-t border-black/10 relative z-30 shadow-inner" style="background-color: #D6B2A3;">
          <div class="flex items-center justify-between text-[10px] font-black uppercase tracking-wider text-[#3D352F] mb-2 px-1">
            <span>Navigation Menu</span>
            <span class="text-[9px] px-2 py-0.5 rounded-full bg-black/10">${currentConfig.badgeText || activePortal}</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-1.5">
            ${currentConfig.tabs.map(tab => {
              const isActive = 
                (tab.id === activeTab) ||
                (activePortal === 'admin' && tab.id === 'teachers' && ['teachers', 'teachers_attendance', 'teacher_requests'].includes(activeTab)) ||
                (activePortal === 'teacher' && tab.id === 'students' && ['students', 'daily_attendance', 'all_days', 'student_profile', 'student_requests'].includes(activeTab)) ||
                (activePortal === 'student' && tab.id === 'teachers' && ['teachers', 'teacher_profile'].includes(activeTab));

              const activeClasses = isActive 
                ? 'bg-black/20 text-[#111111] font-black shadow-inner' 
                : 'text-[#3E3630] font-bold hover:bg-black/10 hover:text-[#111111]';

              return `
                <a href="${tab.href}" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs ${activeClasses} transition">
                  <i class="${tab.icon} text-sm"></i>
                  <span class="tracking-wide">${tab.label}</span>
                  ${isActive ? '<i class="fa-solid fa-check ml-auto text-xs text-[#111111]"></i>' : ''}
                </a>
              `;
            }).join('')}
          </div>
        </div>

      </div>

      <!-- Organic Non-Straight Wave Divider -->
      <!-- Simulates non-straight curved navbar effect seamlessly with transparent lower region matching underlying page body -->
      <div class="w-full overflow-hidden leading-none select-none pointer-events-none">
        <svg class="w-full h-7 sm:h-9 md:h-11 block" viewBox="0 0 1440 60" fill="none" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
          <!-- Upper region: fills from top down to the curve with exact Navbar Sand/Clay color -->
          <path d="M 0,0 L 0,26 C 160,38 320,52 500,50 C 680,48 820,30 1000,32 C 1160,34 1300,48 1440,40 L 1440,0 Z" fill="#DFBEB0"/>
        </svg>
      </div>

    </header>
  `;

  // Fetch current user and sync navbar profile avatar
  if (typeof API !== 'undefined' && API.getCurrentUser) {
    API.getCurrentUser().then(res => {
      if (res && res.user) {
        const u = res.user;
        const avatarEl = document.getElementById('nav-user-avatar');
        const profileBtn = document.getElementById('navbar-profile-btn');

        if (avatarEl && u.avatar) avatarEl.src = u.avatar;
        
        // Ensure profile link targets user's role profile section
        if (profileBtn) {
          if (res.role === 'student') {
            profileBtn.href = '/student/profile';
            profileBtn.title = `${u.name || 'Student'} - My Profile & Approval Status`;
          } else if (res.role === 'teacher') {
            profileBtn.href = '/teacher/profile';
            profileBtn.title = `${u.name || 'Teacher'} - My Teacher Profile`;
          } else if (res.role === 'admin') {
            profileBtn.href = '/admin/settings';
            profileBtn.title = `${u.name || 'Admin'} - Admin Settings & Profile`;
          }
        }
      }
    });
  }

  // Also check backend settings for custom logo if not cached in localStorage
  if (!customLogo && typeof API !== 'undefined' && API.getSettings) {
    API.getSettings().then(s => {
      if (s && s.logo_url) {
        try { localStorage.setItem('custom_app_logo', s.logo_url); } catch(e) {}
        const logoCont = document.getElementById('nav-brand-logo-container');
        if (logoCont) {
          logoCont.innerHTML = `<img src="${s.logo_url}" alt="Institution Logo" class="w-8 h-8 rounded-xl object-contain shadow-sm border border-black/10 bg-white/40">`;
        }
      }
    }).catch(() => {});
  }
}

function closeAllMenus() {
  const p = document.getElementById('portal-menu');
  if (p) p.classList.add('hidden');
  const d = document.getElementById('mobile-nav-drawer');
  if (d) d.classList.add('hidden');
  const icon = document.getElementById('mobile-nav-icon');
  if (icon) icon.className = 'fa-solid fa-bars text-sm';
}

function toggleMobileNav(e) {
  if (e) e.stopPropagation();
  const drawer = document.getElementById('mobile-nav-drawer');
  const icon = document.getElementById('mobile-nav-icon');
  if (drawer) {
    drawer.classList.toggle('hidden');
    const isOpen = !drawer.classList.contains('hidden');
    if (icon) {
      icon.className = isOpen ? 'fa-solid fa-xmark text-sm' : 'fa-solid fa-bars text-sm';
    }
  }
}

function togglePortalMenu(e) {
  if (e) e.stopPropagation();
  const menu = document.getElementById('portal-menu');
  if (menu) menu.classList.toggle('hidden');
}

// Close dropdowns on outside click
document.addEventListener('click', (e) => {
  const pDrop = document.getElementById('portal-switcher-dropdown');
  const pMenu = document.getElementById('portal-menu');
  if (pDrop && pMenu && !pDrop.contains(e.target)) pMenu.classList.add('hidden');

  const mDrawer = document.getElementById('mobile-nav-drawer');
  const mBtn = document.getElementById('mobile-nav-icon');
  if (mDrawer && !mDrawer.contains(e.target) && (!mBtn || !mBtn.contains(e.target))) {
    mDrawer.classList.add('hidden');
    if (mBtn) mBtn.className = 'fa-solid fa-bars text-sm';
  }
});

async function handlePortalSwitch(role, redirectUrl) {
  closeAllMenus();
  try {
    if (typeof API !== 'undefined' && API.switchUser) {
      await API.switchUser(role);
    }
  } catch(e) {
    console.error("Portal switch error:", e);
  }
  const fallbackUrl = (role === 'student') ? '/student/dashboard' : ((role === 'teacher') ? '/teacher/daily-attendance' : '/admin/dashboard');
  window.location.href = redirectUrl || fallbackUrl;
}

async function switchNavbarRole(role) {
  return handlePortalSwitch(role);
}

function logoutSession(e) {
  if (e) e.preventDefault();
  closeAllMenus();
  if (typeof API !== 'undefined' && API.showToast) {
    API.showToast("Signed out successfully", "info");
  }
  setTimeout(() => {
    window.location.href = '/login';
  }, 250);
}

