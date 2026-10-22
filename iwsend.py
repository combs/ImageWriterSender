import argparse, sys, time, traceback, tqdm
import serial

parser = argparse.ArgumentParser(description="Send a preprocessed output file to an attached ImageWriter with flow control.")
parser.add_argument("-b", "--baud", help="Baud rate (1200, 2400, or 9600)", type=int, default=9600)
parser.add_argument("-d", "--device", help="Attached serial port", type=str, default="/dev/ttyUSB0")
parser.add_argument("-t", "--timeout", help="Write timeout", type=int, default=10)
parser.add_argument("filename", help="Preprocessed ImageWriter file to send.", type=str)
args = parser.parse_args()
device = args.device
print(args)

device = serial.Serial(args.device, args.baud, timeout=args.timeout, exclusive=True, rtscts=True, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)

print("Sending", args.filename)

with open(args.filename, "rb") as fh:
    while True:
        bytez = fh.read(8)
        device.write(bytez)
        cts = device.cts, rts = device.rts, dtr = device.dtr, dsr = device.dsr
        if not cts or not rts or not dtr or not dsr:
            print("Unexpected port state found. CTS", device.cts, "RTS", device.rts, "DTR", device.dtr, "DSR", device.dsr)
        if len(bytez)==0:
            break


