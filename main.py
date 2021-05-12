#!/usr/bin/env python3

import grpc
import monitor_pb2
import monitor_pb2_grpc
import serial
import sys


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
        'reboot',
        'watchdog got triggered',
    ]

    return any(err in line.lower() for err in error_strings)


def main(out):
    # open file for output
    with open(out, 'wb') as of:
        # setup grpc client
        channel = grpc.insecure_channel('localhost:50051')
        stub = monitor_pb2_grpc.EspMonitorStub(channel)

        # setup reading from serial port
        ser = serial.Serial('/dev/ttyUSB0', baudrate=115200)
        while True:
            try:
                ser_bytes = ser.readline()
                if contains_error_strings(ser_bytes.decode('utf-8')):
                    try:
                        print("+========================================+",
                                "|                                        |",
                                "|              ERROR FOUND               |",
                                "|                                        |",
                                "+========================================+", sep='\n')
                        notify(stub)
                    except:
                        print("!!! detected FAILURE, but could not notify the monitor")
                of.write(ser_bytes)
                of.flush()
            except UnicodeDecodeError:
                pass

if __name__ == '__main__':
    if len(sys.argv) == 2:
        out = sys.argv[1]
    else:
        print("Invalid arguments")
        exit(1)

    main(out)

