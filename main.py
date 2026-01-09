# Here we start our way in thousand steps since one step
print("Program is started!")
from pathlib import Path

while True:
    folder_path = Path(input("Please enter the path of your folder: "))

    if folder_path.is_dir():
        print("Folder is exist. Selected folder:", folder_path)
        break
    else:
        print("It's not a folder. You need select path to folder.\n")


def scan_folder(folder_path):
    files = []
    total_size = 0

    for path in folder_path.rglob("*"):
        if path.is_file():
            files.append(path)
            total_size += path.stat().st_size

    return {"files": files, "total_size": total_size}


scan_result = scan_folder(folder_path)

print(f"Total files: {len(scan_result['files'])}")
print(f"Total size: {scan_result['total_size'] / 1024 / 1024:.2f} MB")
