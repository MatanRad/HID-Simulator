#pragma once

#include "state.h"

#ifdef DEBUG
#define TRACE_LEVEL(lvl, ...) \
    if (g_state.log_level >= (lvl)) { \
        KdPrintEx((DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, __VA_ARGS__)); \
    }

#else

#define TRACE_LEVEL(lvl, ...) \
    if (g_state.log_level >= (lvl) && LOG_DEBUG != (lvl)) { \
        KdPrintEx((DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, __VA_ARGS__)) \
    }

#endif

#define TRACE(...) TRACE_LEVEL(LOG_INFO, __VA_ARGS__)
#define TRACE_DEBUG(...) TRACE_LEVEL(LOG_DEBUG, __VA_ARGS__)

