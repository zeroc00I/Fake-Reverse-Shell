# Reverse Shell Troll 🧌
A Python-based honeypot that turns the tables on attackers by simulating a compromised system and capturing their credentials.

# Purpose 🎯
- Troll attackers who send reverse shell payloads
- Capture passwords and commands in real-time
- Waste attacker's time with infinite auth loops
- Study attacker behavior during engagements

# Key Features 🔥
- 🕵️ Real-time command logging
- 🔒 Covert password capture
- 💾 Fake Linux environment simulation
- 🔄 Persistent re-authentication prompts
- 📁 Automatic session logging

# How It Works ⚙️
## Attacker's Perspective
```bash
$ nc -lvnp 4444
Connected to prod-web-01 (10.0.3.67)
Linux prod-web-01 5.15.0-101-generic #111-Ubuntu
webadmin@prod-web-01:~$ ls
app.log	config	index.html	node_modules	package.json
webadmin@prod-web-01:~$ sudo -i
[sudo] password: █
Sorry, try again.
```
## Your Perspective
```bash
[+] Connected to attacker at 192.168.1.101:4444
[!] Attacker executed: ls
[!] Attacker executed: sudo -i
[!] Password attempt: p@ssw0rd123
[!] Password attempt: adminadmin
```
# Setup & Usage 🚀
## Clone Repository
```bash
git clone https://github.com/yourusername/reverse-shell-troll.git
cd reverse-shell-troll
```
## Configure Target

```python
FAKE_ENV = {
    "user": "webadmin",          # Change to match your scenario
    "hostname": "prod-web-01",   # Fake hostname
    "ip": "10.0.3.67"            # Fake server IP
}
```

## Edit these variables in main.py:

```python
ATTACKER_IP = 'X.X.X.X'  # Attacker's listening IP
ATTACKER_PORT = 4444     # Attacker's listening port
```

## Run the Trap

```bash
python3 main.py
```
# Behavioral Examples 🎭
## Attacker's Action	What They See	What You See

### Enters ls	Fake file listing	
```
[!] Attacker executed: ls
```
### Types password secret123	
```
Blank field with cursor	[!] Password attempt: secret123
```
### Runs uname -a	Fake kernel version	
```
[!] Attacker executed: uname -a
```

# Limitations ⚠️
- OS Specific: Currently mimics Linux only (TODO: Windows/Mac support)
- Netcat Dependent: Works best with basic nc listeners
- No SSL: Doesn't simulate encrypted connections (TODO: Add TLS)
- Basic Commands: Limited fake command responses (TODO: Expand list)
