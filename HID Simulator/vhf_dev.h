#pragma once

#include <ntddk.h>
#include <vhf.h>
#include <wdf.h>

extern VHFHANDLE g_vhf;

#define MAX_REPORT_DESCRIPTOR_LENGTH (2048)
#define MAX_REPORT_LENGTH (2048)
#define MAX_DEVICE_NAME (32)

#pragma pack(push, 1)

typedef struct vhf_device_s {
    VHFHANDLE handle;
    CHAR name[MAX_DEVICE_NAME];
    USHORT report_desc_length;
    UCHAR report_desc[MAX_REPORT_DESCRIPTOR_LENGTH];
} vhf_device_t;

#pragma pack(pop)

NTSTATUS init_vhf_device(vhf_device_t* device, WDFDEVICE driver_device);
void uninit_vhf_device(vhf_device_t* device);