"""Helpers that shell out to the operating system for batch jobs."""

import os
import subprocess


def archive_directory(directory: str, destination: str) -> int:
    return os.system(f"tar czf {destination} {directory}")


def run_batch_script(command: str) -> int:
    return subprocess.call(command, shell=True)
