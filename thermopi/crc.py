"""Calculate CRC checksums for messages to and from the thermostat."""

CRC_TABLE = [  # A copy of this resides in the thermostat Arduino code, they must be the same.
    247, 250, 54, 124, 174, 56, 24, 25, 76, 240, 58, 22, 88,
    134, 30, 79, 114, 93, 154, 41, 238, 78, 102, 185, 153, 4,
    203, 252, 113, 10, 237, 92, 3, 70, 196, 32, 55, 140, 229,
    244, 242, 116, 106, 209, 204, 77, 144, 15, 253, 217, 164, 246,
    248, 216, 12, 49, 125, 226, 53, 207, 84, 239, 17, 62, 156,
    96, 7, 117, 233, 162, 111, 225, 130, 97, 219, 135, 227, 67,
    45, 141, 83, 243, 8, 118, 129, 59, 43, 188, 180, 86, 231,
    71, 206, 136, 184, 82, 50, 155, 210, 181, 95, 100, 90, 189,
    178, 35, 28, 126, 202, 171, 133, 224, 87, 165, 214, 168, 131,
    98, 128, 173, 249, 42, 255, 177, 119, 221, 208, 120, 132, 222,
    36, 193, 44, 85, 39, 183, 199, 123, 74, 73, 60, 159, 151,
    105, 57, 27, 170, 18, 89, 107, 23, 21, 145, 91, 201, 176,
    19, 192, 190, 115, 112, 230, 94, 245, 72, 75, 38, 152, 61,
    198, 46, 149, 63, 99, 127, 179, 215, 232, 6, 191, 66, 138,
    9, 80, 143, 5, 31, 81, 212, 14, 11, 146, 34, 150, 167,
    254, 69, 213, 142, 169, 235, 251, 122, 148, 163, 157, 137, 37,
    47, 65, 175, 110, 220, 158, 223, 13, 195, 1, 101, 20, 200,
    218, 234, 40, 228, 166, 205, 147, 194, 161, 211, 68, 0, 16,
    236, 109, 241, 64, 104, 51, 33, 182, 2, 121, 172, 48, 186,
    103, 108, 52, 197, 26, 187, 160, 29, 139
]


def crc_calc(data):
    """Calculate a CRC-8 of the object passed

    Source: https://www.maximintegrated.com/en/app-notes/index.mvp/id/27

    Parameters
    ----------
    data : bytearray
        Binary data to calculate the CRC-8 for.

    Returns
    -------
    bytearray
        CRC integer.
    """

    crc = 0x0

    for d in data:
        crc = CRC_TABLE[crc ^ d]

    return bytearray([crc])
