from pathlib import Path

f_path = Path(__file__)
print(f_path.root)          # \
print(f_path.anchor)        # c:\

print(f_path.parents)       # <WindowsPath.parents>
[print(p) for p in f_path.parents]
# c:\Users\simon\Documents\IIS\Tech_Notes\Programming_Language\python
# c:\Users\simon\Documents\IIS\Tech_Notes\Programming_Language
# c:\Users\simon\Documents\IIS\Tech_Notes
# c:\Users\simon\Documents\IIS
# c:\Users\simon\Documents
# c:\Users\simon
# c:\Users
# c:\
