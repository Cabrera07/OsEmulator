import customtkinter as ctk
import tkinter as tk
from os_simulator import OS
from process import ProcessState

class UI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set appearance mode and color theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        # Title and initial window size
        self.title("OS Process Emulator")
        self.geometry("1000x800")

        # Instance of the OS simulator
        self.os = OS()

        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)


        # Error frame and label
        self.error_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.error_frame.grid(row=0, column=0, pady=(5, 0), sticky="ew")
        self.error_frame.grid_remove()

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


        # Control frame for input and buttons
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        
        # Core selection menu
        self.cores_var = tk.StringVar(value="Select CPU Cores")
        self.cores_menu = ctk.CTkOptionMenu(self.control_frame, values=["1", "2", "4", "8"], variable=self.cores_var, command=self.update_cores)
        self.cores_menu.pack(side=tk.LEFT, padx=5)

        # Priority selection menu
        self.priority_var = tk.StringVar(value="Select Process Priority") 
        self.priority_menu = ctk.CTkOptionMenu(self.control_frame, values=["High", "Medium High", "Medium Low", "Low"], variable=self.priority_var)
        self.priority_menu.pack(side=tk.LEFT, padx=5)

        # Add process button
        self.add_process_button = ctk.CTkButton(self.control_frame, text="Add Process", command=self.add_process)
        self.add_process_button.pack(side=tk.LEFT, padx=5)

        # Start button
        self.start_button = ctk.CTkButton(self.control_frame, text="Start", command=self.start_simulation)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Stop button
        self.stop_button = ctk.CTkButton(self.control_frame, text="Stop", command=self.stop_simulation)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Kill (zombie mode) button
        self.kill_button = ctk.CTkButton(self.control_frame, text="Kill", command=self.kill_simulation)
        self.kill_button.pack(side=tk.LEFT, padx=5)


        # Process frame with scrolling
        self.process_frame = ctk.CTkFrame(self.main_frame)
        self.process_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        self.process_canvas = tk.Canvas(self.process_frame, bg='#2a2d2e')
        self.process_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.process_frame, command=self.process_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.process_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.process_canvas.bind('<Configure>', lambda e: self.process_canvas.configure(scrollregion=self.process_canvas.bbox("all")))

        self.inner_frame = ctk.CTkFrame(self.process_canvas)
        self.process_canvas.create_window((20, 20), window=self.inner_frame, anchor="nw")

        # Periodic updates to process display
        self.after(100, self.update_processes)


    def add_process(self):
        """
        Add a new process with the selected priority.
        """
        priority = self.priority_var.get()  # Get the selected priority
        cores = self.cores_var.get()  # Get the selected number of cores

        # Check if the user has selected a valid option for both menus
        if priority == "Select Process Priority" or cores == "Select CPU Cores":
            self.error_label.configure(text="Please select a valid option for cores and priority")
            self.error_frame.grid()
            return

        # If valid options are selected, proceed with adding the process
        try:
            process = self.os.add_process(priority)  # Add a new process to the OS
            self.create_process_widgets(process)  # Create the UI widgets for this process
            self.error_frame.grid_remove()  # Hide the error message if it was visible
        except ValueError as e:
            self.error_label.configure(text=str(e))
            self.error_frame.grid()


    def create_process_widgets(self, process):
        """
        Create the UI widgets for each process (progress bar, state, etc.).
        """
        frame = ctk.CTkFrame(self.inner_frame)
        frame.pack(pady=5, padx=10, fill=tk.X)

        # Label for the process ID and priority
        label = ctk.CTkLabel(frame, text=f"Process {process.pid} (Priority: {process.priority})", width=180, anchor="w")
        label.pack(side=tk.LEFT, padx=(5, 10))

        # Progress bar for the process execution
        progress_bar = ctk.CTkProgressBar(frame, width=200)
        progress_bar.set(0)
        progress_bar.pack(side=tk.LEFT, padx=(5, 10))  

        # Dropdown menu for changing the process state based on current state
        if process.state in [ProcessState.NEW, ProcessState.READY, ProcessState.RUNNING]:
            options = ["Blocked", "End"]
        elif process.state == ProcessState.BLOCKED:
            options = ["Unblocked", "End"]
        elif process.state == ProcessState.BLOCKED_SUSPENDED:
            options = ["Unblocked", "End"]
        elif process.state == ProcessState.READY_SUSPENDED:
            options = ["Blocked", "End"]
        else:
            options = []

        state_var = tk.StringVar(value=process.state.value) # Store the current state of the process
        state_menu = ctk.CTkOptionMenu(frame, values=options, variable=state_var, command=lambda new_state, pid=process.pid: self.change_process_state(pid, new_state), width=100)
        state_menu.pack(side=tk.LEFT, padx=(5, 10), pady=5)  

        # Store UI widgets in the process object for future updates
        process.widgets = {"frame": frame, "progress_bar": progress_bar, "state_var": state_var, "state_menu": state_menu}


    def update_processes(self):
        """
        Periodically update the UI to reflect the current state of each process.
        """
        for process in self.os.processes:
            if hasattr(process, 'widgets'): 
                # Update progress and state in the UI
                if process.widgets["frame"].winfo_exists(): 
                    process.widgets["progress_bar"].set(process.progress / process.execution_time) 
                    process.widgets["state_var"].set(process.state.value)
                    self.update_process_color(process)
                    process.widgets["state_menu"].configure(state="normal" if not self.os.killed else "disabled")

                    # If the process is terminated, remove its widget after 3 seconds
                    if process.state == ProcessState.TERMINATED:
                        if not hasattr(process, "scheduled_for_removal"):
                            process.scheduled_for_removal = True  
                            self.after(3000, lambda p=process: self.remove_process_widget(p))
                else:
                    del process.widgets
        self.after(100, self.update_processes)


    def remove_process_widget(self, process):
        """
        Remove the widget for a process after it's been terminated.
        """
        if hasattr(process, 'widgets') and process.widgets and process.widgets["frame"].winfo_exists():
            process.widgets["frame"].destroy()  # Destroy the widget frame
            del process.widgets  # Remove the reference to the widgets


    def update_process_color(self, process):
        """
        Update the color of a process widget based on its current state.
        """
        colors = {
            ProcessState.NEW: "gray",
            ProcessState.READY: "#9a7d0a",
            ProcessState.RUNNING: "#044b05",
            ProcessState.BLOCKED: "#751901",
            ProcessState.TERMINATED: "#032268",
            ProcessState.ZOMBIE: "#7e4202",
            ProcessState.BLOCKED_SUSPENDED: "#310451",  
            ProcessState.READY_SUSPENDED: "#5f4a05",    
        }
        process.widgets["frame"].configure(fg_color=colors[process.state])


    def start_simulation(self):
        """
        Start or resume the OS process simulation.
        """
        if self.os.killed:  
            self.os.resume()
        else:  
            self.os.start()
        self.update_button_states(killed=False)


    def stop_simulation(self):
        """
        Stop the OS process simulation.
        """
        self.os.stop()
        self.update_button_states(killed=False)


    def kill_simulation(self):
        """
        Simulate killing the OS (zombie mode).
        """
        self.os.kill()
        self.update_button_states(killed=True)


    def change_process_state(self, pid, new_state):
        """
        Change the state of a process based on the user's selection.
        """
        if new_state == "Unblocked":
            new_state = ProcessState.READY
        elif new_state == "Blocked":
            new_state = ProcessState.BLOCKED
        elif new_state == "End":
            new_state = ProcessState.TERMINATED
        elif new_state == "Suspended":
            new_state = ProcessState.BLOCKED_SUSPENDED

        # Change the process state in the OS simulator
        self.os.change_process_state(int(pid), new_state)
        
        # Find the process in the OS process list
        process = next((p for p in self.os.processes if p.pid == pid), None)

        if process:
            # Handle TERMINATED state and remove widget after 3 seconds
            if process.state == ProcessState.TERMINATED:
                if hasattr(process, 'widgets') and process.widgets and process.widgets["frame"].winfo_exists():
                    self.after(3000, lambda: self.remove_process_widget(process))
            
            # Update dropdown menu based on the new state
            elif process.state == ProcessState.BLOCKED:
                process.widgets["state_menu"].configure(values=["Unblocked", "End"])
            elif process.state == ProcessState.READY:
                process.widgets["state_menu"].configure(values=["Blocked", "End"])
            elif process.state == ProcessState.BLOCKED_SUSPENDED:
                process.widgets["state_menu"].configure(values=["Unblocked", "End"])


    def update_button_states(self, killed):
        """
        Update the button states when the OS is killed or resumed.
        """
        if killed:
            self.cores_menu.configure(state="disabled")
            self.priority_menu.configure(state="disabled")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.kill_button.configure(state="disabled")
            self.add_process_button.configure(state="disabled")
        else:
            self.cores_menu.configure(state="normal")
            self.priority_menu.configure(state="normal")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="normal")
            self.kill_button.configure(state="normal")
            self.add_process_button.configure(state="normal")
    
    
    def update_cores(self, num_cores):
        """Update the number of cores in the OS simulator."""
        self.os.set_num_cores(int(num_cores))
        
        