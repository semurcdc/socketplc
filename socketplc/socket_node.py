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
        velocity = round(struct.unpack(fmt, data[0:4])[0],4)
        position = round(struct.unpack(fmt, data[4:8])[0],4)
        alarm = struct.unpack('h', data[8:10])[0]
        # Imprimir los valores recibidos
        print(f"Velocidad: {velocity}")
        print(f"Posición: {position}")
        print(f"Alarma: {alarm}")
        rclpy.spin_once(node, timeout_sec=0.5)
    node.client.close()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
