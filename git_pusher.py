import os
import subprocess
import webbrowser

a = int(input ("123"))

if a == 123:

    def run_git_command(command):
        return subprocess.run(command, capture_output=True, text=True)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)

    print(f"📂 Робоча директорія: {current_dir}")

    if not os.path.isdir(".git"):
        print("❌ Помилка: Ця папка не є Git-репозиторієм!")
        print("Підказка: Виконайте 'git init' або покладіть цей скрипт у папку з проєктом.")
        input("Натисни ENTER для виходу...")
        exit()

    branch_name = input("Введи назву гілки для пушу: ").strip()
    commit_message = input("Що комітити? (повідомлення коміту): ").strip()

    try:
        print(f"🔄 Перемикання на гілку {branch_name}...")
        branches_result = run_git_command(["git", "branch"])
        branches = [b.strip().replace("* ", "") for b in branches_result.stdout.splitlines()]

        if branch_name in branches:
            subprocess.run(["git", "checkout", branch_name], check=True)
        else:
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)

        subprocess.run(["git", "add", "."], check=True)
    
        status = run_git_command(["git", "status", "--porcelain"])
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print("✅ Коміт створено.")
        else:
            print("ℹ️ Немає нових змін для коміту.")

        print(f"🚀 Надсилання у origin/{branch_name}...")
        result = subprocess.run(["git", "push", "-u", "origin", branch_name], capture_output=True, text=True)

        if result.returncode == 0:
            print(f"\n✨ Готово! Все в гілці: {branch_name}")
        else:
            print(f"\n❌ Помилка при пуші: {result.stderr}")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Помилка виконання команди: {e.stderr}")

    url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], text=True).strip()
    webbrowser.open(url.replace(".git", ""))

else:
    print("Вихід...")