# Welcome to the UTHP test suite

The UTHP team put together a set of pytests to test the Yocto build of the UTHP (Ultimate Truck Hacking Platform) image. The tests are located in the `uthp-tests` directory, and are run on the target device after the image has been flashed to the eMMC (embedded MultiMediaCard).

## Prerequisites

### 1. Connect the UTHP to the network and power it on with the SD card inserted. 

>You may need to hold down the s2 button if another image is already flashed to the eMMC.

### 2. SSH into the UTHP
> This is stage 1
```bash
ssh root@192.168.7.2
```
> Don't worry, the root user will be locked, and the UTHP user will be added after the device has been flashed.

### 3. Generate the 'pre-production' image (i.e. the image that will be flashed to the eMMC)
> This updates user, permissions, and packages.

```bash
emmc-flasher
```

Now you are ready to take the tests for a spin! Remove the SD card from the UTHP and power cycle the device.

## Running the tests

> The tests are seperated by core tests (i.e., common functionality of the UTHP), PLC tests (i.e., 12V RAW signal needed seperately to test the PLC), and remote tests (i.e., laptop connected over USB-OTG Ethernet). In this sense the uthp-tests can be parallelized to run 3 tests on 3 different devices at the same time, improving the efficiency of the testing process.

### 1. Set up the physcial testing space

1. Start by plugging in the two battery chargers. Turn on both red safety switches on both the Cascadia and the Brake Board. 
2. After turning on the Cascadia switch on the back side, key on. The brake board serves a J1708 network, and the Cascadia provides J1939. 
3. Plug in the blue DSUB-15 from the brake board to the UTHP. 
4. Plug in the green Deutsch 9-pin connector to the black Deutsch-9 pin conector on the UTHP. 
5. Now the testbench is ready to go! You should have 3 UTHPs connected:
    - UTHP 1 (Cascadia)
    - UTHP 2 (Brake Board)
    - UTHP 3 (Laptop)

### 2. To SSH into the pre-production UTHPs

```bash
ssh uthp@192.168.7.2
```
> Password: 'UTHP-R1-XXXX' (where 'XXXX' is the last 4 digits of the UTHP serial number). 

*THIS PASSWORD IS TEMPORARY AND WILL BE
CHANGED IMMEDIATELY AFTER RUNNING `make production-ready`.*

### 3. Run the tests

> Core and PLC tests are built into the UTHP image, so you can run them from the UTHP itself. The remote tests are run from another local machine connected via USB-OTG Ethernet (192.168.7.2).

```bash
cd uthp-tests
```

Take a look at the Makefile to see the available targets:

```bash
cat Makefile
```
Let's run the core tests:

```bash
make core-test
```
and the PLC tests:

```bash
make plc-test
```
and the remote tests:

> Note: For these tests you will need to clone the following:
> 1. https://github.com/Spenc3rB/TruckDevil
> 2. https://github.com/mguentner/cannelloni --> this will need to be built onto the laptop conducting the remote testing

```bash
make remote-test
```
or if make is not installed on your system, you can simply run:

```bash
pytest ./remote/remote-testing.py
```

> Note: To perform remote tests, you will need to clone the TruckDevil repo: `git clone https://github.com/Spenc3rB/TruckDevil` inside the uthp-tests directory.
> Side note: j1708 encoding is tested by looking at the encoding (which is encoded as a j1708 message) and then sending a message serially to the UTHP. The actual software could not be tested:
```bash
  File "/usr/local/lib/python3.12/dist-packages/j1708-1.0-py3.12.egg/j1708/pid_types.py", line 278, in <module>
  File "/usr/lib/python3.12/enum.py", line 595, in __new__
    enum_class = super().__new__(metacls, cls, bases, classdict, **kwds)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/enum.py", line 271, in __set_name__
    enum_member = enum_class._new_member_(enum_class, *args)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/j1708-1.0-py3.12.egg/j1708/pid_types.py", line 67, in __new__
  File "/usr/lib/python3.12/enum.py", line 1145, in __new__
    raise TypeError("%r has no members defined" % cls)
TypeError: <flag 'BrakeSystemAirPressureLowWarningSwitchStatus'> has no members defined
```

And after we have achieved success, we can submit the image as production-ready:

1. Save the test results:

> Note: Test results should be saved to the UTHP github repo: https://github.com/SystemsCyber/UTHP/tree/main/Testing/Software/assets/logs. The logs should be saved under a directory with the serial number of the UTHP. An example of the directory structure is shown in the [logs](https://github.com/SystemsCyber/UTHP/tree/main/Testing/Software/assets/logs) directory of the UTHP github repo.

```bash
scp -r uthp@192.168.7.2:/home/uthp/uthp-tests/logs <destination>
```

and then copy the remote test results from your local machine as well.

> WARNING: The following command will delete the uthp-tests dir and set the password to expire for the uthp user:
```bash
make production-ready
```

## Troubleshooting

If you encounter any issues, send the logs to the UTHP layer maintainer:

```bash
beersc@colostate.edu
```

## Reset the UTHP tests

If you need to reset the UTHP tests, you can do so by running the following command:

```bash
make reset
```
or if running remote tests:

```bash
make reset-remote
```

# Updates to the UTHP can also be performed by running the following command:

```bash
python3 UpdateTHP.py
```
> Note: This will update the UTHP to the latest version of the UTHP software. The UTHP will reboot after the update is complete.