
import glob
import os

fl = []

target = os.path.join("icons", "*.png")
for file in glob.glob(target):
	b = os.path.basename(file)
	fl.append(f"<file alias=\"{b}\">{file}</file>")

target = os.path.join("gui", "*.png")
for file in glob.glob(target):
	b = os.path.basename(file)
	fl.append(f"<file alias=\"gui-{b}\">{file}</file>")

target = os.path.join("gui", "*.gif")
for file in glob.glob(target):
	b = os.path.basename(file)
	fl.append(f"<file alias=\"gui-{b}\">{file}</file>")

target = os.path.join("fonts", "*.ttf")
for file in glob.glob(target):
	b = os.path.basename(file)
	fl.append(f"<file alias=\"font-{b}\">{file}</file>")

rfiles = "\n".join(fl)

out = f"""
<RCC>
<qresource>
{rfiles}
</qresource>
</RCC>
"""

print(out)
