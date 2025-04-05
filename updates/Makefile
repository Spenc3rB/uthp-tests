LOG_DIR := ./logs
TIMESTAMP := $(shell date +%Y-%m-%d_%H-%M-%S)
HOST := $(shell hostname)
LOG_FILE := $(LOG_DIR)/$(HOST)_$(TIMESTAMP)

core-test: create-log-dir
	@script -q -c "bash -c './core-testing && pytest ./core/'" $(LOG_FILE)-core-results.txt

plc-test: create-log-dir
	@script -q -c "bash -c './plc-testing && pytest ./plc/'" $(LOG_FILE)-plc-results.txt
	sudo systemctl stop plc4trucksduck

remote-test: create-log-dir
	@if ! ip link show vcan0 > /dev/null 2>&1; then \
		sudo modprobe vcan; \
		sudo ip link add dev vcan0 type vcan; \
		sudo ip link set up vcan0; \
	else \
		echo "vcan0 is already available"; \
	fi
	python3 ./remote/remote-testing.py

reset:
	@echo "Running reset on host: $(HOST)"; \
	rm -rf logs/; \
	rm -rf core/__pycache__; \
	rm -rf core/.pytest_cache; \
	rm -rf plc/__pycache__; \
	rm -rf plc/.pytest_cache; \
	sudo rm -f /var/log/plc4trucksduck-errors.log; \
	sudo rm -f /var/log/plc4trucksduck.log; \
	sudo rm -f /var/log/j17084truckduck-errors.log; \
	sudo rm -f /var/log/j17084truckduck.log; \
	if ls /opt/uthp/programs/cmap/*.log 1> /dev/null 2>&1; then sudo rm /opt/uthp/programs/cmap/*.log; fi;

reset-remote:
	@echo "Running reset-remote on host: $(HOST)"; \
	rm -rf logs/; \
	rm -rf remote/__pycache__; \
	rm -rf remote/.pytest_cache;

production-ready: reset
	rm -rf /home/uthp/*
	passwd --expire uthp
	sudo systemctl stop j17084truckduck
	sudo systemctl stop plc4trucksduck
	sudo systemctl stop truckdevil-tcp
	sudo systemctl stop truckdevil-serial

create-log-dir:
	mkdir -p $(LOG_DIR)
