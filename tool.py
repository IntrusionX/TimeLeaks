import sys
import requests
import subprocess
import os
import shutil

def display_menu():
    title = r"""
####################################################################
#________      _____                     _____             ____  __#
#____  */*_______  /___________  ___________(_)______________  |/ /#
# **  / **  ** \  **/_  ___/  / / /_  ___/_  /_  __ \_  __ \_    / #
#__/ /  *  / / / /* *  /   / /*/ /_(__  )_  / / /_/ /  / / /    |  #
#/___/  /_/ /_/\__/ /_/    \__,_/ /____/ /_/  \____//_/ /_//_/|_|  #
####################################################################
    """
    print(title)

# Find the gf binary in various possible locations
def find_gf_binary():
    possible_locations = [
        "/home/attacker/.local/bin/gf",  # Original location
        os.path.expanduser("~/go/bin/gf"),  # Go installation path
        os.path.expanduser("~/.local/bin/gf"),  # Alternative local path
        "/usr/local/bin/gf",  # System-wide installation
        "/usr/bin/gf"  # Another system location
    ]
    
    # Also check if gf is in PATH
    gf_in_path = shutil.which("gf")
    if gf_in_path:
        return gf_in_path
    
    # Check each possible location
    for location in possible_locations:
        if os.path.isfile(location) and os.access(location, os.X_OK):
            print(f"Found gf binary at: {location}")
            return location
    
    print("Could not find gf binary. Please ensure it's installed correctly.")
    return None

# Fetch all the links from the Wayback Machine for a given domain
def fetch_wayback_links(domain):
    url = f"https://web.archive.org/cdx/search/cdx?url={domain}/*&collapse=urlkey&output=text&fl=original"
    response = requests.get(url)
    print("Response Status Code:", response.status_code)  # Print the status code
    print("Response Content:", response.text[:500])  # Print the first 500 characters of the response content for debugging
    
    if response.status_code == 200:
        links = response.text.splitlines()
        print(f"Fetched {len(links)} links from the Wayback Machine for {domain}.")
        return links
    else:
        print("Failed to retrieve data from the Wayback Machine.")
        return []

# Function to check links for a specific vulnerability using gf
def check_vulnerabilities(links, vulnerability_type, gf_path):
    """
    Checks links for a specific vulnerability using gf patterns.
    vulnerability_type can be 'ssrf', 'xss', 'rce', or 'sqli'.
    """
    if not links:
        print("No links to check.")
        return
    
    if not gf_path:
        print("Error: gf binary not found. Cannot check for vulnerabilities.")
        return
    
    # Ensure the ~/.gf directory exists with patterns
    patterns_dir = os.path.expanduser("~/.gf")
    if not os.path.exists(patterns_dir) or not os.listdir(patterns_dir):
        print(f"Warning: The gf patterns directory {patterns_dir} does not exist or is empty.")
        # Try to set up patterns from Gf-Patterns repo
        if not os.path.exists("./Gf-Patterns"):
            print("Cloning Gf-Patterns repository...")
            subprocess.run(["git", "clone", "https://github.com/1ndianl33t/Gf-Patterns.git"], check=True)
        
        # Make sure the ~/.gf directory exists
        os.makedirs(patterns_dir, exist_ok=True)
        
        # Copy patterns to ~/.gf
        if os.path.exists("./Gf-Patterns"):
            pattern_files = [f for f in os.listdir("./Gf-Patterns") if f.endswith(".json")]
            for pattern_file in pattern_files:
                src = os.path.join("./Gf-Patterns", pattern_file)
                dst = os.path.join(patterns_dir, pattern_file)
                shutil.copy2(src, dst)
            print(f"Copied {len(pattern_files)} pattern files to {patterns_dir}")
    
    # Save the links into a temporary file
    with open('temp_links.txt', 'w') as file:
        for link in links:
            file.write(link + "\n")
    
    # Construct the GF command for the vulnerability type
    gf_command = f"{gf_path} {vulnerability_type} < temp_links.txt > {vulnerability_type}_links.txt"
    
    try:
        # Run the GF tool with the selected vulnerability type
        print(f"Running command: {gf_command}")
        subprocess.run(f"sh -c '{gf_command}'", shell=True, check=True)
        print(f"Checked for {vulnerability_type} and saved results in {vulnerability_type}_links.txt")
    except subprocess.CalledProcessError as e:
        print(f"Error running gf tool: {e}")
    finally:
        # Remove temporary file
        os.remove('temp_links.txt')

# Main function to tie everything together
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 intrusionx.py example.com")
        sys.exit(1)
    
    domain = sys.argv[1]
    
    print(f"Starting vulnerability checks for {domain}...")
    
    # Find the gf binary
    gf_path = find_gf_binary()
    if not gf_path:
        print("Cannot continue without gf. Please install it and try again.")
        sys.exit(1)
    
    # Step 1: Fetch links from the Wayback Machine
    links = fetch_wayback_links(domain)
    
    if not links:
        print("No links were fetched. Exiting...")
        return
    
    # Step 2: Check for each type of vulnerability
    vulnerability_types = ['ssrf', 'xss', 'rce', 'sqli']
    
    for vulnerability_type in vulnerability_types:
        check_vulnerabilities(links, vulnerability_type, gf_path)

if __name__ == "__main__":
    display_menu()
    main()
