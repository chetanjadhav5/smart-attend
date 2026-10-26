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
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      console.warn("Camera API not supported in this browser. Using simulation.");
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
      console.warn("Could not access physical webcam:", err.message);
      this.updateStatus(false, "Camera standby / Simulation");
      return false;
    }
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
