#include "vhf_dev.h"

#include "defs.h"

VHFHANDLE g_vhf = NULL;

NTSTATUS init_vhf_device(vhf_device_t* device, WDFDEVICE driver_device) {
    NTSTATUS res = 0;
    VHF_CONFIG conf = {0};

    EXPECT(device != NULL, -1);
    EXPECT(driver_device != NULL, -1);
    EXPECT(device->handle == NULL, -1);
    EXPECT(device->report_desc_length > 0, -1);
    EXPECT(device->report_desc_length < MAX_REPORT_LENGTH, -1);

    PDEVICE_OBJECT dobject = WdfDeviceWdmGetDeviceObject(driver_device);
    EXPECT(dobject != NULL, -1);

    VHF_CONFIG_INIT(&conf, dobject, device->report_desc_length,
                    device->report_desc);

    conf.VendorID = 0xdead;
    conf.ProductID = 0x1337;
    // TODO: Config it here.

    EXPECT_STATUS(VhfCreate(&conf, &device->handle));

cleanup:
    return res;
}

void uninit_vhf_device(vhf_device_t* device) {
    NTSTATUS res = 0;

    EXPECT(device != NULL, -1);
    EXPECT(device->handle != NULL, -1);

    VhfDelete(device->handle, TRUE);

    memset(device, 0, sizeof(*device));
cleanup:
    return;
}