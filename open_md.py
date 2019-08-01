import subprocess
import os

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

output = "this is the thing I want to describe"

write_to_clipboard(output)
os.system('open "x-marked://paste"')


