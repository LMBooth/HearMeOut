import sounddevice as sd
import numpy as np

def list_devices():
    devices = sd.query_devices()
    input_devices = []
    output_devices = []
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            input_devices.append((i, device['name']))
        if device['max_output_channels'] > 0:
            output_devices.append((i, device['name']))
    
    print("Input Devices:")
    for idx, name in input_devices:
        print(f"{idx}: {name}")
    
    print("\nOutput Devices:")
    for idx, name in output_devices:
        print(f"{idx}: {name}")

    return input_devices, output_devices

def select_device(devices, device_type):
    device_idx = int(input(f"\nSelect {device_type} device by index: "))
    for idx, name in devices:
        if idx == device_idx:
            print(f"Selected {device_type}: {name}")
            return device_idx
    raise ValueError("Invalid device index")

def audio_callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

def main():
    input_devices, output_devices = list_devices()

    input_device_idx = select_device(input_devices, 'input')
    output_device_idx = select_device(output_devices, 'output')

    # Set selected devices
    sd.default.device = (input_device_idx, output_device_idx)
    
    # Stream audio from the selected mic to the selected speaker
    with sd.Stream(callback=audio_callback):
        print("\nPress Ctrl+C to stop the audio stream.")
        try:
            while True:
                sd.sleep(1000)
        except KeyboardInterrupt:
            print("\nAudio stream stopped.")

if __name__ == "__main__":
    main()
