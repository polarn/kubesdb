import subprocess

Version = subprocess.check_output(["git", "describe"]).strip().decode("utf-8")
