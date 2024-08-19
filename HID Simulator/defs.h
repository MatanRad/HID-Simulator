#pragma once

#include "tracing.h"

#define EXPECT_STATUS(x)                                                     \
    do {                                                                     \
        res = (x);                                                           \
        if (!NT_SUCCESS(res)) {                                              \
            TRACE_ERROR("[MY_DRIVER] NSTATUS Error %s:%d! Status: %d\n", __FILE__, \
                  __LINE__, res);                                            \
            goto cleanup;                                                    \
        }                                                                    \
    } while (0)

#define EXPECT(x, r)                                                           \
    do {                                                                       \
        if (!(x)) {                                                            \
            res = (r);                                                         \
            TRACE_ERROR("[MY_DRIVER] Error %s:%d! Result: %d\n", __FILE__, __LINE__, \
                  res);                                                        \
            goto cleanup;                                                      \
        }                                                                      \
    } while (0)

#define EXPECT_RETHROW(x)                                                    \
    do {                                                                     \
        res = (x);                                                           \
        if (!NT_SUCCESS(res)) {                                              \
            TRACE_ERROR("		[MY_DRIVER] Rethrown at %s:%d!\n", __FILE__, \
                  __LINE__);                                                 \
            goto cleanup;                                                    \
        }                                                                    \
    } while (0)
