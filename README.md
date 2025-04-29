# runner_wiseportcheck

This script checks the status of specified TCP ports on a given IP address.

## Functionality

- Takes an IP address and a comma-separated list of TCP ports as input.
- For each port, it attempts to establish a TCP connection.
- If the connection is successful:
    - It tries to receive a banner from the service.
    - If no banner is received immediately, it sends a basic HTTP GET request and attempts to read the response.
- It prints the status of each port (open, closed due to error, or timed out) along with any received banner or HTTP response.

## Usage

```bash
python app.py --ip_address <TARGET_IP> --tcp_ports <PORT1,PORT2,PORT3,...>
```

**Example:**

```bash
python app.py --ip_address 192.168.1.1 --tcp_ports 80,443,22
```

## Exit Codes

- **0:** The script completed successfully, attempting all specified ports without connection errors (ports might be closed, but the check itself didn't fail).
- **1:** An error occurred during execution. This could be due to:
    - Invalid command-line arguments (e.g., non-integer port number).
    - Connection timeouts.
    - Other socket errors (e.g., connection refused, host unreachable).
    - IP address resolution errors.