import psutil
import win32process
import win32con
import win32api
import time
import sys

def set_process_priority(pid, priority=win32process.HIGH_PRIORITY_CLASS):
    """Set the process priority to High."""
    try:
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
        win32process.SetPriorityClass(handle, priority)
        win32api.CloseHandle(handle)
        print(f"Process priority set to HIGH for PID: {pid}")
    except Exception as e:
        print(f"Failed to set process priority for PID {pid}: {e}")

def set_cpu_affinity(process, exclude_cpu=0):
    """Set CPU affinity for a process, excluding CPU 0."""
    try:
        # Get the available CPU cores
        cpu_count = psutil.cpu_count(logical=True)
        all_cpus = list(range(cpu_count))
        all_cpus.remove(exclude_cpu)  # Remove CPU 0

        # Set CPU affinity
        process.cpu_affinity(all_cpus)
        print(f"CPU affinity updated: Excluding CPU {exclude_cpu}")
    except Exception as e:
        print(f"Failed to set CPU affinity: {e}")

def find_and_optimize_process(process_name="eldenring.exe"):
    """Find the Elden Ring process and optimize its priority and CPU affinity."""
    try:
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'].lower() == process_name.lower():
                pid = process.info['pid']
                print(f"Elden Ring process found with PID: {pid}")

                # Set process priority to High
                set_process_priority(pid)

                # Set CPU affinity to exclude CPU 0
                set_cpu_affinity(process)

                return True
        print(f"No process named '{process_name}' found.")
    except Exception as e:
        print(f"Error while processing: {e}")
    return False

if __name__ == "__main__":
    print("Searching for Elden Ring process...")
    while True:
        success = find_and_optimize_process()
        if success:
            print("Optimization completed successfully.")
            break
        else:
            print("Retrying in 5 seconds...")
            time.sleep(5)

    # Exit the script after the task is done.
    print("Script completed. Exiting...")
    sys.exit()