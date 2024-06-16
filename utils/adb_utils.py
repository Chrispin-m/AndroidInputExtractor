import subprocess

def run_adb_command(command):
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    return output


def get_current_app_package():
    # Run adb command to get the focused window's package name + Handling the idle state
    try:
    	adb_command = "adb shell dumpsys activity activities | grep ResumedActivity"
    	output = subprocess.check_output(adb_command, shell=True, text=True)
    	# Extract the package name from the output
    	package_name = output.split()[2].split('/')[0]
    except Exception as e:
    	print("\033[91mWarning: " + str(e) + "\033[0m")
    	package_name = "idle.xml"

    return package_name
