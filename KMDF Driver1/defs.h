#pragma once

#ifdef DEBUG

#define TRACE(...) KdPrintEx((__VA_ARGS__))

#else

#define TRACE(...) KdPrintEx((__VA_ARGS__))

#endif