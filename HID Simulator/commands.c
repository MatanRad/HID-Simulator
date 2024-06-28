#include "commands.h"

#include "defs.h"
#include "vhf_dev.h"

#define VERIFY_CMD(buff, buff_len, cmd_struct, cmd_type)               \
    if (buff_len != sizeof(cmd_struct)) {                              \
        TRACE("[MY_DRIVER] Invalid command size: %d! Expected: %d!\n", \
              buff_len, sizeof(cmd_struct));                           \
        EXPECT(0, -1);                                                 \
    }                                                                  \
    EXPECT(buff[0] == (cmd_type), -2);

NTSTATUS exec_bye_cmd(driver_state_t* state, command_bye_t* cmd) {
    NTSTATUS res = STATUS_SUCCESS;
    TRACE("[MY_DRIVER] Executing bye command?!?!\n");

    EXPECT(state && cmd, STATUS_SUCCESS);
    EXPECT(cmd->type == 'b', STATUS_SUCCESS);
    EXPECT(cmd->y == 'y', STATUS_SUCCESS);
    EXPECT(cmd->e == 'e', STATUS_SUCCESS);

    // Time to do a pro gamer move!
    volatile PWDFDEVICE_INIT a = NULL;
    WdfDeviceInitSetIoType(a, WdfDeviceIoBuffered);
cleanup:
    return res;
}

NTSTATUS exec_set_dev_cmd(driver_state_t* state, command_set_dev_t* cmd) {
    NTSTATUS res = STATUS_SUCCESS;
    TRACE("[MY_DRIVER] Executing set command!\n");

    EXPECT(state && cmd, STATUS_SUCCESS);
    EXPECT(cmd->type == CMD_CODE_SET_DEV, STATUS_SUCCESS);

    EXPECT(state->vhf_dev.handle == NULL, STATUS_SUCCESS);
    EXPECT(cmd->dev.handle == NULL, STATUS_SUCCESS);

    vhf_device_t dev = cmd->dev;

    EXPECT_RETHROW(init_vhf_device(&dev, state->driver_dev));

    EXPECT(dev.handle != NULL, STATUS_SUCCESS);
    state->vhf_dev = dev;

cleanup:
    return res;
}

NTSTATUS exec_clear_dev_cmd(driver_state_t* state, command_clear_dev_t* cmd) {
    NTSTATUS res = STATUS_SUCCESS;
    TRACE("[MY_DRIVER] Executing clear command!\n");

    EXPECT(state && cmd, STATUS_SUCCESS);
    EXPECT(cmd->type == CMD_CODE_CLEAR_DEV, STATUS_SUCCESS);

    uninit_vhf_device(&state->vhf_dev);

    EXPECT(state->vhf_dev.handle == NULL, STATUS_SUCCESS);

cleanup:
    return res;
}

NTSTATUS exec_send_input_cmd(driver_state_t* state, command_send_input_t* cmd) {
    NTSTATUS res = STATUS_SUCCESS;
    TRACE("[MY_DRIVER] Executing send input command!\n");

    EXPECT(state && cmd, STATUS_SUCCESS);
    EXPECT(cmd->type == CMD_CODE_SEND_INPUT, STATUS_SUCCESS);

    EXPECT(state->vhf_dev.handle != NULL, -1);

    HID_XFER_PACKET xfer = { 0 };
    xfer.reportId = cmd->report_id;
    xfer.reportBufferLen = cmd->report_len;
    xfer.reportBuffer = cmd->report;
    EXPECT_STATUS(VhfReadReportSubmit(state->vhf_dev.handle, &xfer));

cleanup:
    return res;
}

NTSTATUS exec_user_cmd(driver_state_t* state, PUCHAR buff, ULONG buff_len) {
    NTSTATUS res = STATUS_SUCCESS;
    TRACE("[MY_DRIVER] Executing command!\n");

    switch (buff[0]) {
        case CMD_CODE_BYE:
            VERIFY_CMD(buff, buff_len, command_bye_t, CMD_CODE_BYE);
            EXPECT_RETHROW(exec_bye_cmd(state, (command_bye_t*)buff));
            break;

        case CMD_CODE_SET_DEV:
            VERIFY_CMD(buff, buff_len, command_set_dev_t, CMD_CODE_SET_DEV);
            EXPECT_RETHROW(exec_set_dev_cmd(state, (command_set_dev_t*)buff));
            break;

        case CMD_CODE_CLEAR_DEV:
            VERIFY_CMD(buff, buff_len, command_clear_dev_t, CMD_CODE_CLEAR_DEV);
            EXPECT_RETHROW(
                exec_clear_dev_cmd(state, (command_clear_dev_t*)buff));
            break;

        case CMD_CODE_SEND_INPUT:
            VERIFY_CMD(buff, buff_len, command_send_input_t, CMD_CODE_SEND_INPUT);
            EXPECT_RETHROW(
                exec_send_input_cmd(state, (command_send_input_t*)buff));
            break;
        default:
            TRACE("[MY_DRIVER] Unknown Command Recieved! (%ul)\n", (unsigned int)buff[0]);
            break;
    }

cleanup:
    return res;
}
