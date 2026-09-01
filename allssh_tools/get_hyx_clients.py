import all_ssh_execute
import getpass
import re
from datetime import datetime

def parse_tenant_ids(output):
    """
    Parse tenant IDs from allssh.sh output
    
    Args:
        output (str): Raw output from the command
    
    Returns:
        set: Unique tenant IDs
    """
    tenant_ids = set()
    
    # Find all lines with "Tenant-id"
    for line in output.split('\n'):
        if 'Tenant-id' in line:
            # Extract the tenant ID (everything after "Tenant-id")
            match = re.search(r'Tenant-id\s+(\S+)', line)
            if match:
                tenant_id = match.group(1)
                tenant_ids.add(tenant_id)
    
    return tenant_ids


def get_tenant_names():
    # Read hostnames from file
    cluster_file = input("Cluster file [shared_cohesity_clusters.txt]: ") or "allssh_tools/shared_cohesity_clusters.txt"
    
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
    commands = [
        'sudo -u cohesity bash -c "/home/cohesity/bin/allssh.sh \\"elinks http:0:29992 | grep \'Tenant-id\'\\" | awk \'{print $2}\'\"',
    ]
    
    # Process each cluster
    all_results = {}
    
    for hostname in hostnames:
        print(f"\n{'='*60}")
        print(f"Processing: {hostname}")
        print('='*60)
        
        # Execute commands
        results = all_ssh_execute.ssh_execute(hostname, username, password, commands)
        
        if results:
            # Parse tenant IDs from the output
            output = results[0]['output']
            tenant_ids = parse_tenant_ids(output)
            
            # Store results
            all_results[hostname] = tenant_ids
            
            # Display unique, sorted tenant IDs
            print("\nUNIQUE TENANT IDs (Sorted)")
            print("-" * 60)
            
            for tenant_id in sorted(tenant_ids):
                print(tenant_id)
            
            print(f"\nTotal unique tenants: {len(tenant_ids)}")
        else:
            print(f"No results from {hostname}")
            all_results[hostname] = set()
            
    # Save to file
    while True:
        save_file = input("\nSave to file? [y/N]: ").strip().lower()
        if save_file in ['y', 'n']:
            break
        print("Invalid input. Please enter 'y' or 'n'.")
    
    if save_file == 'y':
        # Save combined results
        print(f"\n{'='*60}")
        print("SAVING COMBINED RESULTS")
        print('='*60)

        filename = f"all_ssh_tools\\outputs\\all_clusters_tenants_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"Cohesity Tenant Report\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for hostname, tenant_ids in all_results.items():
                f.write(f"\nCluster: {hostname}\n")
                f.write("-" * 60 + "\n")
                
                if tenant_ids:
                    for tenant_id in sorted(tenant_ids):
                        f.write(f"  {tenant_id}\n")
                    f.write(f"\nTotal: {len(tenant_ids)} tenant(s)\n")
                else:
                    f.write("  No tenants found\n")
                
                f.write("\n")
        
        print(f"\n✓ Saved to: {filename}")

if __name__ == "__main__":
    get_tenant_names()
