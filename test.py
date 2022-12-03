import os
import subprocess

print(os.getenv('PATH'))
path = "D:/a/ActionsRamblings/ActionsRamblings/IMG_2600.CR2"
print(os.path.exists(path))
subprocess.check_output(["Adobe DNG Converter", path])
