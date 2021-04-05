import whois
import subprocess
import requests

print("Notch 1.0.0a (v1.0.0_1000 Alpha)")
print("Type 'help' for help and 'exit' to quit.")

while True:
    command = input("notch>")

    if command == "exit":
        break

    if command == "help":
        with open("help.txt", "r") as help_file:
            print(help_file.read())

    if command == "help_advanced":
        with open("help_advanced.txt", "r") as help_advanced_file:
            print(help_advanced_file.read())

    if command[0:4] == "ping":
        print("Pinging host server...")
        ping = subprocess.Popen(
            ["ping", "-c", "3", command[5:]],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, error = ping.communicate()
        print(out.decode('utf-8'))

    if command[0:8] == "response":
        try:
            response = requests.get(command[9:])
            print(command[9:] + " returned with a response code of: " + str(response.status_code))
        except requests.exceptions.MissingSchema:
            print("Missing HTTP protocol type. Try adding 'http://' to your URL.")
        except requests.exceptions.ConnectionError:
            print("Connection error.")
        except requests.exceptions.InvalidURL:
            print("Invalid URL.")

    if command == "version":
        print("Notch v1.0.0 alpha")
        print("Build 1000")
        print("(c) 2021 Ethan under the MIT License")

    if command[0:5] == "whois":
        try:
            domain = whois.query(command[6:])
            print("Domain Name: " + domain.name)
            print("Registrar Name: " + domain.registrar)
            print("Updated Date: " + domain.last_updated.strftime("%d-%b-%Y (%H:%M:%S)"))
            print("Creation Date: " + domain.creation_date.strftime("%d-%b-%Y (%H:%M:%S)"))
            print("Expiration Date: " + domain.expiration_date.strftime("%d-%b-%Y (%H:%M:%S)"))
            print("Status: " + domain.status)
            print("Registrant Country: " + domain.registrant_country)
            print("Nameservers:")
            for nameserver in domain.name_servers:
                print("    " + nameserver)
            print("DNSSEC Enabled: " + str(domain.dnssec))
        except whois.exceptions.UnknownTld:
            print("TLD not supported.")
        except AttributeError:
            pass
