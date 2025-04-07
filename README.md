# Welcome to the UTHP test suite

The UTHP team put together a set of pytests to test the Yocto build of the UTHP (Ultimate Truck Hacking Platform) image. The tests are located in the `uthp-tests` directory, and are run on the target device after the image has been flashed to the eMMC (embedded MultiMediaCard).

## Prerequisites

Before you use this repository, you must have a basic understanding of Linux commands, and GitHub. Resource on how to use the Linux command line GitHub can be found [here](https://ubuntu.com/tutorials/command-line-for-beginners#1-overview) and [here](https://docs.github.com/en/get-started/quickstart).

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

Start by turning on the two battery chargers, then turn on both red safety switches on both the Cascadia and the Brake Board. 

### 2. SSH into the "pre-production" UTHPs

```bash
ssh uthp@192.168.7.2
```
> Password: 'UTHP-R1-XXXX' (where 'XXXX' is the last 4 digits of the UTHP serial number). 

*THIS PASSWORD IS TEMPORARY AND WILL BE
CHANGED IMMEDIATELY AFTER RUNNING `make production-ready`.*

### 3. Update the UTHP

```
python3 UpdateTHP.py
```

After this has run, please power cycle the UTHP (ensure the blue LED is completely off before powering it back on).

### 4. Run the tests

ssh back into the UTHP. You should see the coresponding version number (see [./updates/updates.yaml](./updates/updates.yaml)) after you log in.

Core, PLC, and CAN0-2 tests are run from the UTHP image, so you can run them from the UTHP itself. The remote tests are run from another local machine connected via USB-OTG Ethernet (192.168.7.2).

#### 4.1 Understanding the test structure

```bash
cd uthp-tests
```

Take a look at the Makefile to see the available targets:

```bash
cat Makefile
```

You should have the following targets:
- `core-test`: Runs the core tests
- `plc-test`: Runs the PLC tests
- `can0-2-test`: Runs the CAN 0-2 tests
- `remote-test`: Runs the remote tests
- `reset`: Resets the UTHP tests *!!!This will wipe the logs dir!!!*
- `reset-remote`: Resets the remote tests *!!!This will wipe the logs dir!!!*
- `production-ready`: Cleans up the UTHP tests, ensures all services are disabled, and sets the password to expire for the uthp user
- `create-log-dir`: Creates a log directory for the test results (this is done automatically when you run the tests)

It's easiest to run two terminals. One you have ssh'd into with an active session, and another for running remote tests, updates, and other commands.

#### 4.1 Core tests:

> Note: The core tests have been verified on the Cascadia, but should be able to run on any network with CAN, and J1708.

This tests the following:

Software:
- can-utils
- cancat
- canmatrix
- cannelloni
- cmap
- ipython3
- j1939 kernel module
- jupyter lab
- pretty-j1939
- py-hv-networks
- python3-can
- python2.7
- real time clock
- rtl-sdr
- safe-shutdown
- scapy
- sigrok-cli
- tmux
- truckdevil

Hardware:
- Deutch-9 Pin can0 send and receive
- DSUB-15 J1708 send and receive

Let's run the core tests from *within* the UTHP:

```bash
sudo make core-test
```

#### 4.2 PLC tests:

> Note: The PLC tests have been verified on the Brake Board, but should be able to run on any network with PLC.

This tests the following:

Software:
- plc4trucksduck
- pretty-j1587

Hardware:
- DSUB-15 PLC send and receive (VBatt+12v and GND)

Let's run the PLC tests from *within* the UTHP:

> Note: The PLC tests require the Brake Board to be power cycled. First run:

```bash
sudo make plc-test
```
> wait for `Environment setup should be complete... waiting for user to confirm hardware is ready.` and then power cycle the Brake Board. After that, you can hit any key to continue the tests.
#### 4.3 CAN0-2 tests:

> Note: The CAN0-2 tests have been verified on the Truck-In-A-Box, but should be able to run on any network with 12V CAN on the Deutch-9 Pin.

This tests the following:
Software:
- python3-can

Hardware:
- Deutch-9 Pin can0 send and receive
- Deutch-9 Pin can1 send and receive
- Deutch-9 Pin can2 send and receive

> Note: CAN4 is verified manually, by inspecting the bitmagic.

Let's run the CAN0-2 tests from *within* the UTHP:
```
make can0-2-test
```

#### 4.4 Remote tests:

> Note: For these tests you will need to clone the following from within the uthp-tests directory:
> 1. https://github.com/Spenc3rB/TruckDevil

```bash
sudo make remote-test
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

And after we have achieved success, we can submit the image as production-ready, but first...

### 5. Save the test results

> Note: Test results should be saved to the UTHP github repo: https://github.com/SystemsCyber/UTHP/tree/main/Testing/Software/assets/logs. The logs should be saved under a directory with the serial number of the UTHP. An example of the directory structure is shown in the [logs](https://github.com/SystemsCyber/UTHP/tree/main/Testing/Software/assets/logs) directory of the UTHP github repo.

Each test result should be named respectively. Make sure to include all 4 test results (core, PLC, CAN0-2, and remote) in the same directory. The following walks you through the process:

#### 5.1 Clone the UTHP repo from *within* the uthp-tests directory

```bash
git clone https://github.com/SystemsCyber/UTHP
```
#### 5.2 Copy the test results

> Make sure these are the most recent (all passing) test results.

```bash
cd UTHP/Testing/Software/assets/logs 
```
Make a new directory with the UTHP serial number:
> Note: you will need to change XXXX

```bash
mkdir UTHP-R1-XXXX
```
Then copy the `core`, `plc`, and `can0-2` test results:

```bash
scp -r uthp@192.168.7.2:/home/uthp/uthp-tests/logs ./UTHP-R1-XXXX
```

Finally copy the `remote` test results from your local machine to the UTHP repo:
```bash
 cp ../../../../../logs/*-remote-results.txt ./UTHP-R1-XXXX
```

Then open up a text editor and edit the `README.md` file to include the test results, along with your initials. You can continue to update this later if needed.

#### 5.3 Push the test results to the UTHP repo

```bash
git add ./UTHP-R1-XXXX
git commit -m "Added UTHP-R1-XXXX test results - <your initials>"
git push origin main
```

### 6. Production ready

> WARNING: The following command will delete the uthp-tests dir and set the password to expire for the uthp user:
```bash
make production-ready
```

After running the tests, ensure nothing is left in the uthp user's home directory, the output of `systemctl status` looks something similar to this clean report:

```bash
● UTHP-R1-0032
    State: running
    Units: 231 loaded (incl. loaded aliases)
     Jobs: 0 queued
   Failed: 0 units
    Since: Wed 1969-12-31 19:00:03 EST; 55 years 3 months ago
  systemd: 255.17^
   CGroup: /
           ├─init.scope
           │ └─1 /sbin/init
           └─system.slice
             ├─busybox-klogd.service
             │ └─193 /usr/sbin/klogd -n
             ├─busybox-syslog.service
             │ └─194 /usr/sbin/syslogd -n
             ├─dbus.service
             │ └─195 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopid>
             ├─safe-shutdown.service
             │ ├─ 198 /bin/bash -e /opt/uthp/scripts/safe-shutdown.sh
             │ └─5193 sleep 2
             ├─system-getty.slice
             │ └─getty@tty1.service
             │   └─196 /sbin/agetty -o "-p -- \\u" --noclear - linux
             ├─system-serial\x2dgetty.slice
             │ ├─serial-getty@ttyGS0.service
             │ │ └─278 /sbin/agetty -8 -L ttyGS0 115200 linux
             │ └─serial-getty@ttyS0.service
             │   └─199 /sbin/agetty -8 -L ttyS0 115200 linux
             ├─system-sshd.slice
             │ └─sshd@13-192.168.7.2:22-192.168.7.1:6349.service
             │   ├─4553 "sshd: uthp [priv]"
             │   ├─4561 "sshd: uthp@pts/0"
             │   ├─4562 -bash
             │   ├─5194 systemctl status
             │   └─5195 less
             ├─systemd-journald.service
             │ └─105 /usr/lib/systemd/systemd-journald
             ├─systemd-logind.service
             │ └─206 /usr/lib/systemd/systemd-logind
             ├─systemd-networkd.service
             │ └─140 /usr/lib/systemd/systemd-networkd
             ├─systemd-resolved.service
             │ └─172 /usr/lib/systemd/systemd-resolved
             ├─systemd-timesyncd.service
             │ └─173 /usr/lib/systemd/systemd-timesyncd
             ├─systemd-udevd.service
             │ └─udev
             │   └─138 /usr/lib/systemd/systemd-udevd
             └─systemd-userdbd.service
               ├─ 141 /usr/lib/systemd/systemd-userdbd
```

...and pop open another terminal and ensure the passwd is expired for the uthp user. DO NOT SET A NEW PASSWORD. For example:

```bash
ssh uthp@192.168.7.2
uthp@192.168.7.2's password:
Last login: Sat Apr  5 03:28:57 2025 from 192.168.7.1
WARNING: Your password has expired.
You must change your password now and login again!
```

## Reset the UTHP tests

> This stops systemd services that take up the CPU and memory, and resets the UTHP to a clean state. If performed remotely it will clean the cache.

If you need to reset the UTHP tests, you can do so by running the following command:

```bash
make reset
```
or if running remote tests:

```bash
make reset-remote
```