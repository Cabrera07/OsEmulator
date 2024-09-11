# 🎛️ OS Process Management Emulator  <!-- omit from toc -->

![alt text](228_3x_shots_so.png)

A Python-based operating system process management emulator designed to simulate core OS functionalities such as process creation, suspension, termination, and state transitions. The project features a graphical user interface (GUI) to monitor and manage processes dynamically.

## ✨ Features

- ⚙️ **Process Creation**: Add multiple processes with different execution times and priorities.
- 🛑 **Process Suspension and Resumption**: Manage CPU cores, where processes can be suspended if the cores are fully occupied.
- 🖥️ **Graphical User Interface (GUI)**: A user-friendly interface to visualize and manage the processes in real-time.
- 🔄 **Process States**: Processes transition through various states (Ready, Running, Blocked, Blocked Suspended, Ready Suspended, Terminated) based on system resources and user actions.
- 🚫 **Process Termination**: Terminate processes manually or upon completion.
- 🧟 **System Freeze ("Kill")**: Simulate a system freeze where all processes are halted and the GUI becomes unresponsive, emulating the "Zombie" state.

## 📚 Table of Contents <!-- omit from toc -->

- [✨ Features](#-features)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📂 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)

## 📦 Installation

Follow these steps to set up the project on your local machine.

### Prerequisites <!-- omit from toc -->

- **Python 3.9.7** installed on your system (developed and tested with Python 3.9.7).
- Virtual environment (optional but recommended) to manage dependencies.

### Steps <!-- omit from toc -->

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/Cabrera07/OsEmulator.git
    cd OsEmulator
    ```

2. Set up a virtual environment (recommended):

    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:

   - On macOS/Linux:
  
        ```bash
        source venv/bin/activate
        ```

   - On Windows:

        ```bash
        venv\Scripts\activate
        ```

4. Install the project dependencies listed in the requirements.txt file:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the program:

    ```bash
    python main.py
    ```

## 🚀 Usage

Once the emulator is running, use the GUI to perform the following actions:

- ➕ Add Processes: Input details for process priority and CPU Cores, then add processes to the system.
- ▶️ Start: Begin executing processes. The number of simultaneous processes is based on the CPU cores selected.
- ⏸️ Stop: Pause all running processes.
- 🔄 Suspend: Processes exceeding the available cores will be suspended until resources are freed.
- 🗑️ Terminate: Manually terminate any process that is running or suspended.
- ☠️ Kill (Zombie State): Simulate a system freeze where all processes stop and no further actions can be performed until restarted.

## 📂 Project Structure

```bash
OSemulator/
├── images/
│   └── mockup.png            # The mockup image.
├── gui.py                    # Handles the graphical user interface.
├── main.py                   # Entry point of the emulator.
├── os_simulator.py           # Core logic for simulating OS functionalities.
├── process.py                # Defines the process structure and states.
├── .gitignore                # Specifies which files Git should ignore.
├── README.md                 # Project documentation.
├── requirements.txt          # List of dependencies (if any).
└── venv/                     # Virtual environment directory.
```

### 🔑 Key Files  <!-- omit from toc -->

- `gui.py`: Contains the code for managing the graphical user interface.
- `main.py`: The main entry point that runs the entire emulator.
- `os_simulator.py`: Contains the logic for managing CPU cores, process scheduling, and state transitions.
- `process.py`: Defines the structure and attributes of each process, as well as the transitions between different process - states.

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git switch -c feature-branch`).
3. Make your changes and commit them (`git commit -m 'Added new feature'`).
4. Push to your branch (`git push origin feature-branch`).
5. Open a pull request to the main branch.
