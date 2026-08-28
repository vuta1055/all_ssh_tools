import all_ssh_execute
import getpass
import re
import get_hyx_clients

def get_hyx_client_list():
    """
    Retrieves the list of Hyx clients from all clusters.
    """
    get_hyx_clients.get_tenant_names()

while True:
    run_option = input("\nDo you want to run the get_hyx_clients script? (y/n): ").strip().lower()
    if run_option in ['y', 'n']:
            break
    print("Invalid input. Please enter 'y' or 'n'.")

if run_option == 'y':
        get_hyx_client_list()

if run_option == 'n':
    all_ssh_command = input("\nEnter the command to run on all clusters: ").strip()
    cluster_file = "all_ssh_tools/shared_cohesity_clusters.txt"

    try:
        with open(cluster_file, 'r') as f:
            hostnames = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{cluster_file}' not found!")
        exit(1)
            
    print(f"\nFound {len(hostnames)} cluster(s):")
    for i, host in enumerate(hostnames, 1):
        print(f"  {i}. {host}")
            
    # Get credentials (same for all clusters)
    username = "support"
    password = getpass.getpass("Password: ")
            
    # Commands to run
    allssh_base = 'sudo -u cohesity bash -c "/home/cohesity/bin/allssh.sh "'
    commands = [
        allssh_base + '"' + all_ssh_command + '"',
    ]

    for hostname in hostnames:
        print(f"\n{'='*60}")
        print(f"Processing: {hostname}")
        print('='*60)
        
        results = all_ssh_execute.ssh_execute(hostname, username, password, commands)
        
        if results:
            for result in results:
                print(f"\n--- Command: {result['command']} ---")
                
                # Print output if exists
                if result['output']:
                    print("\nOutput:")
                    print(result['output'])
                
                # Print errors if exist
                if result['error']:
                    print("\nErrors:")
                    print(result['error'])
        else:
            print("No results returned")