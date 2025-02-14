import cv2
import face_recognition
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from concurrent.futures import ThreadPoolExecutor
import threading

class FaceOrganizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Face Organizer")
        
        # Configuration variables
        self.Fmodel = tk.StringVar(value="cnn")
        self.use_parallel = tk.BooleanVar(value=True)
        self.Face_A_Codes = []
        self.filenamea = []
        self.folder_a = ""
        self.folders_b = []
        self.output_folder = ""
        self.total_files = 0
        self.processed_files = 0
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Folder selection
        ttk.Button(main_frame, text="Select Folder A", command=self.select_folder_a).grid(
            row=0, column=0, pady=5, sticky=tk.W)
        self.lbl_folder_a = ttk.Label(main_frame, text="No folder selected")
        self.lbl_folder_a.grid(row=0, column=1, padx=10, sticky=tk.W)
        
        ttk.Button(main_frame, text="Add Folder B", command=self.add_folder_b).grid(
            row=1, column=0, pady=5, sticky=tk.W)
        self.lbl_folders_b = ttk.Label(main_frame, text="No folders selected")
        self.lbl_folders_b.grid(row=1, column=1, padx=10, sticky=tk.W)
        
        ttk.Button(main_frame, text="Select Output Folder", command=self.select_output).grid(
            row=2, column=0, pady=5, sticky=tk.W)
        self.lbl_output = ttk.Label(main_frame, text="No folder selected")
        self.lbl_output.grid(row=2, column=1, padx=10, sticky=tk.W)
        
        # Processing options
        options_frame = ttk.LabelFrame(main_frame, text="Processing Options", padding="10")
        options_frame.grid(row=3, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Label(options_frame, text="Detection Model:").grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(options_frame, textvariable=self.Fmodel, 
                    values=["cnn", "hog"], state="readonly").grid(row=0, column=1, sticky=tk.W)
        
        ttk.Checkbutton(options_frame, text="Parallel Processing", 
                       variable=self.use_parallel).grid(row=0, column=2, padx=20, sticky=tk.W)
        
        # Progress controls
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=4, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.btn_start = ttk.Button(main_frame, text="Start Processing", command=self.start_processing)
        self.btn_start.grid(row=5, columnspan=2, pady=10)
        
    def select_folder_a(self):
        self.folder_a = filedialog.askdirectory(title="Select Folder A (Reference Faces)")
        self.lbl_folder_a.config(text=self.folder_a)
        
    def add_folder_b(self):
        folder = filedialog.askdirectory(title="Select Folder B (Photos to Organize)")
        if folder:
            self.folders_b.append(folder)
            self.lbl_folders_b.config(text=f"{len(self.folders_b)} folders selected")
        
    def select_output(self):
        self.output_folder = filedialog.askdirectory(title="Select Output Folder")
        self.lbl_output.config(text=self.output_folder)
        
    def start_processing(self):
        if not self.validate_inputs():
            return
            
        self.btn_start.config(state='disabled')
        self.progress['value'] = 0
        self.total_files = sum(len(os.listdir(f)) for f in self.folders_b)
        self.processed_files = 0
        
        # Start processing in background thread
        threading.Thread(target=self.process_images, daemon=True).start()
        
    def validate_inputs(self):
        if not self.folder_a:
            messagebox.showerror("Error", "Please select Folder A")
            return False
        if not self.folders_b:
            messagebox.showerror("Error", "Please add at least one Folder B")
            return False
        if not self.output_folder:
            messagebox.showerror("Error", "Please select Output Folder")
            return False
        return True
        
    def process_images(self):
        try:
            self.process_folder_a()
            
            all_b_files = []
            for folder_b in self.folders_b:
                all_b_files.extend([(folder_b, f) for f in os.listdir(folder_b)])
            
            if self.use_parallel.get():
                with ThreadPoolExecutor() as executor:
                    for _ in executor.map(self.process_single_file, all_b_files):
                        self.update_progress()
            else:
                for file_info in all_b_files:
                    self.process_single_file(file_info)
                    self.update_progress()
            
            self.show_completion("Processing completed successfully!")
        except Exception as e:
            self.show_completion(f"Error: {str(e)}", error=True)
        finally:
            self.master.after(0, self.btn_start.config, {'state': 'normal'})
            
    def update_progress(self):
        self.processed_files += 1
        progress_value = (self.processed_files / self.total_files) * 100
        self.master.after(0, self.progress.configure, {'value': progress_value})
        
    def show_completion(self, message, error=False):
        self.master.after(0, messagebox.showinfo if not error else messagebox.showerror,
                         "Processing Complete" if not error else "Error",
                         message)
        
    def process_folder_a(self):
        self.Face_A_Codes.clear()
        self.filenamea.clear()
        
        for filename in os.listdir(self.folder_a):
            image_path = os.path.join(self.folder_a, filename)
            image = cv2.imread(image_path)
            if image is None:
                continue
            
            face_locations = face_recognition.face_locations(image, model=self.Fmodel.get())
            if not face_locations:
                continue
            
            try:
                encoding = face_recognition.face_encodings(
                    image, 
                    known_face_locations=face_locations, 
                    model="large"
                )[0]
            except IndexError:
                continue
            
            self.Face_A_Codes.append(encoding)
            self.filenamea.append(filename)
            
            face_folder = os.path.join(self.output_folder, filename)
            os.makedirs(face_folder, exist_ok=True)
            cv2.imwrite(os.path.join(face_folder, filename), image)
        
    def process_single_file(self, file_info):
        folder_b, filename = file_info
        image_path = os.path.join(folder_b, filename)
        image = cv2.imread(image_path)
        if image is None:
            return
        
        face_locations = face_recognition.face_locations(image, model=self.Fmodel.get())
        if not face_locations:
            nff_folder = os.path.join(self.output_folder, "NO_FACES_FOUND")
            os.makedirs(nff_folder, exist_ok=True)
            cv2.imwrite(os.path.join(nff_folder, filename), image)
            return
        
        match_found = False
        for face_location in face_locations:
            try:
                encoding = face_recognition.face_encodings(
                    image, 
                    known_face_locations=[face_location], 
                    model="large"
                )[0]
            except IndexError:
                continue
            
            results = face_recognition.compare_faces(self.Face_A_Codes, encoding, 0.5)
            for i, match in enumerate(results):
                if match:
                    match_found = True
                    face_folder = os.path.join(self.output_folder, self.filenamea[i])
                    os.makedirs(face_folder, exist_ok=True)
                    cv2.imwrite(os.path.join(face_folder, filename), image)
        
        if not match_found:
            nf_folder = os.path.join(self.output_folder, "NOT_FOUND")
            os.makedirs(nf_folder, exist_ok=True)
            cv2.imwrite(os.path.join(nf_folder, filename), image)

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceOrganizerApp(root)
    root.mainloop()
