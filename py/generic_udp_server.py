import socket
import win32file

if __name__ == "__main__":
    handle = win32file.CreateFile(
        r"\\.\MyDevice",
        win32file.GENERIC_READ | win32file.GENERIC_WRITE,
        0,
        None,
        win32file.OPEN_EXISTING,
        0,
        None,
    )

    try: 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind(("0.0.0.0", 13370))
        while True:
            data, addr = sock.recvfrom(4096)
            print("Received: ", data)
            win32file.WriteFile(handle, data, None)

    finally:
        win32file.CloseHandle(handle)