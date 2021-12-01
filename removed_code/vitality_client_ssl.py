import requests

from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from requests_toolbelt.adapters.x509 import X509Adapter


from cryptography.hazmat.primitives.serialization import pkcs12



def decorate_session_with_sslX(session,p12_cert_file,p12_cert_file_password):
    with open(p12_cert_file ,"rb") as f:
        private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(f.read(), p12_cert_file_password.encode('utf8'))
    adapter = X509Adapter(max_retries=3, cert_bytes=cert_bytes, pk_bytes=pk_bytes, encoding=Encoding.DER)
    session.mount('https://', adapter)

def decorate_session_with_ssl(session,p12_cert_file,p12_cert_file_password,pool_connections, pool_maxsize):
    backend = default_backend()
    print(backend)
    with open(p12_cert_file, 'rb') as pkcs12_file:
        pkcs12_data = pkcs12_file.read()
    pkcs12_password_bytes = p12_cert_file_password.encode('utf8')
    pycaP12 = load_key_and_certificates(pkcs12_data, pkcs12_password_bytes, backend)
    cert_bytes = pycaP12[1].public_bytes(Encoding.DER)
    pk_bytes = pycaP12[0].private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption())
    adapter = X509Adapter(max_retries=1, cert_bytes=cert_bytes, pk_bytes=pk_bytes, encoding=Encoding.DER,pool_connections=pool_connections, pool_maxsize=pool_maxsize)
    session.mount('https://', adapter)
