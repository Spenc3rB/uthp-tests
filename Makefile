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
	python3 ./remote/remote-testing.py

can0-2-test: create-log-dir
	@script -q -c "bash -c './can0-2-testing && pytest ./can0-2/'" $(LOG_FILE)-can0-2-results.txt

reset:
	@echo "Running reset on host: $(HOST)"; \
	rm -rf logs/; \
	rm -rf core/__pycache__; \
	rm -rf core/.pytest_cache; \
	rm -rf plc/__pycache__; \
	rm -rf plc/.pytest_cache; \
	rm -rf remote/__pycache__; \
	rm -rf remote/.pytest_cache; \
	rm -rf can0-2/__pycache__; \
	rm -rf can0-2/.pytest_cache; \
	sudo rm -f /var/log/plc4trucksduck-errors.log; \
	sudo rm -f /var/log/plc4trucksduck.log; \
	sudo rm -f /var/log/j17084truckduck-errors.log; \
	sudo rm -f /var/log/j17084truckduck.log; \
	if ls /opt/uthp/programs/cmap/*.log 1> /dev/null 2>&1; then sudo rm /opt/uthp/programs/cmap/*.log; fi;
	sudo systemctl stop j17084truckduck
	sudo systemctl stop plc4trucksduck
	sudo systemctl stop truckdevil-tcp
	sudo systemctl stop truckdevil-serial


reset-remote:
	@echo "Running reset-remote on host: $(HOST)"; \
	rm -rf logs/; \
	rm -rf remote/__pycache__; \
	rm -rf remote/.pytest_cache;

production-ready: reset
	rm -rf /home/uthp/*
	sudo passwd --expire uthp
	@echo "Ensuring all services are disabled"; \
	sudo systemctl disable plc4trucksduck
	sudo systemctl disable j17084truckduck
	sudo systemctl disable truckdevil-tcp
	sudo systemctl disable truckdevil-serial
	sudo passwd --expire uthp
	sudo systemctl disable j17084truckduck
	sudo systemctl disable plc4trucksduck
	sudo systemctl disable truckdevil-tcp
	sudo systemctl disable truckdevil-serial

create-log-dir:
	mkdir -p $(LOG_DIR)
