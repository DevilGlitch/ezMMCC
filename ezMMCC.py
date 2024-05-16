import os
import zipfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
import psutil

loader = 0

def is_process_running(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            return True
    return False

def find_conflicting_jars(jar_files, progress_bar, progress_label, progress_popup):
    conflicts = {}
    total_files = len(jar_files)
    
    for index, jar_file in enumerate(jar_files):
        with zipfile.ZipFile(jar_file, 'r') as z:
            class_files = [name for name in z.namelist() if name.endswith('.class')]
            for class_file in class_files:
                if class_file in conflicts:
                    conflicts[class_file].append(jar_file)
                else:
                    conflicts[class_file] = [jar_file]
        
        progress_bar['value'] = (index + 1) / total_files * 100
        progress_label.config(text=f"Processing {index + 1}/{total_files} files...")
        progress_bar.update()
    
    conflicting_jars = set()
    for class_file, jars in conflicts.items():
        if len(jars) > 1:
            conflicting_jars.update(jars)
    
    progress_popup.destroy()
    return conflicting_jars

def write_to_file(conflicting_jars, folder_path):
    file_path = os.path.join(folder_path, "conflicting_jars.txt")
    with open(file_path, "w") as file:
        if conflicting_jars:
            file.write("Conflicts found in the following jar files:\n")
            for jar_file in conflicting_jars:
                file.write(f"  {jar_file}\n")
        else:
            file.write("No conflicts found.")
    return file_path

def process_jars(folder_path, progress_bar, progress_label, progress_popup, root):
    jar_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.jar')]
    conflicting_jars = find_conflicting_jars(jar_files, progress_bar, progress_label, progress_popup)
    result_file = write_to_file(conflicting_jars, folder_path)
    
    with open(result_file, "r") as file:
        conflicts = file.read()
    
    messagebox.showinfo("Conflicting Jars", conflicts)
    
    # Run script in the 'mods' subfolder
    mods_folder = os.path.join(folder_path, "mods")
    if os.path.exists(mods_folder):
        os.system(f"start cmd /c \"cd {mods_folder} && your_script_here\"")

    root.quit()

def start_processing(folder_path, progress_bar, progress_label, progress_popup, root):
    thread = Thread(target=process_jars, args=(folder_path, progress_bar, progress_label, progress_popup, root))
    thread.start()

def select_folder(root):
    folder_path = filedialog.askdirectory()
    if folder_path:
        progress_popup = tk.Toplevel(root)
        progress_popup.title("Processing...")
        progress_popup.geometry("350x100")

        progress_bar = ttk.Progressbar(progress_popup, orient="horizontal", length=300, mode="determinate")
        progress_label = tk.Label(progress_popup, text="Starting processing...")

        progress_bar.pack(pady=20)
        progress_label.pack(pady=10)
        
        root.update()
        start_processing(folder_path, progress_bar, progress_label, progress_popup, root)

def get_current_user():
    return os.getlogin()

def auto_detect():
    global loader
    loader = 0
    modrinth_running = is_process_running("modrinth app.exe")
    curseforge_running = is_process_running("curseforge.exe")

    if curseforge_running:
        loader = 1
        user_name = get_current_user()
        selected_instance = select_instance_folder(user_name)
        if selected_instance:
            messagebox.showinfo("Auto Detect", f"Selected instance: {selected_instance}")
            # Construct the mods folder path
            mods_folder = os.path.join("C:\\Users", user_name, "curseforge", "minecraft", "Instances", selected_instance, "mods")
            # Save the mods folder path to a temporary variable
            temp_path_variable = mods_folder
        else:
            messagebox.showinfo("Auto Detect", "Failed")
            return
    elif modrinth_running:
        loader = 2
        user_name = get_current_user()
        selected_instance = select_instance_folder(user_name)
        if selected_instance:
            messagebox.showinfo("Auto Detect", f"Selected instance: {selected_instance}")
            # Construct the mods folder path
            mods_folder = os.path.join("C:\\Users", user_name, "AppData", "Roaming", "com.modrinth.theseus", "profiles", selected_instance, "mods")
            # Save the mods folder path to a temporary variable
            temp_path_variable = mods_folder
    else:
        messagebox.showinfo("Auto Detect", "Neither Modrinth nor CurseForge is running.")
        return
    
    # Run Main Script
    manual_processing(temp_path_variable)

def select_instance_folder(user_name):
    global loader  
    # Construct the path to the Instances folder
    if loader == 1:
        instance_folder = os.path.join("C:\\Users", user_name, "curseforge", "minecraft", "Instances")
    elif loader == 2:
        instance_folder = os.path.join("C:\\Users", user_name, "AppData", "Roaming", "com.modrinth.theseus", "profiles")
    
    # Get a list of all folders in the Instances folder
    instance_folders = [f.name for f in os.scandir(instance_folder) if f.is_dir()]
    
    # Create a Tkinter window for multiple choice selection
    instance_selection_window = tk.Toplevel()
    instance_selection_window.title("Select Instance")
    instance_selection_window.geometry("450x300")  # Increased width and height

    # Label for instructions
    instruction_label = tk.Label(instance_selection_window, text="Select the instance:")
    instruction_label.pack(pady=10)
    
    # Variable to store selected instance
    selected_instance = tk.StringVar()
    
    # Function to set the selected instance
    def set_selected_instance():
        selected_instance.set(instance_listbox.get(tk.ACTIVE))
        instance_selection_window.destroy()
    
    # Listbox to display instance folders
    instance_listbox = tk.Listbox(instance_selection_window, selectmode=tk.SINGLE)
    for instance_folder in instance_folders:
        instance_listbox.insert(tk.END, instance_folder)
    instance_listbox.place(relx=0.5, rely=0.4, anchor=tk.CENTER, relwidth=0.75, relheight=0.6)
    
    # Button to confirm selection
    select_button = ttk.Button(instance_selection_window, text="Select", command=set_selected_instance)
    select_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
    
    instance_selection_window.grab_set()
    instance_selection_window.wait_window()
    
    return selected_instance.get()

def manual_processing(folder_path):
    # Create progress popup
    progress_popup = tk.Toplevel()
    progress_popup.title("Processing...")
    progress_popup.geometry("350x100")

    progress_bar = ttk.Progressbar(progress_popup, orient="horizontal", length=300, mode="determinate")
    progress_label = tk.Label(progress_popup, text="Starting processing...")

    progress_bar.pack(pady=20)
    progress_label.pack(pady=10)

    root.update()
    process_jars(folder_path, progress_bar, progress_label, progress_popup, root)

    # After processing, delete the temporary path variable
    del folder_path

def run_script():
    messagebox.showinfo("Run Script", "Please select a folder manually first.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("ezMMCC")

    # Set default window size
    root.geometry("350x150")

    # Create style for buttons
    style = ttk.Style()
    style.configure('TButton', font=('calibri', 10, 'bold'), foreground='black')

    # Create frame for buttons and center it
    button_frame = ttk.Frame(root)
    button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Create Auto Detect button
    auto_detect_button = ttk.Button(button_frame, text="Auto Detect", command=auto_detect)
    auto_detect_button.pack(side="left", padx=5)

    # Create Manual button
    manual_button = ttk.Button(button_frame, text="Manual", command=lambda: select_folder(root))
    manual_button.pack(side="left", padx=5)

    root.mainloop()
