import whois
import subprocess
import requests
import dns.resolver
import socket
import speedtest
import sys
import warnings

if sys.platform != "darwin":
    warnings.warn("This application has only been tested on MacOSX>=10.15.7.")


def main():
    print("Notch 1.1.0 (v1.1.0_1003)")
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
                domain_name = command_args[len(command_args)-1]
                try:
                    if "-a" in command_args:
                        try:
                            result = dns.resolver.resolve(domain_name, 'A')
                            for ip_value in result:
                                print("A:", ip_value.to_text())
                        except dns.resolver.NoAnswer:
                            print("There are no existing A records tied to this domain.")
                    if "-cname" in command_args:
                        try:
                            result = dns.resolver.resolve(domain_name, 'CNAME')
                            for cname_value in result:
                                print("CNAME:", cname_value.to_text())
                        except dns.resolver.NoAnswer:
                            print("There are no existing CNAME records tied to this domain.")
                    if "-txt" in command_args:
                        try:
                            result = dns.resolver.resolve(domain_name, 'TXT')
                            for txt_value in result:
                                print("TXT:", txt_value.to_text())
                        except dns.resolver.NoAnswer:
                            print("There are no existing TXT records tied to this domain.")
                    if "-mx" in command_args:
                        try:
                            result = dns.resolver.resolve(domain_name, 'MX')
                            for mx_value in result:
                                print("MX:", mx_value.to_text())
                        except dns.resolver.NoAnswer:
                            print("There are no existing MX records tied to this domain.")
                except dns.resolver.NXDOMAIN:
                    print("The requested domain does not exist.")
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

        if command[0:3] == "ist":
            command_args = command.split(" ")
            print("Initializing...")
            speed_test_module = speedtest.Speedtest()
            if len(command_args) == 1:
                print("Testing download speed...")
                download_speed = speed_test_module.download() / 1000000
                print("Download Speed: " + str(round(download_speed, 2)) + "Mbit/s")
                print("Testing upload speed...")
                upload_speed = speed_test_module.upload() / 1000000
                print("Upload Speed: " + str(round(upload_speed, 2)) + "Mbit/s")
                print("Testing server ping...")
                server_names = []
                speed_test_module.get_servers(server_names)
                server_ping = speed_test_module.results.ping
                print("Ping: " + str(server_ping) + "s")
            if len(command_args) >= 2:
                if "-d" in command_args:
                    print("Testing download speed...")
                    download_speed = speed_test_module.download() / 1000000
                    print("Download Speed: " + str(round(download_speed, 2)) + "Mbit/s")
                if "-u" in command_args:
                    print("Testing upload speed...")
                    upload_speed = speed_test_module.upload() / 1000000
                    print("Upload Speed: " + str(round(upload_speed, 2)) + "Mbit/s")
                if "-p" in command_args:
                    print("Testing server ping...")
                    server_names = []
                    speed_test_module.get_servers(server_names)
                    server_ping = speed_test_module.results.ping
                    print("Ping: " + str(server_ping) + "s")

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
            print("Notch version 1.1.0")
            print("Build 1003")
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
