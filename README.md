# ESP32 Monitor Probe
 The monitor probe is used for checking the serial output of the ESP running some application.

When the probe finds malfunction it notifies the monitor at `0.0.0.0:50051`

The output of the ESP is saved into file provided as parameter

## Usage

```shell
python monitor.py monitor_out
```

## Requirements
The requirements can be satisfied by running:
```
pip install -r requirements.txt
```

## Proto compilation
To recompile the protofiles used by the grpc run
```shell
protoc -I ./proto --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ./proto/monitor.proto
```

## Blacklist
The list of the string triggering monitor norification is:
 - `"panic"`
 - `"dump"`
 - `"exception"`
 - `"watch"`
 - `"triggered"`
 - `"corrupt"`
 - `"failure"`
 - `"protect"`
 - `"reboot"`
 - `"watchdog got triggered"`
