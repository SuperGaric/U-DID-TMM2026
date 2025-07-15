# 例子：只关注‘7C’的变化
hex_data_without_did = "2E0101C1FFFF91A12801007B000780000A00000D00"
hex_data_with_did = "2E0101C1FFFF91A12801007B000780000A00000D007C"

# 将十六进制数据转换为字节
byte_data_without_did = bytes.fromhex(hex_data_without_did)
byte_data_with_did = bytes.fromhex(hex_data_with_did)

# 比较末尾数据
print(f"Without DID: {byte_data_without_did[-1]}")
print(f"With DID: {byte_data_with_did[-1]}")
