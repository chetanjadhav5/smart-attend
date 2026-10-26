// RaiSakshya Camera & Face Scanner Controller

class CameraController {
  constructor(videoElementId, canvasElementId, statusBadgeId) {
    this.video = document.getElementById(videoElementId);
    this.canvas = document.getElementById(canvasElementId) || document.createElement('canvas');
    this.statusBadge = document.getElementById(statusBadgeId);
    this.stream = null;
    this.isStreaming = false;
  }

  async startCamera() {
    // Check if browser context is insecure (browsers block getUserMedia on plain HTTP for external IPs)
    if (!window.isSecureContext && window.location.protocol === 'http:' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
      console.warn("Camera blocked by browser: navigator.mediaDevices requires a Secure Context (HTTPS).");
      this.showHttpsPrompt();
      this.updateStatus(false, "Requires HTTPS");
      return false;
    }

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      console.warn("Camera API not supported or disabled in this browser context.");
      if (window.location.protocol === 'http:') {
        this.showHttpsPrompt();
      }
      this.updateStatus(false, "Simulation Mode");
      return false;
    }

    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user'
        },
        audio: false
      });

      if (this.video) {
        this.video.srcObject = this.stream;
        await this.video.play();
        this.isStreaming = true;
        this.updateStatus(true, "Camera ready");
      }
      return true;
    } catch (err) {
      console.warn("Could not access physical webcam:", err.name, err.message);
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        this.updateStatus(false, "Permission Denied");
        this.showPermissionPrompt();
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        this.updateStatus(false, "No camera found");
      } else {
        this.updateStatus(false, "Camera standby / Simulation");
      }
      return false;
    }
  }

  showHttpsPrompt() {
    if (document.getElementById('https-camera-prompt')) return;
    const httpsUrl = `https://${window.location.hostname}:5000${window.location.pathname}${window.location.search}`;
    const banner = document.createElement('div');
    banner.id = 'https-camera-prompt';
    banner.className = 'fixed top-4 left-1/2 -translate-x-1/2 z-50 max-w-xl w-[90%] p-4 bg-slate-900/95 text-white border border-amber-500/50 rounded-2xl shadow-2xl backdrop-blur-md flex items-center justify-between gap-4 animate-in fade-in slide-in-from-top-4 duration-300';
    banner.innerHTML = `
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center shrink-0">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <div>
          <div class="text-sm font-semibold text-amber-300">Camera Requires Secure HTTPS</div>
          <div class="text-xs text-slate-300">Modern browsers block webcam access on HTTP. Switch to HTTPS to open the camera.</div>
        </div>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <a href="${httpsUrl}" class="px-3.5 py-1.5 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-slate-950 font-semibold text-xs rounded-lg transition-all shadow-md">
          Open HTTPS
        </a>
        <button onclick="document.getElementById('https-camera-prompt').remove()" class="p-1 text-slate-400 hover:text-white rounded-lg">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
    `;
    document.body.appendChild(banner);
  }

  showPermissionPrompt() {
    if (document.getElementById('perm-camera-prompt')) return;
    const banner = document.createElement('div');
    banner.id = 'perm-camera-prompt';
    banner.className = 'fixed top-4 left-1/2 -translate-x-1/2 z-50 max-w-xl w-[90%] p-4 bg-slate-900/95 text-white border border-rose-500/50 rounded-2xl shadow-2xl backdrop-blur-md flex items-center justify-between gap-4 animate-in fade-in slide-in-from-top-4 duration-300';
    banner.innerHTML = `
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-rose-500/20 text-rose-400 flex items-center justify-center shrink-0">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
          </svg>
        </div>
        <div>
          <div class="text-sm font-semibold text-rose-300">Camera Permission Blocked</div>
          <div class="text-xs text-slate-300">Click the camera or lock icon in your browser's address bar and set Camera to "Allow", then reload.</div>
        </div>
      </div>
      <button onclick="document.getElementById('perm-camera-prompt').remove()" class="p-1 text-slate-400 hover:text-white rounded-lg shrink-0">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>
    `;
    document.body.appendChild(banner);
  }

  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
    this.isStreaming = false;
    this.updateStatus(false, "Camera off");
  }

  updateStatus(active, text) {
    if (!this.statusBadge) return;
    const dot = this.statusBadge.querySelector('.status-dot');
    const label = this.statusBadge.querySelector('.status-text');
    if (dot) {
      dot.className = `status-dot w-2.5 h-2.5 rounded-full ${active ? 'bg-emerald-500 animate-pulse' : 'bg-amber-400'}`;
    }
    if (label) {
      label.textContent = text;
    }
  }

  captureSnapshotBase64() {
    if (this.isStreaming && this.video) {
      const width = this.video.videoWidth || 640;
      const height = this.video.videoHeight || 480;
      this.canvas.width = width;
      this.canvas.height = height;
      const ctx = this.canvas.getContext('2d');
      ctx.drawImage(this.video, 0, 0, width, height);
      return this.canvas.toDataURL('image/jpeg', 0.85);
    }

    // If camera stream not active, generate a clean sample snapshot from face
    return null;
  }
}
