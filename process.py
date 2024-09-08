from enum import Enum

# DEFINE THE POSSIBLE STATES OF A PROCESS
class ProcessState(Enum):
    NEW = "New" # Process has been created 
    READY = "Ready" # Process ready to be executed 
    RUNNING = "Running" # Process in execution 
    BLOCKED = "Blocked" # The execution of the process stop 
    TERMINATED = "Terminated" # Process completed 
    ZOMBIE = "Zombie" # State to represent zombie mode 

# TO REPRESENT THE OS PROCESS 
class Process:
    def __init__(self, pid, execution_time):
        self.pid = pid
        self.state = ProcessState.NEW
        self.execution_time = execution_time
        self.progress = 0
        self.manual_state = None
        self.pre_zombie_state = None