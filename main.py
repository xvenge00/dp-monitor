import grpc
import monitor_pb2
import monitor_pb2_grpc
import serial

def notify(stub):
    stub.Notify(monitor_pb2.google_dot_protobuf_dot_empty__pb2.Empty())


def contains_error_strings(line: str):
    error_strings = [
        'panic',
        'dump',
        'exception',
        'watch',
        'triggered',
        'corrupt',
        'failure',
        'protect',
    ]

    return any(err in line.lower() for err in error_strings)


def main():
    # setup grpc client
    channel = grpc.insecure_channel('localhost:50051')
    stub = monitor_pb2_grpc.EspMonitorStub(channel)

    # setup reading from serial port
    ser = serial.Serial('/dev/ttyUSB0', baudrate=115200)
    while True:
        ser_bytes = ser.readline()
        # TODO bude to fungovat aj pri panics/core dumps?
        if contains_error_strings(ser_bytes.decode('utf-8')):
            print(ser_bytes)
            print("===============NOT OK ==================")
            notify(stub)


if __name__ == '__main__':
    main()

