import subprocess

def run_shell(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout

result = run_shell("free")
print(result)