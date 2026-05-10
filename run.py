import subprocess
import sys
from pathlib import Path

# Change to python_app directory and run the app
python_app_dir = Path(__file__).parent / "python_app"
result = subprocess.run(
    [sys.executable, "run.py"],
    cwd=python_app_dir,
)
sys.exit(result.returncode)
