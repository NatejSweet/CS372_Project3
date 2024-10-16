import socket
import time


def system_seconds_since_1900():
    seconds_delta = 2208988800
    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch
def get_NIST_time():
    s = socket.socket()

    remote = ('time.nist.gov', 37)
    s.connect(remote)
    print("Connected to server")

    data = s.recv(4)
    print("Received data:", data)

    s.close()

    NIST_time = int.from_bytes(data, byteorder='big')
    return NIST_time

NIST_time = get_NIST_time()
sys_time = system_seconds_since_1900()
print("NIST Time:", NIST_time)
print("System Time:", sys_time)