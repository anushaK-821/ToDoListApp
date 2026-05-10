import shutil
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def run_step(args, label):
    print(f"[{label}] {' '.join(args)}")
    subprocess.run(args, check=True, cwd=BASE_DIR)


def ensure_env_file():
    env_file = BASE_DIR / ".env"
    env_example = BASE_DIR / ".env.example"

    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("[setup] Created .env from .env.example")


def ensure_dependencies():
    required = ["flask", "pymongo", "dotenv"]
    missing = []

    for module_name in required:
        try:
            __import__(module_name)
        except ModuleNotFoundError:
            missing.append(module_name)

    if missing:
        run_step([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], "deps")


def main():
    ensure_env_file()
    ensure_dependencies()
    run_step([sys.executable, "seed_user.py"], "seed")
    run_step([sys.executable, "app.py"], "run")


if __name__ == "__main__":
    main()
