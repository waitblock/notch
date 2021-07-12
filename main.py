import whois
import subprocess
import requests
import dns.resolver
import socket
import speedtest
import psutil
import sys
import warnings
import smtplib
import sslcheck

if sys.platform != "darwin":
    warnings.warn("This application is intended for use on MacOSX>=10.15.7.")


def main():
    print("Notch 1.3.0 (v1.3.0_1006)")
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
            print("This command is currently disabled due to an issue with the speedtest library.")
            # command_args = command.split(" ")
            # print("Initializing...")
            # speed_test_module = speedtest.Speedtest()
            # if len(command_args) == 1:
            #     print("Testing download speed...")
            #     download_speed = speed_test_module.download() / 1000000
            #     print("Download Speed: " + str(round(download_speed, 2)) + "Mbit/s")
            #     print("Testing upload speed...")
            #     upload_speed = speed_test_module.upload() / 1000000
            #     print("Upload Speed: " + str(round(upload_speed, 2)) + "Mbit/s")
            #     print("Testing server ping...")
            #     server_names = []
            #     speed_test_module.get_servers(server_names)
            #     server_ping = speed_test_module.results.ping
            #     print("Ping: " + str(server_ping) + "s")
            # if len(command_args) >= 2:
            #     if "-d" in command_args:
            #         print("Testing download speed...")
            #         download_speed = speed_test_module.download() / 1000000
            #         print("Download Speed: " + str(round(download_speed, 2)) + "Mbit/s")
            #     if "-u" in command_args:
            #         print("Testing upload speed...")
            #         upload_speed = speed_test_module.upload() / 1000000
            #         print("Upload Speed: " + str(round(upload_speed, 2)) + "Mbit/s")
            #     if "-p" in command_args:
            #         print("Testing server ping...")
            #         server_names = []
            #         speed_test_module.get_servers(server_names)
            #         server_ping = speed_test_module.results.ping
            #         print("Ping: " + str(server_ping) + "s")

        if command == "netcount":
            stats = psutil.net_io_counters()
            print("Total bytes sent: " + str(stats.bytes_sent))
            print("Total bytes received: " + str(stats.bytes_recv))
            print("Total packets sent: " + str(stats.packets_sent))
            print("Total packets received: " + str(stats.packets_recv))
            print("Total input errors: " + str(stats.errin))
            print("Total output errors: " + str(stats.errout))
            print("Total drop inputs: " + str(stats.dropin))
            print("Total drop outputs: " + str(stats.dropout))

        if command[0:4] == "ping":
            print("Pinging host server...")
            ping = subprocess.Popen(
                ["ping", "-c", "3", command[5:]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out, error = ping.communicate()
            print(out.decode('utf-8'))

        if command[0:4] == "port":
            command_args = command.split(" ")
            if len(command_args) == 1:
                print("Missing required argument: <port>")
            if len(command_args) == 2:
                port = command_args[1]
                port_testing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                response = port_testing_socket.connect_ex(('127.0.0.1', int(port)))
                if response == 0:
                    print("Port " + port + " on 127.0.0.1 (localhost) is open.")
                else:
                    print("Port " + port + " on 127.0.0.1 (localhost) is closed.")
                port_testing_socket.close()
            if len(command_args) == 3:
                try:
                    host = command_args[1]
                    port = command_args[2]
                    port_testing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    response = port_testing_socket.connect_ex((host, int(port)))
                    if response == 0:
                        print("Port " + port + " on " + socket.gethostbyname(host) + " is open.")
                    else:
                        print("Port " + port + " on " + socket.gethostbyname(host) + " is closed.")
                    port_testing_socket.close()
                except socket.gaierror:
                    print("The host server does not exist or is offline.")
            else:
                print("Maximum number of arguments is 2: [host] <port>")

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

        if command[0:4] == "smtp":
            smtp_server_name = command[5:]
            if command[5:] == "":
                print("Missing required argument: <host>")
            else:
                print("Press Ctrl-C to close the connection.")
                print("Querying server...")
                try:
                    smtp_server_test = smtplib.SMTP(smtp_server_name, timeout=30)
                    response = smtp_server_test.noop()
                    smtp_server_test.close()
                    print("The SMTP host server " + smtp_server_name + " returned " + response[1].decode() + " with code " + str(response[0]) + ".")
                except socket.gaierror:
                    print("The host does not exist or is offline.")
                except socket.timeout:
                    print("The connection timed out.")
                except ConnectionRefusedError:
                    print("The connection was disconnected or refused by the host.")
                except KeyboardInterrupt:
                    try:
                        smtp_server_test.close()
                    except UnboundLocalError:
                        pass

        if command[0:3] == "ssl":
            ssl_server_name = command[4:]
            sslcheck.main(ssl_server_name)

        if command == "version":
            print("Notch version 1.2.1")
            print("Build 1005")
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
