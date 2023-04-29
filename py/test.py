import IPython
import win32file
import struct

HID_REPORT = [
    0x5,
    0x1,  # USAGE_PAGE (Generic Desktop)
    0x9,
    0x4,  # USAGE (Joystick)
    0xA1,
    0x1,  # COLLECTION (Application)
    0x9,
    0x1,  #   USAGE (Pointer)
    0xA1,
    0x0,  #   COLLECTION (Physical)
    0x5,
    0x1,  #     USAGE_PAGE (Generic Desktop)
    0x9,
    0x30,  #     USAGE (X)
    0x15,
    0x0,  #     LOGICAL_MINIMUM (0)
    0x26,
    0xFF,
    0x3,  #     LOGICAL_MAXIMUM (1023)
    0x75,
    0x10,  #     REPORT_SIZE (16)
    0x95,
    0x1,  #     REPORT_COUNT (1)
    0x81,
    0x82,  #     Input (Data, Variable, Absolute, Volatile)     */
    0xC0,  #   END_COLLECTION
    0xC0,  # END_COLLECTION
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
