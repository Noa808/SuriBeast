#This script will take the urls in the input file and output the ip addresses following the correct notation for suricata's IPREP.
#I reccomend you place this in your home directory.
#!/usr/bin/env python3
import os
import subprocess

# Paths
input_file = "/home/noa/blocklist.txt"
output_file = "/etc/suricata/iprep/reputation.list"

def perform_dig(domain, all_ips=False):
    """Perform dig +short command and return the first or all IP addresses."""
    result = subprocess.run(['dig', '+short', domain], capture_output=True, text=True)
    ip_addresses = result.stdout.strip().splitlines()
    if all_ips:
        return ip_addresses  # Return all IP addresses
    if ip_addresses:
        return [ip_addresses[0]]  # Return only the first IP address
    return []

def write_to_file(output_path, sections):
    """Write IP addresses to the output file with specified formatting."""
    with open(output_path, 'w') as f:
        for idx, section in enumerate(sections):
            for ip in section:
                # Append the appropriate suffix based on the section
                suffix = f"/24,{idx+1},1"
                f.write(f"{ip}{suffix}\n")
            f.write("\n")  # Add an empty line after each section

def main():
    # Read domains from the input file
    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist.")
        return
    
    with open(input_file, 'r') as infile:
        domains = [line.strip() for line in infile.readlines()]

    all_ips_first_sections = []
    all_ips_fourth_section = []

    # Process each domain and get IPs
    for i, domain in enumerate(domains):
        if i < 30:
            ips = perform_dig(domain)
            all_ips_first_sections.extend(ips)
        else:
            ips = perform_dig(domain, all_ips=True)
            all_ips_fourth_section.extend(ips)

    # Split the first 30 IPs into 3 sections of 10 IPs each
    first_three_sections = [all_ips_first_sections[i:i+10] for i in range(0, 30, 10)]

    # Create the fourth section with all IPs from the remaining domains
    fourth_section = all_ips_fourth_section

    # Combine all sections
    sections = first_three_sections + [fourth_section]

    # Write the IPs to the output file with formatting
    write_to_file(output_file, sections)

    print("done")

if __name__ == "__main__":
    main()
