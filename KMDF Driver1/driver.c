#include <ntddk.h>
#include <wdf.h>
#include "defs.h"

//Key=qdixckzal28c.1xj9ha16g59w5.1hie5bc8e5nt3.1jc7ypf744jdd

DRIVER_INITIALIZE DriverEntry;
EVT_WDF_DRIVER_DEVICE_ADD KmdfHelloWorldEvtDeviceAdd;

#define DOS_DEVICE_NAME  L"\\DosDevices\\MyDevice"
DECLARE_CONST_UNICODE_STRING(dosDeviceName, DOS_DEVICE_NAME);

unsigned char g_buf[4096] = { 0 };
unsigned long g_buf_len;

WDFQUEUE  g_queue = NULL;


NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath) {
	NTSTATUS ret = STATUS_SUCCESS;

	WDF_DRIVER_CONFIG config = { 0 };

    TRACE(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "[MY_DRIVER] Driver Entry!\n");

	WDF_DRIVER_CONFIG_INIT(&config,
		KmdfHelloWorldEvtDeviceAdd
	);

	ret = WdfDriverCreate(DriverObject, RegistryPath, WDF_NO_OBJECT_ATTRIBUTES, &config, WDF_NO_HANDLE);

	return ret;
}

void KmdfIoQueueIoWrite(WDFQUEUE Queue, WDFREQUEST Request, size_t Length) {
    NTSTATUS status;
    WDFMEMORY memory;
    PVOID buffer;
    size_t bufferLength;

    UNREFERENCED_PARAMETER(Queue);
    UNREFERENCED_PARAMETER(Length);

    status = WdfRequestRetrieveInputMemory(Request, &memory);
    if (!NT_SUCCESS(status)) {
        TRACE(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "[MY_DRIVER] Error retriving memory on write: %l!\n", status);
        WdfRequestComplete(Request, status);
        return;
    }

    buffer = WdfMemoryGetBuffer(memory, &bufferLength);
    if (buffer == NULL) {
        TRACE(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "[MY_DRIVER] Error retriving buffer on write: %l!\n", status);
        WdfRequestComplete(Request, status);
        return;
    }

    // Print the buffer to the debug console
    TRACE(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "[MY_DRIVER] Message: %s!\n", (PCSTR)buffer);

    if (bufferLength > sizeof(g_buf) || bufferLength == 0) {
        g_buf_len = 0;
    } else {
        g_buf_len = (unsigned long)bufferLength;
        memcpy(g_buf, buffer, g_buf_len);
    }

    if (g_buf_len == 3 && g_buf[0] == 'b' && g_buf[1] == 'y' && g_buf[2] == 'e') {
        // Time to do a pro gamer move!
        volatile PWDFDEVICE_INIT a = NULL;
        WdfDeviceInitSetIoType(a, WdfDeviceIoBuffered);
    }

    WdfRequestComplete(Request, status);
}

void KmdfIoQueueIoRead(WDFQUEUE Queue, WDFREQUEST Request, size_t Length) {
    NTSTATUS status;
    WDFMEMORY memory;
    PVOID buffer;
    size_t bufferLength;

    UNREFERENCED_PARAMETER(Queue);
    UNREFERENCED_PARAMETER(Length);

    status = WdfRequestRetrieveOutputMemory(Request, &memory);
    if (!NT_SUCCESS(status)) {
        TRACE(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "[MY_DRIVER] Error retriving memory on read: %l!\n", status);
        WdfRequestComplete(Request, status);
        return;
    }

    buffer = WdfMemoryGetBuffer(memory, &bufferLength);
    if (buffer == NULL) {
        TRACE(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "[MY_DRIVER] Error retriving buffer on write: %l!\n", status);
        WdfRequestComplete(Request, status);
        return;
    }

    if (g_buf_len > 0) {
        memcpy_s(buffer, bufferLength, g_buf, g_buf_len);
        g_buf_len = 0;
    }
    
    WdfRequestCompleteWithInformation(Request, status, bufferLength);
}

NTSTATUS KmdfHelloWorldEvtDeviceAdd(WDFDRIVER Driver, PWDFDEVICE_INIT DeviceInit) {
    UNREFERENCED_PARAMETER(Driver);

    NTSTATUS ret_status;
    NTSTATUS status;

    WDFDEVICE hDevice;

    WDF_IO_QUEUE_CONFIG  ioQueueConfig;

    TRACE(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "[MY_DRIVER] KmdfHelloWorldEvtDeviceAdd\n");

    if (DeviceInit == NULL) {
        TRACE(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "[MY_DRIVER] Device Init is null wtf?! %d\n");
        return 0;
    }

    WdfDeviceInitSetIoType(DeviceInit, WdfDeviceIoBuffered);

    ret_status = WdfDeviceCreate(&DeviceInit,
        WDF_NO_OBJECT_ATTRIBUTES,
        &hDevice
    );

    if (g_queue != NULL) {
        TRACE(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "[MY_DRIVER] Queue Already Initialized!\n");
        return ret_status;
    }


    status = WdfDeviceCreateSymbolicLink(hDevice, &dosDeviceName);
    if (!NT_SUCCESS(status)) {
        TRACE(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "[MY_DRIVER] Error creating symlink: %l!\n", status);
        return status;
    }
    TRACE(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "[MY_DRIVER] Created symlink!\n");
    
    // IO Queue
    WDF_IO_QUEUE_CONFIG_INIT_DEFAULT_QUEUE(&ioQueueConfig, WdfIoQueueDispatchSequential);
    ioQueueConfig.EvtIoWrite = KmdfIoQueueIoWrite;
    ioQueueConfig.EvtIoRead = KmdfIoQueueIoRead;

    status = WdfIoQueueCreate(hDevice, &ioQueueConfig, WDF_NO_OBJECT_ATTRIBUTES, &g_queue);
    if (!NT_SUCCESS(status)) {
        TRACE(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "[MY_DRIVER] Error creating queue: %l!\n", status);
        return status;
    }

    return ret_status;
}