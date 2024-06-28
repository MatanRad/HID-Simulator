from driver_communicator import BaseDriverCommunicator, SocketDriverCommunicator, DirectDriverCommunicator
from commands import SetDeviceCommand, ClearDeviceCommand, ByeCommand, SendInputCommand

JOYSTICK_REPORT = bytes([
	0x05, 0x01,          # Usage Page (Generic Desktop)                       */
	0x09, 0x04,          # Usage (Joystick)                                   */
	0xa1, 0x01,          # Collection (Application)                           */
	0x09, 0x01,          #   Usage (Pointer)                                  */
	0xa1, 0x00,          #   Collection (Physical)                            */
	0x05, 0x01,          #     Usage Page (Generic Desktop)                   */
	0x09, 0x30,          #     Usage (X)                                      */
	0x09, 0x31,          #     Usage (Y)                                      */
	0x15, 0x9c,          #     Logical Minimum (-100)                         */
	0x25, 0x64,          #     Logical Maximum (100)                          */
	0x75, 0x08,          #     Report Size (8)                                */
	0x95, 0x02,          #     Report Count (2)                               */
	0x81, 0x82,          #     Input (Data, Variable, Absolute, Volatile)     */
	0xc0,                #   End Collection                                   */
	0x05, 0x09,          #   Usage Page (Button)                              */
	0x09, 0x02,          #   Usage (Button 2)                                 */
	0x09, 0x01,          #   Usage (Button 1)                                 */
	0x15, 0x00,          #   Logical Minimum (0)                              */
	0x25, 0x01,          #   Logical Maximum (1)                              */
	0x75, 0x01,          #   Report Size (1)                                  */
	0x95, 0x02,          #   Report Count (2)                                 */
	0x81, 0x02,          #   Input (Data, Variable, Absolute)                 */
	0x75, 0x06,          #   Report Size (6)                                  */
	0x95, 0x01,          #   Report Count (1)                                 */
	0x81, 0x01,          #   Input (Constant)                                 */
	0xc0                 # End Collection                                     */
])

MODIFIED_JOYSTICK_REPORT = bytes([
	0x05, 0x01,          # Usage Page (Generic Desktop)                       */
	0x09, 0x04,          # Usage (Joystick)                                   */
	0xa1, 0x01,          # Collection (Application)                           */
	0x09, 0x01,          #   Usage (Pointer)                                  */
	0xa1, 0x00,          #   Collection (Physical)                            */
	0x05, 0x01,          #     Usage Page (Generic Desktop)                   */
	0x09, 0x30,          #     Usage (X)                                      */
	# 0x09, 0x31,          #     Usage (Y)                                      */
	0x15, 0x9c,          #     Logical Minimum (-100)                         */
	0x25, 0x64,          #     Logical Maximum (100)                          */
	0x75, 0x08,          #     Report Size (8)                                */
	0x95, 0x01,          #     Report Count (1)                               */
	0x81, 0x82,          #     Input (Data, Variable, Absolute, Volatile)     */
	0xc0,                #   End Collection                                   */
	# 0x05, 0x09,          #   Usage Page (Button)                              */
	# 0x09, 0x02,          #   Usage (Button 2)                                 */
	# 0x09, 0x01,          #   Usage (Button 1)                                 */
	# 0x15, 0x00,          #   Logical Minimum (0)                              */
	# 0x25, 0x01,          #   Logical Maximum (1)                              */
	# 0x75, 0x01,          #   Report Size (1)                                  */
	# 0x95, 0x02,          #   Report Count (2)                                 */
	# 0x81, 0x02,          #   Input (Data, Variable, Absolute)                 */
	# 0x75, 0x06,          #   Report Size (6)                                  */
	# 0x95, 0x01,          #   Report Count (1)                                 */
	# 0x81, 0x01,          #   Input (Constant)                                 */
	0xc0                 # End Collection                                     */
])

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

    def send_input(self, report: bytes, report_id: int = 0):
        send_cmd = SendInputCommand.build(dict(report=report, report_id=report_id))
        self._communicator.send(send_cmd)

    def __enter__(self):
        self._communicator.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._communicator.__exit__(exc_type, exc_val, exc_tb)


if __name__ == "__main__":
    with DriverManager(SocketDriverCommunicator("192.168.40.128")) as d:
        import IPython
        IPython.embed()