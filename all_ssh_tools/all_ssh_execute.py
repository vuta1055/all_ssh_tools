import paramiko

def ssh_execute(hostname, username, password, commands):
    """Execute commands on remote server"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    results = []  # ← Create results list
    
    try:
        print(f"Connecting to {hostname}...")
        ssh.connect(hostname, username=username, password=password, port=22)
        print("✓ Connected\n")
        
        for cmd in commands:
            print(f">>> {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            # Store the results
            results.append({
                'command': cmd,
                'output': output,
                'error': error
            })
            
            #if output:
            #    print(output)
            #if error:
            #    print(f"ERROR: {error}")
            #print()
        
        return results  # ← RETURN the results
        
    except Exception as e:
        print(f"Error: {e}")
        return None  # ← Return None on error
    
    finally:
        ssh.close()