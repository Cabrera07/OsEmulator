import random
import threading
import time
from process import Process, ProcessState

# TO EMULATE OS PROCESS MANAGEMENT
class OS:
    # CONSTRUCTOR 
    def __init__(self):
        self.processes = []
        self.running = False
        self.killed = False
        self.thread = None

    # METHOD TO ADD A NEW PROCESS 
    def add_process(self, execution_time):
        pid = len(self.processes) + 1
        process = Process(pid, execution_time)
        self.processes.append(process)
        return process

    # MAIN LOOP FOR PROCESS MANAGEMENT 
    def run(self):
        while self.running:
            if not self.killed:
                for process in self.processes:
                    # Handle zombie state 
                    if process.state == ProcessState.ZOMBIE:
                        process.state = process.pre_zombie_state or ProcessState.READY
                        process.pre_zombie_state = None
                    # Handle manually terminated process (end)
                    if process.manual_state == ProcessState.TERMINATED:
                        continue  
                    # Handle manually blocked process 
                    elif process.manual_state == ProcessState.BLOCKED:
                        process.state = ProcessState.BLOCKED
                    # Update process to ready 
                    elif process.manual_state is None or process.manual_state == ProcessState.READY:
                        self.update_process_state(process)
            else:
                # If OS is killed create zombie state 
                for process in self.processes:
                    if process.state != ProcessState.TERMINATED:
                        if process.state != ProcessState.ZOMBIE:
                            process.pre_zombie_state = process.state
                        process.state = ProcessState.ZOMBIE
            time.sleep(0.1)

    # METHOD TO UPDATE THE STATE OF A INDIVIDUAL PROCESS
    def update_process_state(self, process):
        if process.state == ProcessState.NEW:
            process.state = ProcessState.READY
        elif process.state == ProcessState.READY:
            if random.random() < 0.2:
                process.state = ProcessState.RUNNING
        elif process.state == ProcessState.RUNNING:
            process.progress += 1
            if process.progress >= process.execution_time:
                process.state = ProcessState.TERMINATED

    # METHOD TO STAR OS SIMULATION 
    def start(self):
        self.running = True
        self.killed = False
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    # METHOD TO PAUSE OS SIMULATION 
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        self.thread = None

    # METHOD TO EMULATE ZOMBIE STATE 
    def kill(self):
        self.killed = True

    # METHOD TO CONTINUE PROCESSES
    def resume(self):
        self.killed = False
        
    # METHOD TO MANUALLY CHANGE THE STATE OF A PROCESS
    def change_process_state(self, pid, new_state):
        for process in self.processes:
            if process.pid == pid:
                if new_state == ProcessState.TERMINATED: # "End"
                    process.state = ProcessState.TERMINATED
                    process.manual_state = ProcessState.TERMINATED
                elif new_state == ProcessState.BLOCKED:
                    process.state = ProcessState.BLOCKED
                    process.manual_state = ProcessState.BLOCKED
                elif new_state == ProcessState.READY:  # "Unblocked"
                    process.state = ProcessState.READY
                    process.manual_state = None  # Continiue regular process
                break

