import IPython
import win32file
import struct

HID_REPORT = [
    0x05,
    0x01,  # UsagePage(Generic Desktop[1])
    0x09,
    0x04,  # UsageId(Joystick[4])
    0xA1,
    0x01,  # Collection(Application)
    0x85,
    0x01,  #     ReportId(1)
    0x05,
    0x02,  #     UsagePage(Simulation Controls[2])
    0x09,
    0xB9,  #     UsageId(Elevator Trim[185])
    0x15,
    0x00,  #     LogicalMinimum(0)
    0x26,
    0xFF,
    0x03,  #     LogicalMaximum(1,023)
    0x95,
    0x01,  #     ReportCount(1)
    0x75,
    0x0A,  #     ReportSize(10)
    0x81,
    0x02,  #     Input(Data, Variable, Absolute, NoWrap, Linear, PreferredState, NoNullPosition, BitField)
    0x75,
    0x06,  #     ReportSize(6)
    0x81,
    0x03,  #     Input(Constant, Variable, Absolute, NoWrap, Linear, PreferredState, NoNullPosition, BitField)
    0xC0,  # EndCollection()
]

handle = None


class vhf_device_t:
    def __init__(self, report_desc_length, report_desc):
        self.handle = 0
        self.report_desc_length = report_desc_length
        self.report_desc = report_desc

    def pack(self):
        return struct.pack(
            "PH2048s", self.handle, self.report_desc_length, self.report_desc
        )

    @property
    def size(self):
        return struct.calcsize("PH2048s")


class command_set_dev_t:
    def __init__(self, dev: vhf_device_t):
        self.type = ord("s")
        self.dev = dev

    def pack(self):
        return struct.pack(f"B{self.dev.size}s", self.type, self.dev.pack())


class command_clear_dev_t:
    def __init__(self):
        self.type = ord("c")

    def pack(self):
        return struct.pack("B", self.type)


def echo_test():
    global handle
    while True:
        print("Input: ", end="")
        s = str(input()).strip()
        if s == "exit":
            break

        win32file.WriteFile(handle, s.encode("ascii"), None)
        data = win32file.ReadFile(handle, 4096, None)

        print(data[1].decode("utf-8"))


def set_dev():
    global handle
    dev = vhf_device_t(len(HID_REPORT), bytes(HID_REPORT))
    cmd = command_set_dev_t(dev)
    win32file.WriteFile(handle, cmd.pack(), None)


def clear_dev():
    global handle
    cmd = command_clear_dev_t()
    win32file.WriteFile(handle, cmd.pack(), None)


def main():
    global handle

    # Open the device symlink
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
        IPython.embed()
    finally:
        # Close the device handle
        win32file.CloseHandle(handle)


if __name__ == "__main__":
    main()
