import subprocess
import os

def get_wifi_profiles():
    """Retrieve a list of saved Wi-Fi profiles."""
    try:
        output = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("utf-8")
        profiles = [line.split(":")[1][1:-1] for line in output.split("\n") if "All User Profile" in line]
        return profiles
    except subprocess.CalledProcessError:
        print("[!] Failed to retrieve Wi-Fi profiles. Run as Administrator.")
        return []

def get_wifi_password(profile):
    """Retrieve the Wi-Fi password for a given profile."""
    try:
        output = subprocess.check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"]).decode("utf-8")
        for line in output.split("\n"):
            if "Key Content" in line:
                return line.split(":")[1][1:-1]  # Extract password
    except subprocess.CalledProcessError:
        print(f"[!] Error retrieving password for {profile}.")
    return "N/A"

def main():
    """Main function to fetch and display Wi-Fi credentials."""
    profiles = get_wifi_profiles()
    if not profiles:
        print("[!] No Wi-Fi profiles found.")
        return

    results = []
    print("\n{:<30} |  {:<}".format("Wi-Fi Name", "Password"))
    print("-" * 50)
    
    for profile in profiles:
        password = get_wifi_password(profile)
        results.append(f"{profile:<30} |  {password}")
        print(f"{profile:<30} |  {password}")

    # Optional: Save to a file
    save_results(results)

def save_results(results, filename="wifi_passwords.txt"):
    """Save the retrieved Wi-Fi credentials to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Wi-Fi Name                     |  Password\n")
        file.write("-" * 50 + "\n")
        file.write("\n".join(results))
    print(f"\n[✔] Wi-Fi passwords saved to {os.path.abspath(filename)}")

if __name__ == "__main__":
    main()
