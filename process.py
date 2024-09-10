from enum import Enum

# DEFINE THE POSSIBLE STATES OF A PROCESS
class ProcessState(Enum):
    NEW = "New"  # Process has been created
    READY = "Ready"  # Process is ready to be executed
    RUNNING = "Running"  # Process is in execution
    BLOCKED = "Blocked"  # The execution of the process is stopped
    TERMINATED = "Terminated"  # Process has completed
    ZOMBIE = "Zombie"  # State to represent zombie mode
    BLOCKED_SUSPENDED = "Blocked Suspended"  
    READY_SUSPENDED = "Ready Suspended" 

# CLASS TO REPRESENT THE OS PROCESS
class Process:
    # MAPPING PRIORITY LEVELS TO EXECUTION TIMES (LONGER EXECUTION TIMES)
    PRIORITY_EXECUTION_TIMES = {
        'High': 100,          # High priority gets the shortest execution time
        'Medium High': 200,   # Medium High priority gets more time
        'Medium Low': 300,    # Medium Low priority gets even more time
        'Low': 400,           # Low priority gets the longest execution time
    }

    def __init__(self, pid, priority):
        """
        Initialize a new process with a given priority.
        
        :param pid: Process ID
        :param priority: Priority level ('High', 'Medium High', 'Medium Low', 'Low')
        """
        self.pid = pid
        self.state = ProcessState.NEW  # Start in the NEW state
        self.priority = priority  # Priority of the process
        # Assign execution time based on the priority level
        self.execution_time = Process.PRIORITY_EXECUTION_TIMES[priority]
        self.progress = 0  # Progress starts at 0
        self.manual_state = None  # No manual state change initially
        self.pre_zombie_state = None  # To track the state before entering Zombie mode