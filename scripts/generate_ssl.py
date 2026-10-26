#!/usr/bin/env python3
"""
RaiSakshya SSL Certificate Generator
Generates self-signed X.509 v3 SSL/TLS certificate and private key with SAN (Subject Alternative Name)
for EC2 public IP and localhost, enabling browser Secure Context (HTTPS) and unlocking camera/webcam access.
"""

import os
import sys
import datetime
import ipaddress
from dotenv import load_dotenv

# Try importing cryptography
try:
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
except ImportError:
    print("Error: 'cryptography' library is not installed.")
    print("Run: pip install cryptography")
    sys.exit(1)


def generate_self_signed_cert(
    cert_path="cert.pem",
    key_path="key.pem",
    ip_address=None,
    domain_name=None,
    valid_days=825
):
    """
    Generates cert.pem and key.pem containing Subject Alternative Name (SAN)
    for the specified IP address and localhost.
    """
    load_dotenv(override=True)
    if not ip_address:
        ip_address = os.environ.get("EC2_PUBLIC_IP", "3.110.208.141").strip()

    print(f"[*] Generating SSL Private Key and Certificate...")
    print(f"[*] Target Public IP: {ip_address}")

    # 1. Generate 2048-bit RSA Private Key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # 2. Build Subject & Issuer Information
    common_name = ip_address if ip_address else "localhost"
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Maharashtra"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Nashik"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "RaiSakshya Smart Attendance"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    # 3. Build Subject Alternative Names (SAN) - Essential for Chrome/Edge/Firefox
    san_list = [
        x509.DNSName("localhost"),
        x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        x509.IPAddress(ipaddress.IPv4Address("0.0.0.0"))
    ]

    if ip_address:
        try:
            san_list.append(x509.IPAddress(ipaddress.ip_address(ip_address)))
        except ValueError:
            san_list.append(x509.DNSName(ip_address))

    if domain_name:
        san_list.append(x509.DNSName(domain_name))

    # 4. Build X.509 v3 Certificate
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=valid_days))
        .add_extension(
            x509.SubjectAlternativeName(san_list),
            critical=False
        )
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True
        )
        .sign(private_key, hashes.SHA256())
    )

    # 5. Save Private Key (key.pem)
    key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(key_path, "wb") as f:
        f.write(key_bytes)

    # Restrict permissions on Unix/Linux
    try:
        os.chmod(key_path, 0o600)
    except Exception:
        pass

    # 6. Save Certificate (cert.pem)
    cert_bytes = cert.public_bytes(serialization.Encoding.PEM)
    with open(cert_path, "wb") as f:
        f.write(cert_bytes)

    print(f"[+] SSL Certificate created: {os.path.abspath(cert_path)}")
    print(f"[+] SSL Private Key created: {os.path.abspath(key_path)}")
    print(f"[+] SAN Entries: {[str(item.value) for item in san_list]}")
    print("\n" + "=" * 60)
    print(" SSL SETUP COMPLETE FOR CAMERA PERMISSIONS")
    print("=" * 60)
    print(f" Secure Access URL: https://{ip_address}:5000")
    print("\n Browser Instructions:")
    print(" 1. Open: https://" + ip_address + ":5000 in your browser")
    print(" 2. Click 'Advanced' -> 'Proceed to " + ip_address + " (unsafe)'")
    print(" 3. The browser will grant Secure Context and camera access will work!")
    print("=" * 60 + "\n")

    return cert_path, key_path


if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else None
    generate_self_signed_cert(ip_address=ip)
