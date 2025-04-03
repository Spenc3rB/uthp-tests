LOG_DIR := ./logs
TIMESTAMP := $(shell date +%Y-%m-%d_%H-%M-%S)
HOST := $(shell hostname)
LOG_FILE := $(LOG_DIR)/$(HOST)_$(TIMESTAMP)

core-test: create-log-dir
	@script -q -c "bash -c './core-testing && pytest ./core/'" $(LOG_FILE)-core-results.txt

plc-test: create-log-dir
	@script -q -c "bash -c './plc-testing && pytest ./plc/'" $(LOG_FILE)-plc-results.txt

remote-test: create-log-dir
	python3 ./remote/remote-testing.py

reset:
	@if [ "${HOST#UTHP}" = "$HOST" ]; then \
		echo "Running reset on host: $(HOST)"; \
		rm -rf logs/; \
		rm -rf core/__pycache__; \
		rm -rf core/.pytest_cache; \
		rm -rf plc/__pycache__; \
		rm -rf plc/.pytest_cache; \
		sudo rm -f /var/log/plc4trucksduck-errors.log; \
		sudo rm -f /var/log/plc4trucksduck.log; \
		sudo rm -f /var/log/j17084truckduck-errors.log; \
		sudo rm -f /var/log/j17084truckduck.log; \
		if ls /opt/uthp/programs/cmap/*.log 1> /dev/null 2>&1; then sudo rm /opt/uthp/programs/cmap/*.log; fi; \
	else \
		echo "Error: The reset target can only be run on a host with a name starting with 'UTHP'." >&2; \
		exit 1; \
	fi

reset-remote:
	@if [ "${HOST#UTHP}" != "$HOST" ]; then \
		echo "Running reset-remote on host: $(HOST)"; \
		rm -rf logs/; \
		rm -rf remote/__pycache__; \
		rm -rf remote/.pytest_cache; \
	else \
		echo "Error: The reset-remote target can only be run on a host NOT starting with 'UTHP'."; \
		exit 1; \
	fi

production-ready: reset
	rm -rf /home/uthp/uthp-tests
	passwd --expire uthp

create-log-dir:
	mkdir -p $(LOG_DIR)
