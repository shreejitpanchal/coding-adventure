"""Generates (and caches) a self-signed TLS certificate for the browser
preview's HTTPS server -- see main_web.py. Not for the primary desktop
app, which has no network listener at all.

The certificate's Common Name is fixed at "coding-adventure" (not a real
hostname) since this only ever serves localhost/127.0.0.1 for local
browser previewing -- browsers will still show a one-time "not secure"
warning for it, since it's self-signed rather than issued by a trusted
CA, which is expected and fine for local-only use. The cert is cached in
the data directory (see platform_paths.py) and reused across runs,
regenerated automatically once it's within 7 days of expiring."""
from __future__ import annotations

import datetime
from pathlib import Path

from app.config.platform_paths import resolve_platform_data_dir

CERT_CN = "coding-adventure"
_VALIDITY_DAYS = 825  # under the ~825-day max most browsers accept for a leaf cert
_RENEW_WITHIN_DAYS = 7


def _cert_paths() -> tuple[Path, Path]:
    cert_dir = resolve_platform_data_dir() / "certs"
    cert_dir.mkdir(parents=True, exist_ok=True)
    return cert_dir / "coding-adventure.crt", cert_dir / "coding-adventure.key"


def _is_cert_still_valid(cert_path: Path) -> bool:
    from cryptography import x509

    try:
        cert = x509.load_pem_x509_certificate(cert_path.read_bytes())
    except (OSError, ValueError):
        return False

    expires_soon = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=_RENEW_WITHIN_DAYS)
    return cert.not_valid_after_utc > expires_soon


def _generate_cert(cert_path: Path, key_path: Path) -> None:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, CERT_CN)])
    now = datetime.datetime.now(datetime.timezone.utc)

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=_VALIDITY_DAYS))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName(CERT_CN),
                x509.IPAddress(__import__("ipaddress").ip_address("127.0.0.1")),
            ]),
            critical=False,
        )
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(key, hashes.SHA256())
    )

    key_path.write_bytes(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))


def ensure_self_signed_certificate() -> tuple[str, str]:
    """Returns (cert_path, key_path) as strings, generating a fresh
    self-signed certificate (CN=coding-adventure) if none is cached yet
    or the cached one is expired/near-expiry."""
    cert_path, key_path = _cert_paths()

    if not (cert_path.exists() and key_path.exists() and _is_cert_still_valid(cert_path)):
        _generate_cert(cert_path, key_path)

    return str(cert_path), str(key_path)
