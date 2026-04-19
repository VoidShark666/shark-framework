import sys
import os
# ццц
from shark_core import SharkBase, execute_safely, show_dashboard

def run_base():
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "./incoming"
    os.makedirs(output_dir, exist_ok=True)

    # ццц
    show_dashboard({"Role": "Base", "Listening Port": "31337", "Output Dir": output_dir, "Status": "Awaiting Targets"})

    # ццц
    if not os.path.exists("shark_private.pem"):
        print("[!] Ошибка: shark_private.pem не найден!")
        sys.exit(1)

    base = SharkBase("shark_private.pem", output_dir)
    base.run()

if __name__ == "__main__":
    execute_safely(run_base, lambda: print("System Error 0x80040154"))