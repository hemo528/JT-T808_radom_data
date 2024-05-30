#此脚本用于创建注册数据包

import random
import struct


def random_hex(length):
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(length))


def generate_bcd(phone_num):
    if len(phone_num) % 2 != 0:
        phone_num += '0'
    bcd = bytes((int(phone_num[i:i + 2], 16) for i in range(0, len(phone_num), 2)))
    return bcd


def jt808_set_message_register(phone_num):
    # 初始化变量
    msgData = {}
    msgBodyRegister = {}

    # 处理终端号码
    terminal_num = generate_bcd(phone_num)

    # 设置消息头
    msgData['startMsgFlag'] = 0x7E
    msgData['msgID'] = 0x0100  # Register message ID
    msgBodyLen = 15  # Example length of register message body
    msgData['msgAttribute'] = (msgBodyLen & 0x03FF) | (0 << 10) | (0 << 13) | (0 << 14) | (0 << 15)
    msgData['terminalNum'] = terminal_num
    msgData['msgSerinum'] = random.randint(0, 65535)

    # 打印调试信息
    print(f"sizeof(JT808_Message_Body_Register) = {msgBodyLen}")

    # 模拟注册消息体内容
    msgBodyRegister['provinceID'] = random.randint(0, 65535)
    msgBodyRegister['cityID'] = random.randint(0, 65535)
    msgBodyRegister['manufacturerID'] = random_hex(5)
    msgBodyRegister['terminalType'] = random_hex(8)
    msgBodyRegister['terminalID'] = random_hex(7)
    msgBodyRegister['licensePlateColor'] = random.randint(0, 255)
    msgBodyRegister['licensePlate'] = random_hex(7)

    # 生成消息负载
    playLoad = struct.pack('!HH5s8s7sB7s',
                           msgBodyRegister['provinceID'],
                           msgBodyRegister['cityID'],
                           msgBodyRegister['manufacturerID'].encode(),
                           msgBodyRegister['terminalType'].encode(),
                           msgBodyRegister['terminalID'].encode(),
                           msgBodyRegister['licensePlateColor'],
                           msgBodyRegister['licensePlate'].encode())

    # 计算校验和
    checkNum = 0
    header = struct.pack('!2BHB6sH',
                         msgData['startMsgFlag'],
                         msgData['msgID'] >> 8,
                         msgData['msgID'] & 0xFF,
                         msgData['msgAttribute'],
                         msgData['terminalNum'],
                         msgData['msgSerinum'])
    for byte in header[1:]:  # Exclude the start flag (0x7E)
        checkNum ^= byte
    for byte in playLoad:
        checkNum ^= byte

    msgData['checkNum'] = checkNum
    msgData['endMsgFlag'] = 0x7E

    # 组装最终数据包
    sendHex = header + playLoad + struct.pack('!BB', msgData['checkNum'], msgData['endMsgFlag'])

    return sendHex.hex().upper()


# 示例：生成一个随机的注册数据包
phone_num = "020220101009"  # 示例终端手机号
print(jt808_set_message_register(phone_num))
