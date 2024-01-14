import os
import subprocess

test_path = 'test'

# Iterate over all files in the directory
for filename in os.listdir(test_path):
    if filename.endswith('.py'):
        script_path = os.path.join(test_path, filename)

        print(f"--------- {script_path} -----------")
        result = subprocess.run(['python', script_path])
        if result.returncode != 0:
            print(f"return code : {result.returncode}", end="\n\n")


