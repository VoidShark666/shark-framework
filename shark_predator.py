import sys
# Импортируем твои классы и функции из ядра
from shark_core import SharkPredator, execute_safely, show_dashboard

# ВСТАВЬ СЮДА СВОЙ ПУБЛИЧНЫЙ КЛЮЧ
SHARK_PUBLIC_KEY = b"""-----BEGIN PUBLIC KEY-----
      here is the key
-----END PUBLIC KEY-----"""

def run_predator():
    if len(sys.argv) < 3:
        print("Usage: python shark_predator.py <file> <target_ip>")
        sys.exit(1)

    file_path = sys.argv[1]
    target_ip = sys.argv[2]

    show_dashboard({"Role": "Predator", "Target IP": target_ip, "File": file_path, "Status": "Encrypting & Sending"})

    # ццц
    predator = SharkPredator(SHARK_PUBLIC_KEY, target_ip)
    try:
        predator.send_file(file_path)
        print("\n[bold green][+] Файл успешно отправлен![/bold green]")
    except Exception as e:
        print(f"\n[bold red][!] Ошибка при отправке: {e}[/bold red]")

if __name__ == "__main__":
    # ццц
    execute_safely(run_predator, lambda: print("System Error 0x80040154"))