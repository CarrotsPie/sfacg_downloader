# sign.py
import hashlib

def get_sign(nonce: str, timestamp: int, device_token: str, salt: str) -> str:
    long_nonce = (nonce * 4).encode("ascii")

    def index_calc(x):
        x0 = long_nonce[x]
        x17 = x0 // 0x24
        offset = x0 - x17 * 0x24
        return offset

    offset1 = index_calc(1)
    offset2 = index_calc(2)
    offset3 = index_calc(3)
    offset4 = index_calc(4)

    nonce_reorder = (
        long_nonce[offset1:offset1 + 13] +
        long_nonce[offset2:offset2 + 16] +
        long_nonce[offset3:offset3 + 36] +
        long_nonce[offset4:offset4 + 36]
    )

    auth_string = (str(timestamp) + salt + device_token + nonce).encode("ascii")

    result = ""
    for i in range(101):
        result += chr((auth_string[i] + nonce_reorder[i]) >> 1)

    lens = [13, 16, 36, 36]
    A = result[0:lens[0]]
    B = result[lens[0]:lens[0] + lens[1]]
    C = result[lens[0] + lens[1]:lens[0] + lens[1] + lens[2]]
    D = result[lens[0] + lens[1] + lens[2]:]

    string_after_reorder = D + A + C + B

    final = ""
    for i in range(101):
        char_code = ord(string_after_reorder[i])
        if char_code < 0x30:
            if 0x39 < char_code + 19 < 0x41:
                final += chr(0x39)
            else:
                final += chr(char_code + 19)
        elif 0x39 < char_code < 0x41:
            final += chr(char_code + 19)
        elif 0x5A < char_code < 0x61:
            final += chr(char_code + 19)
        else:
            final += string_after_reorder[i]

    return hashlib.md5(final.encode("utf-8")).hexdigest().upper()