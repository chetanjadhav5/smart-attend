import os
import smtplib
import socket
import ssl
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv(override=True)


class EmailService:
    """Enterprise SMTP Email Service for RaiSakshya Smart Attendance System.
    Connects to Google SMTP server and dispatches authenticated OTP emails."""

    def __init__(self):
        self.load_config()

    def load_config(self):
        load_dotenv(override=True)
        self.smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com").strip()
        self.smtp_port = int(os.environ.get("SMTP_PORT", 587))
        self.smtp_user = os.environ.get("SMTP_USER", "").strip()
        # Clean spaces from Google App Password
        raw_pass = os.environ.get("SMTP_PASS", "")
        self.smtp_pass = raw_pass.replace(" ", "").strip()
        self.smtp_from = os.environ.get("SMTP_FROM", f"RaiSakshya Attendance <{self.smtp_user}>").strip()

    def _get_ipv4_connection(self):
        """Forces IPv4 connection to prevent Windows IPv6 connection reset issues with Gmail."""
        orig_getaddrinfo = socket.getaddrinfo

        def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
            return orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

        try:
            socket.getaddrinfo = getaddrinfo_ipv4
            if self.smtp_port == 465:
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context, timeout=15)
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15)
                server.ehlo()
                server.starttls()
                server.ehlo()

            server.login(self.smtp_user, self.smtp_pass)
            return server
        finally:
            socket.getaddrinfo = orig_getaddrinfo

    def test_connection(self):
        """Tests SMTP authentication with Google account."""
        self.load_config()
        try:
            server = self._get_ipv4_connection()
            server.quit()
            return {
                "success": True,
                "message": f"Successfully connected and authenticated with {self.smtp_host} as {self.smtp_user}."
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"SMTP Authentication failed: {str(e)}"
            }

    def generate_otp_html(self, to_email: str, otp_code: str, purpose: str = "Account Verification") -> str:
        """Generates an elegant, responsive HTML email template for OTP."""
        return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Verification Code - RaiSakshya</title>
</head>
<body style="margin: 0; padding: 0; background-color: #F1F5F9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #F1F5F9; padding: 40px 15px;">
    <tr>
      <td align="center">
        <!-- Main Card -->
        <table role="presentation" width="100%" style="max-width: 540px; background-color: #FFFFFF; border-radius: 28px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01); border: 1px solid #E2E8F0; overflow: hidden;" cellspacing="0" cellpadding="0">
          
          <!-- Header Banner -->
          <tr>
            <td style="background: linear-gradient(135deg, #0B1522 0%, #162438 100%); padding: 36px 32px 30px 32px; text-align: center;">
              <table role="presentation" align="center" cellspacing="0" cellpadding="0">
                <tr>
                  <td style="width: 44px; height: 44px; background-color: rgba(0, 196, 140, 0.15); border: 1px solid rgba(0, 196, 140, 0.4); border-radius: 14px; text-align: center; vertical-align: middle;">
                    <span style="font-size: 22px; line-height: 44px; display: inline-block;">🛡️</span>
                  </td>
                  <td style="padding-left: 14px; text-align: left;">
                    <span style="color: #FFFFFF; font-size: 20px; font-weight: 800; letter-spacing: -0.5px; display: block;">RaiSakshya</span>
                    <span style="color: #65FCBF; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; display: block;">Smart Attendance Intelligence</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Content Body -->
          <tr>
            <td style="padding: 36px 36px 28px 36px;">
              <h2 style="color: #0F172A; font-size: 20px; font-weight: 800; margin: 0 0 12px 0; letter-spacing: -0.3px;">
                One-Time Verification Code
              </h2>
              <p style="color: #475569; font-size: 14px; line-height: 1.6; margin: 0 0 24px 0;">
                Hello, we received a request for <strong>{purpose}</strong> associated with <span style="color: #0284C7; font-weight: 600;">{to_email}</span>. Use the security code below to proceed:
              </p>

              <!-- OTP Code Display Card -->
              <div style="background-color: #F8FAFC; border: 2px dashed #CBD5E1; border-radius: 20px; padding: 24px 20px; text-align: center; margin: 24px 0;">
                <span style="display: block; color: #64748B; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px;">
                  Your 6-Digit Passcode
                </span>
                <span style="display: inline-block; font-size: 36px; font-weight: 900; color: #0B1522; letter-spacing: 8px; font-family: 'Courier New', Courier, monospace; background: #FFFFFF; padding: 10px 24px; border-radius: 12px; border: 1px solid #E2E8F0; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);">
                  {otp_code}
                </span>
                <div style="margin-top: 14px;">
                  <span style="display: inline-block; background-color: #FEF3C7; color: #92400E; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 9999px; border: 1px solid #FDE68A;">
                    ⏱️ Valid for 10 minutes only
                  </span>
                </div>
              </div>

              <!-- Security Notice -->
              <div style="background-color: #F0FDF4; border-left: 4px solid #00C48C; padding: 14px 16px; border-radius: 0 12px 12px 0; margin-bottom: 24px;">
                <p style="color: #166534; font-size: 12px; line-height: 1.5; margin: 0;">
                  <strong>Security Reminder:</strong> Never share this code with anyone. RaiSakshya staff or faculty will never ask for your one-time password.
                </p>
              </div>

              <p style="color: #94A3B8; font-size: 12px; line-height: 1.5; margin: 0;">
                If you did not request this verification code, you can safely ignore this email or review your account activity.
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #F8FAFC; border-top: 1px solid #F1F5F9; padding: 20px 36px; text-align: center;">
              <p style="color: #94A3B8; font-size: 11px; line-height: 1.5; margin: 0;">
                © 2026 RaiSakshya College of Engineering &amp; Technology<br>
                Automated Facial Biometric Attendance &amp; Identity System
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    def send_otp_email(self, to_email: str, otp_code: str, purpose: str = "Account Verification", async_send: bool = False):
        """Sends an authenticated OTP email to the recipient via Google SMTP server."""
        if async_send:
            thread = threading.Thread(
                target=self._send_email_worker,
                args=(to_email, otp_code, purpose)
            )
            thread.daemon = True
            thread.start()
            return True, "Email dispatch initiated asynchronously."

        return self._send_email_worker(to_email, otp_code, purpose)

    def _send_email_worker(self, to_email: str, otp_code: str, purpose: str = "Account Verification"):
        self.load_config()
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Your RaiSakshya Verification Code: {otp_code}"
            msg["From"] = self.smtp_from
            msg["To"] = to_email

            # Plain text fallback
            text_content = (
                f"RaiSakshya Smart Attendance System\n\n"
                f"Your one-time verification code for {purpose} is: {otp_code}\n\n"
                f"This code will expire in 10 minutes.\n"
                f"If you did not request this, please ignore this email."
            )

            # HTML content
            html_content = self.generate_otp_html(to_email, otp_code, purpose)

            msg.attach(MIMEText(text_content, "plain", "utf-8"))
            msg.attach(MIMEText(html_content, "html", "utf-8"))

            server = self._get_ipv4_connection()
            server.sendmail(self.smtp_user, [to_email], msg.as_string())
            server.quit()

            print(f"[EmailService] OTP email successfully delivered to {to_email} via Google SMTP.")
            return True, f"OTP sent to {to_email}"

        except Exception as e:
            err_msg = f"[EmailService Error] Failed to send email to {to_email}: {str(e)}"
            print(err_msg)
            return False, str(e)


# Global singleton instance
email_service = EmailService()
