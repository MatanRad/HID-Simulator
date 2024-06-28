from driver_communicator import BaseDriverCommunicator, SocketDriverCommunicator, DirectDriverCommunicator
from commands import SetDeviceCommand, ClearDeviceCommand, ByeCommand


class DriverManager(object):
    def __init__(self, communicator: BaseDriverCommunicator):
        self._communicator = communicator

    def set_device(self, report_desc: bytes):
        set_dev_cmd = SetDeviceCommand.build(dict(dev=dict(report_desc=report_desc)))
        self._communicator.send(set_dev_cmd)

    def clear_device(self):
        clear_dev_cmd = ClearDeviceCommand.build({})
        self._communicator.send(clear_dev_cmd)
    
    def bye(self):
        bye_cmd = ByeCommand.build({})
        self._communicator.send(bye_cmd)

    def __enter__(self):
        self._communicator.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._communicator.__exit__(exc_type, exc_val, exc_tb)


if __name__ == "__main__":
    with DriverManager(SocketDriverCommunicator("192.168.40.128")) as d:
        import IPython
        IPython.embed()