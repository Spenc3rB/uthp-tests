#!/usr/bin/env python3
import os
import subprocess
import logging
import sys
from datetime import datetime
from dotenv import load_dotenv

def init_logging():
    """Set up logging to file + console with timestamp."""
    LOG_DIR = "logs"
    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    host = os.getenv("SSH_PASS", "unknown")
    logfile = os.path.join(LOG_DIR, f"{host}_{timestamp}-remote-results.txt")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        handlers=[
            logging.FileHandler(logfile),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger()

def cleanup_env():
    for var in ["SSH_HOST", "SSH_USER", "SSH_PASS", "SERIAL_PORT", "TRUCKDEVIL_PORT", "GRIMMJ1708_PORT"]:
        os.environ.pop(var, None)
    print("Environment cleaned.")

def main():
    os.environ["SSH_HOST"] = "192.168.7.2"
    os.environ["SSH_USER"] = "uthp"
    os.environ["SSH_PASS"] = input("Enter SSH password: ").strip()

    if input("Are you connected over USB? (y/n): ").strip().lower() == 'y':
        load_dotenv()
        os.environ["SERIAL_PORT"] = os.getenv("SERIAL_PORT", "/dev/ttyACM0")
        os.environ["TRUCKDEVIL_PORT"] = os.getenv("TRUCKDEVIL_PORT", "/dev/ttyACM1")
        os.environ["GRIMMJ1708_PORT"] = os.getenv("GRIMMJ1708_PORT", "/dev/ttyACM2")

    logger = init_logging()

    try:
        logger.info("Starting remote tests...\n")
        # Stream output directly into logging
        with subprocess.Popen(["pytest", "./remote"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as proc:
            for line in proc.stdout:
                logger.info(line.strip())
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
    finally:
        cleanup_env()

if __name__ == "__main__":
    main()
