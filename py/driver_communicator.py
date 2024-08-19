from abc import ABC, abstractmethod
import socket
import win32file

class BaseDriverCommunicator(ABC):
    @abstractmethod
    def send(self, data):
        pass

    @abstractmethod
    def receive(self):
        pass

    @abstractmethod
    def _start(self):
        pass

    @abstractmethod
    def _exit(self):
        pass

    def __enter__(self):
        self._start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._exit()

class SocketDriverCommunicator(BaseDriverCommunicator):
    def __init__(self, ip, port=13370):
        self.ip = ip
        self.port = port
        self._sock = None
    
    def _start(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    def _exit(self):
        self._sock.close()
        self._sock = None

    def send(self, data):
        self._sock.sendto(data, (self.ip, self.port))

    def receive(self):
        raise NotImplementedError()
    
class DirectDriverCommunicator(BaseDriverCommunicator):
    def __init__(self, path=r"\\.\MyDevice"):
        self._handle = None
    
    def _start(self):
        self._handle = win32file.CreateFile(
            r"\\.\MyDevice",
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None,
        )
    
    def _exit(self):
        self._handle.close()
        self._handle = None

    def send(self, data):
        win32file.WriteFile(self._handle, data, None)

    def receive(self):
        raise NotImplementedError()
    
