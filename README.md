# Remote Access Local

I'm a cyber security student and this repository is a learning project demonstrating a minimal remote-control client and server implemented in Python. The code and build artifacts are intended for study, local testing, and classroom exercises only.

> **⚠ WARNING — FOR EDUCATIONAL USE ONLY**
>
> Do NOT use this software to access, damage, or control machines you do not own or do not have explicit written permission to test. Misuse may be illegal and unethical. If you publish or share this code, include the same clear legal and ethical disclaimer and remove any sensitive data.
# ⚡ Remote Access — Student Demo

> A compact, polished README for demos and presentations.

---

## TL;DR
- Student project: lightweight Python remote-control (server + client).
- Intended for learning and safe lab testing only.
- Use `START_ULTIMATE.pyw` to quickly save a test IP to `LAST_IP.txt` and run the server.

---

## Quick demo steps (host -> VM)
1. On the host (run server):

```powershell
python START_ULTIMATE.pyw    # GUI prompt saves LAST_IP.txt
# or
python server_professional.py
```

2. On the VM (run client):

```powershell
$ip = Get-Content .\LAST_IP.txt
.\remotecontrol.exe --server $ip --port 5555
# or
python client_control.py --server $ip --port 5555
```

---

## Safe test walkthrough (host + VM)
Follow these concise steps to test locally in a safe environment. These assume the host and VM are on the same LAN or bridged network.

Host (run the server)
1. Start the server GUI or the console server on the host:

```powershell
python START_ULTIMATE.pyw    # launcher that saves LAST_IP.txt
# or
python server_professional.py
```

2. If you used the launcher, copy the IP it saved into `LAST_IP.txt` (or enter the host LAN IP when prompted). Example host IP: `192.168.117.1`.

3. Ensure the host firewall allows incoming TCP on port 5555 while testing (remove rule after):

```powershell
# requires admin
New-NetFirewallRule -DisplayName 'RemoteControl 5555' -Direction Inbound -LocalPort 5555 -Protocol TCP -Action Allow
```

VM (run the client)
1. Transfer or copy `LAST_IP.txt` from the host to the VM (shared folder, SCP, or manual copy/paste).

2. On the VM use the saved IP to run the client (PowerShell):

```powershell
$ip = Get-Content .\LAST_IP.txt
$env:SERVER_IP = $ip
python client_control.py --port 5555

# or if you have the built exe:
.\remotecontrol.exe --server $ip --port 5555
```

3. If connection fails, run these checks on the VM:

```powershell
Test-Connection -ComputerName $ip -Count 2
Test-NetConnection -ComputerName $ip -Port 5555
```

When testing is finished, remove any temporary firewall rule on the host and delete `LAST_IP.txt` when you no longer need it.

---

## Student note
This repo is my lab work as a cyber security student. It demonstrates basic remote-control concepts (frame streaming, control commands). It's not intended for distribution beyond controlled, authorized exercises.

> **⚠ IMPORTANT:** Do **not** run this against systems you don't own or don't have explicit permission to test. Always follow legal and ethical guidelines.

---

## Troubleshooting & checks
- From the VM, verify you can reach the host and port before running the client:

```powershell
# ping host
Test-Connection -ComputerName 192.168.117.1 -Count 2
# check TCP port
Test-NetConnection -ComputerName 192.168.117.1 -Port 5555
```

- On the host, confirm the server is listening on port 5555:

```powershell
netstat -an | Select-String ":5555"
```

---

## Notes
- The `build/` directory contains PyInstaller outputs and can be regenerated. Do not commit local test files (e.g., `LAST_IP.txt`) — `.gitignore` already excludes them.

## License
This project is licensed under the MIT License — see `LICENSE`.
.\remotecontrol.exe --server $ip --port 5555
```

3. If connection fails, run these checks on the VM:

```powershell
Test-Connection -ComputerName $ip -Count 2
Test-NetConnection -ComputerName $ip -Port 5555
```

When testing is finished, remove any temporary firewall rule on the host and delete `LAST_IP.txt` when you no longer need it.


Safety & ethics (important)
- This repository contains remote-control tooling. Only run it on systems you own or on targets where you have explicit authorization.
- Do NOT hard-code private or production IP addresses in source files. The project uses environment variables and CLI flags so you can test safely without editing code.
- If you publish this project (for a demo, assignment, or portfolio), include the same clear legal and ethical disclaimer and remove any sensitive data.

Troubleshooting & checks
- From the VM, verify you can reach the host and port before running the client:

```powershell
# ping host
Test-Connection -ComputerName 192.168.117.1 -Count 2
# check TCP port
Test-NetConnection -ComputerName 192.168.117.1 -Port 5555
```

- On the host, confirm the server is listening on port 5555:

```powershell
netstat -an | Select-String ":5555"
```

Notes
- The `build/` directory contains PyInstaller outputs and can be regenerated. Do not commit local test files (e.g., `LAST_IP.txt`) — `.gitignore` already excludes them.

License
This project is licensed under the MIT License — see `LICENSE`.
