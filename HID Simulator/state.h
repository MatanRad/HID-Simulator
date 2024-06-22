#pragma once

#include "vhf_dev.h"

typedef struct driver_state_s {
    vhf_device_t vhf_dev;
    WDFDEVICE driver_dev;
} driver_state_t;