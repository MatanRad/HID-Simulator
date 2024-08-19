from construct import Int64ul, Int32ul, Int16ul, Int8ul, Default, Rebuild, Struct, Const, this, Padded, GreedyBytes, len_, PaddedString

VHFDevice = Struct(
    "handle" / Default(Int64ul, 0),
    "name" / PaddedString(32, "ascii"),
    "report_desc_length" / Rebuild(Int16ul, len_(this.report_desc)),
    "report_desc" / Padded(2048, GreedyBytes)
)

ByeCommand = Struct(
    "type" / Const(b'b'),
    "y" / Const(b'y'),
    "e" / Const(b'e'),
)

SetDeviceCommand = Struct(
    "type" / Const(b's'),
    "dev_id" / Int32ul,
    "dev" / VHFDevice,
)

ClearDeviceCommand = Struct(
    "type" / Const(b'c'),
    "dev_id" / Int32ul,
)

SendInputCommand = Struct(
    "type" / Const(b'i'),
    "dev_id" / Int32ul,
    "report_id" / Default(Int8ul, 0),
    "report_length" / Rebuild(Int32ul, len_(this.report)),
    "report" / Padded(2048, GreedyBytes)
)
