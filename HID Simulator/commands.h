#pragma once
#include <ntddk.h>
#include <wdf.h>

#include "state.h"
#include "vhf_dev.h"

#pragma pack(push, 1)

#define CMD_CODE_BYE ('b')
typedef struct command_bye_s {
    UCHAR type;
    UCHAR y;
    UCHAR e;
} command_bye_t;

#define CMD_CODE_SET_DEV ('s')
typedef struct command_set_dev_s {
    UCHAR type;
    ULONG dev_id;
    vhf_device_t dev;
} command_set_dev_t;

#define CMD_CODE_CLEAR_DEV ('c')
typedef struct command_clear_dev_s {
    UCHAR type;
    ULONG dev_id;
} command_clear_dev_t;

#define CMD_CODE_SEND_INPUT ('i')
typedef struct command_send_input_s {
    UCHAR type;
    ULONG dev_id;
    UCHAR report_id;
    ULONG report_len;
    UCHAR report[MAX_REPORT_LENGTH];
} command_send_input_t;

#pragma pack(pop)

NTSTATUS exec_user_cmd(driver_state_t* state, PUCHAR buff, ULONG buff_len);
