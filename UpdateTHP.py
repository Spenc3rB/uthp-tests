import paramiko
from scp import SCPClient
import yaml

hostname = '192.168.7.2'
port = 22
username = 'uthp'
password = input("Enter SSH password: ")
update_overlays = input("Do you want to update overlays? (yes/no): ").strip().lower()
with open('./updates/updates.yaml', 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)

local_dts_paths = config['client_file_paths'].split(',')
remote_dts_paths = config['uthp_file_paths'].split(',')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Connecting to remote host...")
    ssh.connect(hostname, port=port, username=username, password=password)
    
    for local_dts_path, remote_dts_path in zip(local_dts_paths, remote_dts_paths):
        with SCPClient(ssh.get_transport()) as scp:
            print("Uploading patched files...")
            scp.put(local_dts_path, "/home/uthp/")
        print(f"Moving {local_dts_path} to {remote_dts_path}...")
        ssh.exec_command("echo {} | sudo -S mv /home/uthp/{} {}".format(password, local_dts_path.split('/')[-1], remote_dts_path))
        ssh.exec_command("echo {} | sudo -S chmod 644 {}".format(password, remote_dts_path))
    if update_overlays == 'yes':
        print("Updating overlays...")
        if ssh.exec_command("echo {} | sudo -S update-overlays".format(password))[1].read().decode():
            print("Overlays updated successfully.")
        else:
            print("Error updating overlays.")
    else:
        print("Skipping overlays update.")
    
    ssh.exec_command("echo {} | sudo -S shutdown now".format(password))
    
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    ssh.close()
    print("Connection closed.")
