import argparse, math, sys, time, traceback, tqdm
import serial

parser = argparse.ArgumentParser(description="Send a preprocessed output file to an attached ImageWriter with flow control.")
parser.add_argument("-b", "--baud", help="Baud rate (1200, 2400, or 9600)", type=int, default=9600)
parser.add_argument("-d", "--device", help="Attached serial port", type=str, default="/dev/ttyUSB0")
parser.add_argument("-t", "--timeout", help="Write timeout", type=int, default=10)
parser.add_argument("filename", help="Preprocessed ImageWriter file to send.", type=str)
args = parser.parse_args()
device = args.device

device = serial.Serial(args.device, args.baud, timeout=args.timeout, exclusive=True, rtscts=True, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)

print("Sending", args.filename, "at rate", args.baud, "bps to device", args.device)

with open(args.filename, "rb") as fh:
    allbytez = fh.read()
    chunks = math.ceil(len(allbytez) / 8)

    for chunk in tqdm.tqdm(range(chunks)):
        bytez = allbytez[chunk*8:((chunk+1)*8)]
        device.write(bytez)
        (cts, rts, dtr, dsr) = (device.cts, device.rts, device.dtr, device.dsr)
        if not cts or not rts or not dtr or not dsr:
            print("Unexpected port state found. Waiting for it to clear. CTS", device.cts, "RTS", device.rts, "DTR", device.dtr, "DSR", device.dsr)
            while not cts or not rts or not dtr or not dsr:
                (cts, rts, dtr, dsr) = (device.cts, device.rts, device.dtr, device.dsr)
                time.sleep(0.001)

        if len(bytez)==0:
            break


