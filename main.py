import whois
import subprocess
import requests
import dns.resolver
import socket
import sys
import warnings

if sys.platform != "darwin":
    warnings.warn("This application has only been tested on MacOSX>=10.15.7.")


def main():
    print("Notch 1.0.1 (v1.0.1_1002)")
    print("Type 'help' for help and 'exit' to quit.")

    while True:
        command = input("notch>")

        if command[0:3] == "dns":
            command_args = command.split(" ")
            if len(command_args) == 1:
                print("Missing required argument: <domain>")
            if len(command_args) == 2:
                try:
                    domain_name = command_args[1]
                    print(socket.gethostbyname(domain_name))
                except socket.gaierror:
                    print("The requested domain does not exist.")
                except UnicodeError:
                    print("The requested domain name is too long.")
            if len(command_args) >= 3:
                print("Fetching records...")
                record_type = command_args[1]
                domain_name = command_args[2]
                try:
                    if record_type == "-a":
                        result = dns.resolver.resolve(domain_name, 'A')
                        for ip_value in result:
                            print("A:", ip_value.to_text())
                    if record_type == "-cname":
                        result = dns.resolver.resolve(domain_name, 'CNAME')
                        for cname_value in result:
                            print("CNAME:", cname_value.to_text())
                    if record_type == "-txt":
                        result = dns.resolver.resolve(domain_name, 'TXT')
                        for txt_value in result:
                            print("TXT:", txt_value.to_text())
                    if record_type == "-mx":
                        result = dns.resolver.resolve(domain_name, 'MX')
                        for mx_value in result:
                            print("MX:", mx_value.to_text())
                except dns.resolver.NXDOMAIN:
                    print("The requested domain does not exist.")
                except dns.resolver.NoAnswer:
                    print("There are no existing records tied this domain for the requested record type.")
                except dns.exception.Timeout:
                    print("The request timed out.")

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
            print("Notch version 1.0.1")
            print("Build 1002")
            print("(c) 2021 Ethan under the MIT License")

        if command[0:5] == "whois":
            print("Querying WHOIS server...")
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


if __name__ == "__main__":
    main()
