
import socket
import ssl

hostname = "api.openai.com"

context = ssl.create_default_context()

try:
    with socket.create_connection((hostname, 443), timeout=15) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            print("SSL connection successful")
            print("Certificate issuer:")
            print(secure_sock.getpeercert().get("issuer"))

except Exception as e:
    print("SSL Error:", repr(e))
