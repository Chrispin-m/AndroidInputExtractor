import subprocess
import sys
import re
import os

# Color codes for printing
class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

def print_intro():
    print(colors.GREEN + "=============================================")
    print("    Welcome to the Cool ADB Connector! (Best For Wireless Debugging)")
    print("=============================================" + colors.END)
    print()

def enable_developer_options():
    print("To connect via USB/Wi-Fi, you need to enable Developer Options and USB Debugging on your device.")
    print("Please follow the instructions below:")
    print("1. Go to Settings > About Phone.")
    print("2. Tap on 'Build number' 7 times until you see 'You are now a developer!' message.")
    print("3. Go back to Settings > System > Developer options.")
    print("4. Enable 'USB Debugging'.")

def connect_via_wifi():
    print("Connecting via Wi-Fi...")
    print("1. Connect your device to the same Wi-Fi network as your computer.")
    print("2. Find your device IP address and port under Settings > System > Developer options > Wireless debugging.")
    print("3. Enable 'Pair device with pairing code' and generate the pairing code.")
    pair_device = "no"
    pair_device = input("Do you want to pair the device? (yes/no) default = no (must be yes if it's first time): ").lower()
    if pair_device == "yes":
        print("4. Goto Wireless Debugging on your phone >> Pair device with pairing code.")
        pair_code=input("Enter pairing code on your device:")
        try:
            ip_address = input("Enter the IP address of your device: ")
            port = input("Enter the port (default is 5555): ")
            subprocess.run(["adb", "pair", f"{ip_address}:{port}", pair_code], check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print(colors.RED + "Error: Failed to connect via Wi-Fi. Please ensure your device is connected to the same network and try again." + colors.END)
        print(colors.GREEN + "Paired via Wi-Fi successfully!" + colors.END)
    elif pair_device == "no":
        pass
    else:
        print("Invalid choice. Please enter 'yes' or 'no'.")
        sys.exit(1)

    ip_address = input("Enter the IP address of your device(ip_address under wireless debugging): ")
    port = input("Enter the port (default is 5555) (port under wireless debugging): ")
    if not port:
        port = "5555"
    try:
        subprocess.run(["adb", "connect", f"{ip_address}:{port}"], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print(colors.RED + "Error: Failed to connect via Wi-Fi. Please ensure your device is connected to the same network and try again." + colors.END)
        sys.exit(1)
    print(colors.GREEN + "Connected via Wi-Fi successfully!" + colors.END)

def connect_via_usb():
    print("Connecting via USB...")
    try:
        subprocess.run(["adb", "devices"], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print(colors.RED + "Error: ADB is not installed or USB Debugging is not enabled." + colors.END)
        sys.exit(1)
    print(colors.GREEN + "Connected via USB successfully!" + colors.END)

def main():
    print_intro()
    enable_developer_options()

    while True:
        connection_type = input("How would you like to connect? (USB - 1/Wi-Fi - 2): ").lower()
        if connection_type == "1":
            connect_via_usb()
            break
        elif connection_type == "2":
            connect_via_wifi()
            break
        else:
            print("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    main()
