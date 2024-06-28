from construct import Int64ul, Default, Int16ul, Rebuild, Struct, Const, this, Padded, GreedyBytes, len_
_InternalVHFDevice = Struct(
    "handle" / Default(Int64ul, 0),
    "report_desc_length" / Rebuild(Int16ul, len_(this.report_desc)),
    "report_desc" / GreedyBytes
)

VHFDevice = Padded(2048 + 8 + 2, _InternalVHFDevice)

ByeCommand = Struct(
    "type" / Const(b'b'),
    "y" / Const(b'y'),
    "e" / Const(b'e'),
)

SetDeviceCommand = Struct(
    "type" / Const(b's'),
    "dev" / VHFDevice,
)

ClearDeviceCommand = Struct(
    "type" / Const(b'c'),
)