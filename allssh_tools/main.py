import inspect
import getpass
import all_ssh_execute
import get_hyx_clients
from datetime import datetime

# --- Menu functions (add new ones here) ------------------------------

def get_hyx_client_list():
    """Get HyX Client List - Retrieves tenant names from all clusters."""
    # keep prompting / ssh logic inside this function
    get_hyx_clients.get_tenant_names()


def run_allssh_command():
    """Run Custom AllSSH Command - Execute a command across all clusters."""
    all_ssh_command = input("\nEnter the command to run on all clusters (e.g. 'ip addr'): ").strip()
    if not all_ssh_command:
        print("No command entered. Cancelling.")
        return

    cluster_file = "all_ssh_tools/shared_cohesity_clusters.txt"
    try:
        with open(cluster_file, 'r') as f:
            hostnames = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{cluster_file}' not found!")
        return

    print(f"\nFound {len(hostnames)} cluster(s).")
    username = "support"
    password = getpass.getpass("Password: ")

    # Build command for allssh.sh (adjust quoting if needed)
    allssh_base = 'sudo -u cohesity bash -c "/home/cohesity/bin/allssh.sh '
    commands = [allssh_base + '"' + all_ssh_command + '"' + '"']

    for hostname in hostnames:
        print(f"\n{'='*60}")
        print(f"Cluster: {hostname}")
        print('='*60)
        results = all_ssh_execute.ssh_execute(hostname, username, password, commands)

        if not results:
            print("No results returned or connection failed.")
            continue

        # pretty-print results (simple)
        for result in results:
            print(f"\n--- Command: {result['command']} ---")
            if result['output']:
                print("Output:")
                print(result['output'])
            if result['error']:
                print("Errors:")
                print(result['error'])

# --- Menu engine (auto-discover) -------------------------------------

def _discover_menu_functions(module):
    """
    Return list of (name, func) for functions to include in the menu.
    Criteria:
      - is a function
      - has a docstring
      - name does not start with underscore
      - not the main() function itself
    """
    functions = inspect.getmembers(module, inspect.isfunction)
    menu_funcs = [
        (name, func)
        for name, func in functions
        if func.__module__ == module.__name__               # defined in this module
        and not name.startswith('_')
        and name != 'main'
        and func.__doc__ and func.__doc__.strip()
    ]
    return menu_funcs


def main():
    current_module = inspect.getmodule(inspect.currentframe())
    menu_items = _discover_menu_functions(current_module)

    if not menu_items:
        print("No menu functions found. Add functions with docstrings to appear in the menu.")
        return

    # Build ordered list for display
    menu_items = sorted(menu_items, key=lambda x: x[0])  # optional: sort by name

    while True:
        print("\n" + "="*60)
        print("Cohesity Management Tools")
        print("="*60)

        for idx, (name, func) in enumerate(menu_items, 1):
            # Use first line of docstring for label
            label = func.__doc__.strip().splitlines()[0]
            print(f"{idx}. {label}")

        print("q. Quit")

        choice = input("\nSelect an option: ").strip().lower()
        if choice == 'q':
            print("Goodbye.")
            break

        try:
            index = int(choice) - 1
        except ValueError:
            print("Invalid input. Enter a menu number or 'q'.")
            continue

        if not (0 <= index < len(menu_items)):
            print("Invalid selection. Try again.")
            continue

        name, func = menu_items[index]
        label = func.__doc__.strip().splitlines()[0]
        print(f"\n{'-'*60}\nRunning: {label}\n{'-'*60}")

        # Run the function safely
        try:
            func()
        except Exception as e:
            print(f"ERROR running {name}: {e}")

        input("\nPress Enter to return to menu...")


if __name__ == "__main__":
    main()
