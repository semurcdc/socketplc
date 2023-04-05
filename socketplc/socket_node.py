import rclpy
from rclpy.node import Node
import socket
import struct
import time


class SocketNode(Node):
    def __init__(self):
        super().__init__('socket_node')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        plc_address = ('192.168.1.3', 10000)
        self.sock.connect(plc_address)

def main(args=None):
    rclpy.init(args=args)
    node = SocketNode()
    while rclpy.ok():
        # Enviar el número 28 en hexadecimal al PLC
        node.sock.sendall(bytes.fromhex('2801'))
        # Leer la respuesta del PLC
        data = node.sock.recv(1024)
        fmt = ">f"  # ">" indica big-endian y "f" indica float
        # Decodificar los datos recibidos en variables
        VelocityJoint1 = round(struct.unpack(fmt, data[0:4])[0],4)
        PositionJoint1 = round(struct.unpack(fmt, data[4:8])[0],4)
        AlarmJoint1 = struct.unpack('h', data[8:10])[0]
        VelocityJoint2 = round(struct.unpack(fmt, data[10:14])[0], 4)
        PositionJoint2 = round(struct.unpack(fmt, data[14:18])[0], 4)
        AlarmJoint2 = struct.unpack('h', data[18:20])[0]
        VelocityJoint3 = round(struct.unpack(fmt, data[20:24])[0], 4)
        PositionJoint3 = round(struct.unpack(fmt, data[24:28])[0], 4)
        AlarmJoint3 = struct.unpack('h', data[28:30])[0]
        VelocityJoint4 = round(struct.unpack(fmt, data[30:34])[0], 4)
        PositionJoint4 = round(struct.unpack(fmt, data[34:38])[0], 4)
        AlarmJoint4 = struct.unpack('h', data[38:40])[0]
        # Imprimir los valores recibidos
        print(f"VelocityJoint1: {VelocityJoint1}")
        print(f"PositionJoint1: {PositionJoint1}")
        print(f"AlarmJoint1: {AlarmJoint1}")
        print(f"VelocityJoint2: {VelocityJoint2}")
        print(f"PositionJoint2: {PositionJoint2}")
        print(f"AlarmJoint2: {AlarmJoint2}")
        print(f"VelocityJoint3: {VelocityJoint3}")
        print(f"PositionJoint3: {PositionJoint3}")
        print(f"AlarmJoint3: {AlarmJoint3}")
        print(f"VelocityJoint4: {VelocityJoint4}")
        print(f"PositionJoint4: {PositionJoint4}")
        print(f"AlarmJoint4: {AlarmJoint4}")
        rclpy.spin_once(node, timeout_sec=0.5)
    node.client.close()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
