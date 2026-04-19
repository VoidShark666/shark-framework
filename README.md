```markdown

\# 🦈 SHARK Framework - Advanced Cryptographic Transport Layer



\[!\[Python](https://img.shields.io/badge/Python-3.10%2B-red?style=for-the-badge\&logo=python\&logoColor=white)](https://python.org)

\[!\[License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)](LICENSE)

\[!\[Crypto](https://img.shields.io/badge/Crypto-AES--256--CBC%20%7C%20RSA--4096-red?style=for-the-badge)](https://pycryptodome.org)



```text

╔═══════════════════════════════════════════════════════════════════════════════╗

║                                                                               ║

║      ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄      ║

║     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ║

║     ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀      ║

║     ▐░▌        ▐░▌▐░▌        ▐░▌▐░▌        ▐░▌▐░▌        ▐░▌▐░▌               ║

║     ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌        ▐░▌▐░█▄▄▄▄▄▄▄▄▄      ║

║     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌        ▐░▌▐░░░░░░░░░░░▌     ║

║     ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌        ▐░▌ ▀▀▀▀▀▀▀▀▀█░▌     ║

║     ▐░▌           ▐░▌        ▐░▌▐░▌           ▐░▌        ▐░▌           ▐░▌     ║

║     ▐░▌           ▐░▌        ▐░▌▐░▌           ▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌     ║

║     ▐░▌           ▐░▌        ▐░▌▐░▌           ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ║

║      ▀             ▀          ▀  ▀             ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀      ║

║                                                                               ║

║                      SECURE ENCRYPTION \& TRANSPORT LAYER                      ║

║                                 v3.0 - "Mako"                                 ║

╚═══════════════════════════════════════════════════════════════════════════════╝

```



\## ⚠️ IMPORTANT DISCLAIMER

This software is provided for \*\*educational and research purposes only\*\*. The authors do not condone or support any illegal use. You are solely responsible for compliance with all applicable laws. Use only on systems you own or have explicit permission to test.



\## 🎯 Overview

\*\*SHARK Framework\*\* is a modular cryptographic transport library implementing hybrid encryption (RSA-4096 + AES-256-CBC) with UDP-based reliable transmission and anti-forensic capabilities. It is designed to demonstrate advanced networking and security principles.



\## ✨ Key Features

\- \*\*Hybrid Cryptography\*\*: RSA-4096 OAEP wraps AES-256-CBC session keys.

\- \*\*Reliable UDP\*\*: Custom ACK-based retransmission logic (up to 5 retries).

\- \*\*Anti-Forensics\*\*: 

&#x20;   - Sandbox \& Virtual Machine detection.

&#x20;   - Debugger identification.

&#x20;   - Secure memory management.

\- \*\*DPI Evasion\*\*: Dynamic magic headers and traffic chaffing (random noise packets).

\- \*\*Professional TUI\*\*: Real-time dashboards with a Dark Red aesthetic.



\## 🏗 Architecture

\- `shark\_core.py` — The core engine (OOP-based classes for Encryption/Transport).

\- `shark\_predator.py` — Client implementation for encrypting and sending files.

\- `shark\_base.py` — Server implementation for receiving and decrypting data.

\- `generate\_keys.py` — Tool for RSA-4096 keypair generation.



\## 📦 Installation



```bash

\# Clone the repository

git clone \[https://github.com/yourusername/shark-framework.git](https://github.com/yourusername/shark-framework.git)

cd shark-framework



\# Install dependencies

pip install pycryptodome rich

```



\## 🚀 Quick Start



\### 1. Generate Security Keys

On your base machine, generate your RSA 4096-bit keypair:

```bash

python generate\_keys.py

```

\*Keep `shark\_private.pem` secure. Embed `shark\_public.pem` into your `shark\_predator.py` script.\*



\### 2. Start the Receiver (Base)

```bash

python shark\_base.py ./received\_files

```



\### 3. Transmit Data (Predator)

```bash

python shark\_predator.py <path\_to\_file> <target\_ip>

```



\## 🔒 Security Model

| Threat | Mitigation |

|--------|------------|

| Sniffing | RSA-4096 + AES-256 Encryption |

| Traffic Analysis | Chaffing \& Hourly Rotating Headers |

| Forensic Dumps | In-memory key wiping |

| Sandboxing | Active VM/Debugger Checks |



\## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.



\## 📞 Contact

\- \*\*Developer\*\*: voidshark666

\- \*\*Email\*\*: voidshark666@proton.me

\- \*\*Status\*\*: Research \& Development



\---

\*Created by voidshark666. Stay anonymous. Stay secure.\*



