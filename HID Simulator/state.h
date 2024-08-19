#pragma once

#include "vhf_dev.h"

#define MAX_DEVICES (4)

typedef enum driver_log_level_e {
    LOG_DEBUG = 0,
    LOG_INFO = 1,
    LOG_WARNING = 2,
    LOG_ERROR = 3,
} driver_log_level_t;

typedef struct driver_state_s {
    vhf_device_t vhf_devices[MAX_DEVICES];
    WDFDEVICE driver_dev;
    driver_log_level_t log_level;
} driver_state_t;

extern driver_state_t g_state;