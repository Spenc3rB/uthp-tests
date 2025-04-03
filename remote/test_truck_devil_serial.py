import pytest
import os
import sys
import subprocess

# send a serial command to verify init
# "#0500000can0"

# recv serial command to verify recv
# should be in the form: "$0cea000b03ecfe00*"

@pytest.fixture(scope="session", autouse=True)
def change_working_dir():
    """Change the working directory and update sys.path for imports."""
    truckdevil_path = "../TruckDevil/truckdevil"
    os.chdir(truckdevil_path)
    sys.path.insert(0, truckdevil_path) # needed for python module imports
    print(f"Changed working directory to {os.getcwd()}")

def test_serial_read():
    """Ensure that the truckdevil serial read runs without errors."""
    command = "python3 ./truckdevil.py add_device m2 can0 500000 " + os.environ.get("TRUCKDEVIL_PORT") + " run_module read_messages set num_messages 5 print_messages"
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
    print(result.stdout)

    assert result.returncode == 0, f"Command failed with return code {result.returncode}"
    assert "error" not in result.stderr.lower(), f"Error in command output: {result.stderr}"

if __name__ == "__main__":
    os.environ["TRUCKDEVIL_PORT"] = input("Enter the serial port for TruckDevil: ").strip()
    pytest.main(["-v", __file__])