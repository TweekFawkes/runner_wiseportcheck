import argparse

### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###

try:
    import socket
except ImportError:
    print("Please install requirements.txt first: pip install -r requirements.txt")
    exit(1)

### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--ip_address', required=True, help='IP Address')
        parser.add_argument('--tcp_ports', required=True, help='TCP Ports, comma separated (e.g. 80,443,22)')
        args = parser.parse_args()

        ip_address = args.ip_address
        list_tcp_ports = args.tcp_ports.split(',')
        any_connection_errors = False # Flag to track connection issues
        for tcp_port_str in list_tcp_ports:
            try:
                tcp_port = int(tcp_port_str.strip()) # Strip whitespace and convert
            except ValueError:
                print(f"[!] Invalid port value: '{tcp_port_str}'. Skipping.")
                any_connection_errors = True # Consider invalid input an error for exit code
                continue # Skip to the next port in the list

            ### --- Port Check Logic Start --- ###
            print(f"\n# Attempting to connect to {ip_address}:{tcp_port}...")
            sock = None
            try:
                sock = socket.create_connection((ip_address, tcp_port), timeout=5)
                print(f"[+] Port {tcp_port} appears to be open.")
            
                # Try receiving banner
                sock.settimeout(3) # Short timeout for banner grab
                try:
                    banner = sock.recv(1024)
                    if banner:
                        print(f"## Received Banner:\n{banner.decode(errors='ignore')}")
                    else:
                        # This case (empty banner immediately) is less common than a timeout
                        print("[-] Connection closed immediately by server without banner.")
                        
                except socket.timeout:
                    print("[-] No banner received immediately. Assuming HTTP or similar service.")
                    # Send HTTP GET request
                    http_get = f"GET / HTTP/1.1\\r\\nHost: {ip_address}\\r\\nConnection: close\\r\\n\\r\\n".encode()
                    print(f"[*] Sending HTTP GET request...")
                    print(f"\n--- Request ---\n{http_get.decode()}\n---------------") # Print the request
                    try: # Nested try for sending/receiving HTTP
                        sock.sendall(http_get)
                    
                        # Receive response
                        response = b""
                        # Set a longer timeout for receiving HTTP response
                        sock.settimeout(10) 
                        while True:
                            try:
                                chunk = sock.recv(4096)
                                if not chunk:
                                    break
                                response += chunk
                            except socket.timeout:
                                print("[-] Timed out waiting for HTTP response.")
                                break # Stop receiving if timeout occurs
                            except socket.error as e:
                                print(f"[!] Socket error receiving HTTP response: {e}")
                                break
                        if response:
                            decoded_response = response.decode(errors='ignore')
                            if len(decoded_response) > 10000:
                                print(f"## Received Response (truncated to 10000 chars):\n{decoded_response[:10000]}...")
                            else:
                                print(f"## Received Response:\n{decoded_response}")
                        else:
                            print("[-] No response received after GET request.")
                    except socket.error as e:
                        print(f"[!] Error sending HTTP GET request: {e}")
                    except Exception as e:
                         print(f"[!] Unexpected error during HTTP communication: {e}")

                except Exception as e:
                    print(f"[!] Error during banner grab: {e}")
        
            except socket.timeout:
                print(f"[-] Connection to {ip_address}:{tcp_port} timed out.")
                any_connection_errors = True
            except socket.error as e:
                print(f"[-] Could not connect to {ip_address}:{tcp_port}. Error: {e}")
                any_connection_errors = True
            finally:
                if sock:
                    sock.close()
        print("### --- Port Check Logic End --- ###\n")
        ###
        return 1 if any_connection_errors else 0
    except socket.gaierror as e:
        print(f"[!] Error resolving IP address or connecting: {e}")
        return 1 # Return 1 on resolution error
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        return 1

### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###

if __name__ == "__main__":
    exit(main())