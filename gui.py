import customtkinter as ctk
import tkinter as tk
from os_simulator import OS
from process import ProcessState

class UI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # APERANCE MODE AND COLOR THEME 
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        # TITLE & INITIAL SCREEN SIZE 
        self.title("OS Process Emulator")
        self.geometry("800x600")

        # INSANCE OF CLASS OS
        self.os = OS()
        
        # SCREEN EXPANSION DISTRUBUTION 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # MAIN FRAME FOR OTHER FRAMES AND WIDGETS 
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        # ERROR FRAME AND LABEL
        self.error_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.error_frame.grid(row=0, column=0, pady=(5, 0), sticky="ew")
        self.error_frame.grid_remove()  

        # Color setting for error_label
        self.error_label = ctk.CTkLabel(
            self.error_frame, 
            text="", 
            text_color="black",
            fg_color="#f7b2b2",  
            corner_radius=6,
            padx=10,
            pady=5
        )
        self.error_label.pack(padx=5, pady=5)
        
        
        # FRAME FOR UPPER CONTROLS 
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew") 
        
        
        # ENTRY FOR EXECUTION TIME 
        self.add_process_entry = ctk.CTkEntry(self.control_frame, placeholder_text="Execution Time")
        self.add_process_entry.pack(side=tk.LEFT, padx=5)

        # BUTTON TO ADD NEW PROCESS
        self.add_process_button = ctk.CTkButton(self.control_frame, text="Add Process", command=self.add_process)
        self.add_process_button.pack(side=tk.LEFT, padx=5)
        
        # BUTTON TO START THE PROCESS SIMULATION         
        self.start_button = ctk.CTkButton(self.control_frame, text="Start", command=self.start_simulation)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # BUTTON TO PAUSE THE SIMULATION 
        self.stop_button = ctk.CTkButton(self.control_frame, text="Stop", command=self.stop_simulation)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # BUTTON TO SIMULATE ZOMBIE STATE 
        self.kill_button = ctk.CTkButton(self.control_frame, text="Kill", command=self.kill_simulation)
        self.kill_button.pack(side=tk.LEFT, padx=5)

        # BUTTON TO CONTINUE SIMULATION 
        self.resume_button = ctk.CTkButton(self.control_frame, text="Resume", command=self.resume_simulation)
        self.resume_button.pack(side=tk.LEFT, padx=5)
        

        # FRAME THAT CONTAINS THE PROCESS AND SCROLLING 
        self.process_frame = ctk.CTkFrame(self.main_frame) 
        self.process_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        

        # CANVAS INSIDE OF process_frame TO DISPLAY THE PROCESS 
        self.process_canvas = tk.Canvas(self.process_frame, bg='#2a2d2e')  
        self.process_canvas.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.process_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # VERTICAL SCROLLBAR 
        self.scrollbar = ctk.CTkScrollbar(self.process_frame, command=self.process_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # LINK SCROLLBAR TO CANVAS 
        self.process_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # ADJUST SCROLL REGION 
        self.process_canvas.bind('<Configure>', lambda e: self.process_canvas.configure(scrollregion=self.process_canvas.bbox("all")))


        # INNER FRAME FOR PROCESS WIDGETS 
        self.inner_frame = ctk.CTkFrame(self.process_canvas)
        self.process_canvas.create_window((20, 20), window=self.inner_frame, anchor="nw")

        # SETTING PERIODIC PROCESS UI UPDATES 
        self.after(100, self.update_processes)

    # METHOD TO ADD NEW PROCESS TO THE EMULATOR WITH EXECUTION TIME 
    def add_process(self):
        try:
            execution_time = int(self.add_process_entry.get())
            if execution_time <= 0:
                raise ValueError("Execution time must be positive")
            process = self.os.add_process(execution_time)
            self.create_process_widgets(process)
            
            # HIDE THE ERROR LABEL 
            self.error_frame.grid_remove()
           
        except ValueError as e:
            if str(e).startswith("invalid literal for int() with base 10"):
                self.error_label.configure(text="Please enter a valid execution time.")
            else:
                self.error_label.configure(text=str(e))
            self.error_frame.grid()

    # METHOD TO CREATE WIDGETS TO SHOW THE PROCESSES
    def create_process_widgets(self, process):
        frame = ctk.CTkFrame(self.inner_frame)
        frame.pack(pady=5, padx=10, fill=tk.X)

        label = ctk.CTkLabel(frame, text=f"Process {process.pid}")
        label.pack(side=tk.LEFT, padx=5)

        progress_bar = ctk.CTkProgressBar(frame, width=200)
        progress_bar.set(0)
        progress_bar.pack(side=tk.LEFT, padx=5)

        # Setting process options 
        if process.state in [ProcessState.NEW, ProcessState.READY, ProcessState.RUNNING]:
            options = ["Blocked", "End"]
        elif process.state == ProcessState.BLOCKED:
            options = ["Unblocked", "End"]
        else:
            options = []

        # Dropdown menu & process options
        state_var = tk.StringVar(value=process.state.value)
        state_menu = ctk.CTkOptionMenu(frame, values=options, variable=state_var, command=lambda new_state, pid=process.pid: self.change_process_state(pid, new_state))
        state_menu.pack(side=tk.LEFT, padx=5)

        # Dictionary to store association of widget with specific process
        process.widgets = {"frame": frame, "progress_bar": progress_bar, "state_var": state_var, "state_menu": state_menu}

    # METHOD TO PERIODICALLY UPDATES OF UI STATES PROCESS
    def update_processes(self):
        for process in self.os.processes:
            if hasattr(process, 'widgets'):
                # Verify if progress widget exits
                if process.widgets["frame"].winfo_exists():
                    process.widgets["progress_bar"].set(process.progress / process.execution_time)
                    process.widgets["state_var"].set(process.state.value)
                    self.update_process_color(process)
                    process.widgets["state_menu"].configure(state="normal" if not self.os.killed else "disabled")
                else:
                    # If not, remove the reference in the dictionary
                    del process.widgets
        self.after(100, self.update_processes)

    # METHOD TO UPDATE DE COLOR OF THE PROCESS DEPENDING OF THE STATE 
    def update_process_color(self, process):
        colors = {
            ProcessState.NEW: "gray",
            ProcessState.READY: "#9a7d0a",
            ProcessState.RUNNING: "#044b05",
            ProcessState.BLOCKED: "#751901",
            ProcessState.TERMINATED: "#032268",
            ProcessState.ZOMBIE: "#7e4202"
        }
        process.widgets["frame"].configure(fg_color=colors[process.state])

    # METHOD TO STARTS THE PROCESS SIMULATION
    def start_simulation(self):
        self.os.start()
        self.update_button_states(killed=False)

    # METHOD TO PAUSE THE PROCESS SIMULATION
    def stop_simulation(self):
        self.os.stop()
        self.update_button_states(killed=False)

    # METHOD STARTS ZOMBIE SIMULATION
    def kill_simulation(self):
        self.os.kill()
        self.update_button_states(killed=True)

    # METHOD TO RESUMES THE PROCESS SIMULATION 
    def resume_simulation(self):
        self.os.resume()
        self.update_button_states(killed=False)

    # METHOD TO CHANGE PROCESS STATE DEPENDING OF USER  SELECTION 
    def change_process_state(self, pid, new_state):
        if new_state == "Unblocked":
            new_state = ProcessState.READY
        elif new_state == "Blocked":
            new_state = ProcessState.BLOCKED
        elif new_state == "End":
            new_state = ProcessState.TERMINATED

        self.os.change_process_state(int(pid), new_state)
        process = next((p for p in self.os.processes if p.pid == pid), None)

        if process:
            if process.state == ProcessState.TERMINATED:
                process.widgets["frame"].destroy()  
                self.os.processes.remove(process)   
            elif process.state == ProcessState.BLOCKED:
                process.widgets["state_menu"].configure(values=["Unblocked", "End"])
            elif process.state == ProcessState.READY:
                process.widgets["state_menu"].configure(values=["Blocked", "End"])

    # METHOD TO DISABLE BUTTONS ON ZOMBIE STATE 
    def update_button_states(self, killed):
        if killed:
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.kill_button.configure(state="disabled")
            self.resume_button.configure(state="disabled")
            self.add_process_button.configure(state="disabled")
        else:
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="normal")
            self.kill_button.configure(state="normal")
            self.resume_button.configure(state="normal")
            self.add_process_button.configure(state="normal")