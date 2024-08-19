from abc import ABC, abstractmethod
from commands import SetDeviceCommand, ClearDeviceCommand, ByeCommand, SendInputCommand
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


class DriverManager(object):
    def __init__(self, communicator: BaseDriverCommunicator):
        self._communicator = communicator

    def set_device(self, report_desc: bytes, name: str = "Virtual HID Device", dev_id: int = 0):
        set_dev_cmd = SetDeviceCommand.build(dict(dev=dict(report_desc=report_desc, name=name), dev_id=dev_id))
        self._communicator.send(set_dev_cmd)

    def clear_device(self, dev_id: int = 0):
        clear_dev_cmd = ClearDeviceCommand.build(dict(dev_id=dev_id))
        self._communicator.send(clear_dev_cmd)
    
    def bye(self):
        bye_cmd = ByeCommand.build({})
        self._communicator.send(bye_cmd)

    def send_input(self, report: bytes, report_id: int = 0, dev_id: int = 0):
        send_cmd = SendInputCommand.build(dict(report=report, report_id=report_id, dev_id=dev_id))
        self._communicator.send(send_cmd)

    def __enter__(self):
        self._communicator.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._communicator.__exit__(exc_type, exc_val, exc_tb)