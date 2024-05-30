#生成随机数据包
import random


def random_hex(length):
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(length))


def create_jt808_packet():
    packet = []

    # 固定的消息头和尾
    packet.append('7E')

    # 消息ID
    packet.append('0200')

    # 消息体属性
    packet.append('00A6')

    # 终端手机号（6字节，BCD码）
    packet.append(''.join(random.choice('0123456789') for _ in range(12)))

    # 消息流水号
    packet.append(random_hex(4))

    # 报警
    packet.append('00000000')

    # 状态
    packet.append('00080000')

    # 经纬度和其他固定字段
    packet.append(random_hex(16))
    packet.append('0000')
    packet.append('0000')
    packet.append('0000')

    # 时间
    packet.append(''.join(random.choice('0123456789') for _ in range(12)))

    # 后面的数据段
    packet.append(random_hex(6))
    packet.append(random_hex(6))
    packet.append('E564')
    packet.append('474944464530303456313035')
    packet.append('323032362D30332D3239')
    packet.append('4749444645313030')
    packet.append('3158434D38303000')
    packet.append('5858585876313030')
    packet.append('000000000000000000000000000000')
    packet.append('3839383630333653323430323532363832363634')
    packet.append('0000000000000000000000000000000000000000')
    packet.append('383637327637303638363431393632')

    # 副数据段
    packet.append('FE08')
    packet.append('0100000008000101')
    packet.append('E4020103')

    # 校验码
    packet_data = ''.join(packet[1:])  # Exclude the start 7E
    checksum = 0
    for i in range(0, len(packet_data), 2):
        checksum ^= int(packet_data[i:i + 2], 16)
    packet.append(f'{checksum:02X}')

    # 消息尾
    packet.append('7E')

    return ''.join(packet)


# 生成一个随机数据包
print(create_jt808_packet())
