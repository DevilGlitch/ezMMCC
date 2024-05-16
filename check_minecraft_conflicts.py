#Old Simple Drag and Run Paired with OldInstall.bat
import os
import zipfile

def find_conflicting_jars(jar_files):
    conflicts = {}
    for jar_file in jar_files:
        with zipfile.ZipFile(jar_file, 'r') as z:
            class_files = [name for name in z.namelist() if name.endswith('.class')]
            for class_file in class_files:
                if class_file in conflicts:
                    conflicts[class_file].append(jar_file)
                else:
                    conflicts[class_file] = [jar_file]
    conflicting_jars = set()
    for class_file, jars in conflicts.items():
        if len(jars) > 1:
            conflicting_jars.update(jars)
    return conflicting_jars

def write_to_file(conflicting_jars):
    with open("conflicting_jars.txt", "w") as file:
        if conflicting_jars:
            file.write("Conflicts found in the following jar files:\n")
            for jar_file in conflicting_jars:
                file.write(f"  {jar_file}\n")
        else:
            file.write("No conflicts found.")

def main():
    jar_files = [file for file in os.listdir('.') if file.endswith('.jar')]
    conflicting_jars = find_conflicting_jars(jar_files)
    write_to_file(conflicting_jars)
    print("Output written to conflicting_jars.txt.")

if __name__ == "__main__":
    main()
