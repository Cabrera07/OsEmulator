import random
import threading
import time
from process import Process, ProcessState

# CLASS TO EMULATE OS PROCESS MANAGEMENT
class OS:
    def __init__(self):
        """
        Initialize the OS simulator with an empty process list and management flags.
        """
        self.processes = []  # List of all processes in the OS
        self.running = False  # Flag to indicate if the OS is running
        self.killed = False  # Flag for killing the OS (zombie mode)
        self.thread = None  # Thread for running the OS in the background

    # METHOD TO ADD A NEW PROCESS WITH A SPECIFIED PRIORITY
    def add_process(self, priority):
        """
        Add a new process to the OS with a specified priority.
        
        :param priority: Priority of the process ('High', 'Medium High', 'Medium Low', 'Low')
        :return: The newly created process
        """
        pid = len(self.processes) + 1  # Assign a unique PID to the new process
        process = Process(pid, priority)
        self.processes.append(process)
        return process

    # MAIN LOOP FOR PROCESS MANAGEMENT
    def run(self):
        """
        Main loop to manage and execute processes in the OS.
        This loop checks the state of each process and updates it accordingly.
        """
        while self.running:
            if not self.killed:
                for process in self.processes:
                    if process.state == ProcessState.ZOMBIE:
                        process.state = process.pre_zombie_state or ProcessState.READY
                        process.pre_zombie_state = None
                    
                    if process.manual_state == ProcessState.TERMINATED:
                        continue  # Skip terminated processes

                    elif process.manual_state == ProcessState.BLOCKED:
                        process.state = ProcessState.BLOCKED

                    elif process.manual_state is None or process.manual_state == ProcessState.READY:
                        self.update_process_state(process)
            else:
                # If OS is killed, all processes become zombies
                for process in self.processes:
                    if process.state != ProcessState.TERMINATED:
                        if process.state != ProcessState.ZOMBIE:
                            process.pre_zombie_state = process.state
                        process.state = ProcessState.ZOMBIE

            time.sleep(0.1)

    def update_process_state(self, process):
        """
        Update the state of an individual process based on its progress and execution time.
        """
        running_processes = [p for p in self.processes if p.state == ProcessState.RUNNING]

        if process.state == ProcessState.NEW:
            process.state = ProcessState.READY  # Transition to READY state

        elif process.state == ProcessState.READY:
            if len(running_processes) < 10:
                if random.random() < 0.2:
                    process.state = ProcessState.RUNNING
            else:
                # Find the process with the lowest priority among running processes
                lowest_priority_process = min(running_processes, key=lambda p: self.get_priority_value(p.priority))
                
                # If the current process has higher priority, swap them
                if self.get_priority_value(process.priority) > self.get_priority_value(lowest_priority_process.priority):
                    lowest_priority_process.state = ProcessState.BLOCKED_SUSPENDED
                    process.state = ProcessState.RUNNING
                else:
                    process.state = ProcessState.BLOCKED_SUSPENDED

        elif process.state == ProcessState.RUNNING:
            process.progress += 1
            if process.progress >= process.execution_time:
                process.state = ProcessState.TERMINATED
                self.handle_process_completion()

        elif process.state == ProcessState.BLOCKED_SUSPENDED:
            # Move to READY_SUSPENDED if there's space
            if len(running_processes) < 10:
                self.schedule_transition(process, ProcessState.READY_SUSPENDED, 5)

        elif process.state == ProcessState.READY_SUSPENDED:
            # Move to READY if the process is in READY_SUSPENDED 
            self.schedule_transition(process, ProcessState.READY, 10)

        elif process.state == ProcessState.READY:
            # Once READY, move to RUNNING 
            self.schedule_transition(process, ProcessState.RUNNING, 5)


    def schedule_transition(self, process, target_state, delay):
        """
        Schedule a process to transition to another state after a delay.
        """
        if not hasattr(process, "scheduled") or process.scheduled is False:
            process.scheduled = True  # Prevent multiple transitions being scheduled
            threading.Timer(delay, lambda: self.set_process_state(process, target_state)).start()

    def get_priority_value(self, priority):
        """
        Convert priority string to a numeric value for comparison.
        """
        priority_values = {
            'High': 4,
            'Medium High': 3,
            'Medium Low': 2,
            'Low': 1
        }
        return priority_values.get(priority, 0)
    
    def set_process_state(self, process, state):
        """
        Set the state of a process and reset its scheduled flag.
        """
        process.state = state
        process.scheduled = False

    def handle_process_completion(self):
        """
        Called when a process completes (TERMINATED). Move a suspended process to READY_SUSPENDED if available.
        """
        for process in self.processes:
            if process.state == ProcessState.BLOCKED_SUSPENDED:
                self.schedule_transition(process, ProcessState.READY_SUSPENDED, 3)
                break

    def remove_terminated_process(self, process):
        """
        Remove a process from the OS once it has been in the TERMINATED state for 3 seconds.
        """
        if process.state == ProcessState.TERMINATED:
            self.processes.remove(process)

    def start(self):
        """
        Start the OS simulation in a background thread.
        """
        self.running = True
        self.killed = False
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self):
        """
        Stop the OS simulation and wait for the thread to terminate.
        """
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        self.thread = None

    def kill(self):
        """
        Simulate killing the OS, placing all non-terminated processes into ZOMBIE state.
        """
        self.killed = True

    def resume(self):
        """
        Resume the OS simulation after being in ZOMBIE state.
        """
        self.killed = False

    def change_process_state(self, pid, new_state):
        """
        Manually change the state of a process based on user input.
        """
        for process in self.processes:
            if process.pid == pid:
                if new_state == ProcessState.TERMINATED:
                    process.state = ProcessState.TERMINATED
                    process.manual_state = ProcessState.TERMINATED
                elif new_state == ProcessState.BLOCKED:
                    process.state = ProcessState.BLOCKED
                    process.manual_state = ProcessState.BLOCKED
                elif new_state == ProcessState.READY:
                    process.state = ProcessState.READY
                    process.manual_state = ProcessState.READY
                    # Start a timer to change the state after 1 second
                    threading.Timer(1.0, self.release_ready_state, args=[process]).start()
                break
        
            
    def release_ready_state(self, process):
        """
        Release the process from the READY state after 1 second.
        """
        if process.state == ProcessState.READY and process.manual_state == ProcessState.READY:
            process.manual_state = None  # Continue regular process
            print(f"Process {process.pid} released from READY state")
