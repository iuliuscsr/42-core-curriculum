#!/usr/bin/env python3
import sys
import os
import site


def detect_venv() -> bool:
    return sys.prefix != sys.base_prefix


def get_pkg_path() -> str:
    try:
        pkg = site.getsitepackages()
        return pkg[0] if pkg else "Unknown"
    except Exception:
        return "Unknown"


def env_stats() -> dict[str, str]:
    if detect_venv():
        return {
            "status" : "Welcome to the construct\n",
            "python" : sys.executable,
            "venv" : os.path.basename(sys.prefix),
            "path" : sys.prefix,
            "message" : "SUCCESS: You're in an isolated environment!\n"
            "Safe to install packages without affecting\n"
            "the global system.", 
            "pkg_path" : get_pkg_path()
            }
    return {
        "status" : "You're still plugged in",
        "python" : sys.executable,
        "venv" : "None detected",
        "message" : ("You're in the global environment!\n" 
        "The machines can see everything you install.\n\n" 
        "To enter the construct, run:\n" 
        "python -m venv matrix_env\n" 
        "source matrix_env/bin/activate # On Unix\n" 
        "matrix_env\\Scripts\\activate # On Windows")
    }


def main() -> None:
    info = env_stats()
    in_venv = detect_venv()

    print(f"MATRIX STATUS: {info['status']}")
    print(f"Current Python: {info['python']}")
    print(f"Virtual Environment: {info['venv']}")

    if in_venv:
        print(f"Environment Path: {info['path']}")

    print(f"\n{info['message']}")

    if in_venv:
        print(f"\nPackage installation path:\n{info['pkg_path']}")


if __name__ == "__main__":
    main()
