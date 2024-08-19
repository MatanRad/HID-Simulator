from driver_communicator import DriverManager, SocketDriverCommunicator, DirectDriverCommunicator
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


if __name__ == "__main__":
    with DriverManager(DirectDriverCommunicator()) as d:
        import IPython
        IPython.embed()