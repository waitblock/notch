# -*- encoding: utf-8 -*-

# ssl-check.py revision 9 by gdamjan
# last modified July 12, 2021
# source file link: https://gist.githubusercontent.com/gdamjan/55a8b9eec6cf7b771f92021d93b87b2c/raw/d8dc194ec4d0187f985a57138019d04e3a59b51f/ssl-check.py


from OpenSSL import SSL
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna
import concurrent.futures

from socket import socket
from socket import gaierror
from collections import namedtuple

HostInfo = namedtuple(field_names='cert hostname peername', typename='HostInfo')


def verify_cert(cert, hostname):
    # verify notAfter/notBefore, CA trusted, servername/sni/hostname
    cert.has_expired()
    # service_identity.pyopenssl.verify_hostname(client_ssl, hostname)
    # issuer


def get_certificate(hostname, port):
    hostname_idna = idna.encode(hostname)
    sock = socket()

    sock.connect((hostname, port))
    peer_name = sock.getpeername()
    ctx = SSL.Context(SSL.SSLv23_METHOD) # most compatible
    ctx.check_hostname = False
    ctx.verify_mode = SSL.VERIFY_NONE

    sock_ssl = SSL.Connection(ctx, sock)
    sock_ssl.set_connect_state()
    sock_ssl.set_tlsext_host_name(hostname_idna)
    sock_ssl.do_handshake()
    cert = sock_ssl.get_peer_certificate()
    crypto_cert = cert.to_cryptography()
    sock_ssl.close()
    sock.close()

    return HostInfo(cert=crypto_cert, peername=peer_name, hostname=hostname)


def get_alt_names(cert):
    try:
        ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        return ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        return None


def get_common_name(cert):
    try:
        names = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None


def get_issuer(cert):
    try:
        names = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None


def print_basic_info(host_info):
    s = '''» {hostname} « … {peername}
    \tcommonName: {commonname}
    \tSAN: {SAN}
    \tissuer: {issuer}
    \tnotBefore: {notbefore}
    \tnotAfter:  {notafter}
    '''.format(
            hostname=host_info.hostname,
            peername=host_info.peername,
            commonname=get_common_name(host_info.cert),
            SAN=get_alt_names(host_info.cert),
            issuer=get_issuer(host_info.cert),
            notbefore=host_info.cert.not_valid_before,
            notafter=host_info.cert.not_valid_after
    )
    print(s)


def check_it_out(hostname, port):
    host_info = get_certificate(hostname, port)
    print_basic_info(host_info)


def main(hostname):
    host = [
        (hostname, 443),
    ]
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
            for host_info in e.map(lambda x: get_certificate(x[0], x[1]), host):
                print_basic_info(host_info)
    except SSL.Error:
        print("The hostname does not exist.")
    except idna.core.IDNAError:
        print("Empty domain.")
    except gaierror:
        print("The hostname does not exist.")
