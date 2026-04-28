class Process:
    """
    Represents a single process in the scheduling simulation.
    
    Attributes:
        pid (int): Process identifier
        arrival_time (int): Time when process arrives in the system
        cpu_burst (int): Duration of CPU execution needed
        io_burst (int): Duration of I/O operation needed after CPU execution
        priority (int): Priority level (lower value = higher priority)
        state (str): Current process state (new, ready, running, terminated)
        waiting_time (int): Total time spent waiting in the queue
        turnaround_time (int): Total time from arrival to completion
        response_time (int): Time from arrival to first CPU execution
        finish_time (int): Clock time when process completes
    """
    def __init__(self, pid, arrival_time, cpu_burst, io_burst, priority=1):
        self.pid = pid
        self.arrival_time = arrival_time
        self.cpu_burst = cpu_burst
        self.io_burst = io_burst
        self.priority = priority
        self.state = "new"
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = None
        self.finish_time = None

def run_simulation(processes, algorithm):
    """
    Execute the CPU scheduling simulation with the specified algorithm.
    
    The simulation models a single-CPU system where processes arrive at different times
    and require CPU and I/O resources. The simulator runs a clock and manages a ready queue.
    
    Algorithm Details:
    - FCFS (First Come, First Served): Executes processes in arrival order
    - SJF (Shortest Job First): Executes process with shortest CPU burst first
    - Priority: Executes process with lowest priority number (highest priority) first
    
    Args:
        processes (list): List of Process objects to schedule
        algorithm (str): Scheduling algorithm - one of "fcfs", "sjf", or "priority"
    
    Returns:
        list: List of completed Process objects with calculated metrics
    
    Notes:
        - Processes only move to "ready" state once they arrive (arrival_time <= clock)
        - Response time is measured from arrival to first CPU execution
        - Turnaround time includes both execution and I/O wait time
        - When queue is empty, clock jumps to next process arrival time
    """
    clock = 0
    queue = []
    finished = []

    while len(finished) < len(processes):

        for p in processes:
            if p.arrival_time <= clock and p.state == "new":
                p.state = "ready"
                queue.append(p)

        if algorithm == "fcfs":
            queue.sort(key=lambda p: p.arrival_time)
        elif algorithm == "sjf":
            queue.sort(key=lambda p: p.cpu_burst)
        elif algorithm == "priority":
            queue.sort(key=lambda p: p.priority)

        if queue:
            p = queue.pop(0)
            if p.response_time is None:
                p.response_time = clock - p.arrival_time
            clock += p.cpu_burst
            clock += p.io_burst
            p.finish_time = clock
            p.turnaround_time = p.finish_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.cpu_burst - p.io_burst
            p.state = "terminated"
            finished.append(p)
        else:
            # Jump to the next arrival time
            next_arrivals = [p.arrival_time for p in processes if p.state == "new"]
            if next_arrivals:
                clock = min(next_arrivals)
            else:
                break

    return finished

def print_results(finished, label):
    """
    Print simulation results in a formatted table with performance metrics.
    
    Displays individual process metrics and average statistics for the simulation.
    
    Metrics Explained:
    - Wait: Total time process waited in the queue before execution
    - Turnaround: Total time from arrival to completion (includes CPU, I/O, and wait time)
    - Response: Time from arrival to first CPU execution (response time to user)
    
    Args:
        finished (list): List of completed Process objects
        label (str): Label describing the algorithm and scenario (e.g., "FCFS - Scenario A")
    """
    print(f"\n{label}")
    print(f"{'PID':<5} {'Wait':<8} {'Turnaround':<12} {'Response'}")
    for p in finished:
        print(f"P{p.pid:<4} {p.waiting_time:<8} {p.turnaround_time:<12} {p.response_time}")
    n = len(finished)
    avg_wt  = sum(p.waiting_time for p in finished) / n
    avg_tat = sum(p.turnaround_time for p in finished) / n
    avg_rt  = sum(p.response_time for p in finished) / n
    print(f"Averages: Wait={avg_wt:.1f}  TAT={avg_tat:.1f}  Response={avg_rt:.1f}")