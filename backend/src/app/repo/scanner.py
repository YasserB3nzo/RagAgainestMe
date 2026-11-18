import subprocess
import sys
from pathlib import Path

ALLOWED_EXTENSIONS = {".py", ".md"}
SKIP_DIRS = {"node_modules", ".venv", "venv", "build", "dist", "__pycache__", "vendor", "third_party"}
REPO_PATH = "/home/y4s3r/Desktop/Rag/data/repos/python-dotenv"

def get_commit(repo: Path) -> str:
    """Return the current commit hash of the repo."""
    # f = open("/home/y4s3r/Desktop/Rag/data/repos/python-dotenv/.git/refs/heads/main", "r")
    # print(f.read)
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

    # hint: subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
    ...


def list_tracked_files(repo: Path) -> list[str]:
    """Return every file path Git tracks, relative to the repo root."""
    # hint: same as above with "ls-files", then .splitlines()
    result = subprocess.run(
        ["git", "-C", str(repo), "ls-files"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.splitlines()

    ...


def is_eligible(path: str) -> bool:
    list_of = path.split("/")
    for folder in list_of:
        if folder in SKIP_DIRS:
            return False
        
    file_name = list_of[-1]
    if file_name.lower().endswith((".py", ".md")):
      return True

    return False
    ...


def is_text_file(path: Path) -> bool:
    """True if the file has no null bytes and decodes as UTF-8."""
    # hint: path.read_bytes(), b"\x00" in data, try/except UnicodeDecodeError
    ...


def scan(repo: Path) -> list[str]:
    """Combine everything: tracked + eligible + text files."""
    ...


if __name__ == "__main__":
    repo = Path(sys.argv[1]).resolve()
    try:
        print("commit:", get_commit(repo))
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while fetching commit: {e}")
        sys.exit(1)
    files = scan(repo)
    for f in files:
        print(f)
    print(f"{len(files)} eligible files")
