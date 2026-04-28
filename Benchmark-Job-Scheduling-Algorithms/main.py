"""
Job Scheduling Algorithm Benchmark - Main Runner
==================================================

Simulates three CPU scheduling algorithms (FCFS, SJF, Priority) across three distinct 
workload scenarios (CPU-heavy, I/O-heavy, balanced with priority).

Results are displayed to console and saved to RESULTS.txt.
See README.md for detailed analysis and findings.
"""

import sys
from io import StringIO
from simulation import Process, run_simulation, print_results

# Scenario A: CPU-Heavy Workload
# Long CPU bursts, minimal I/O - tests CPU-bound workload handling
scenario_a = [
    Process(1, 0,  cpu_burst=40, io_burst=5),
    Process(2, 2,  cpu_burst=35, io_burst=4),
    Process(3, 4,  cpu_burst=50, io_burst=3),
    Process(4, 6,  cpu_burst=5,  io_burst=20),
    Process(5, 8,  cpu_burst=3,  io_burst=30),
]

# Scenario B: I/O-Heavy Workload
# Short CPU bursts, long I/O waits - tests I/O-bound workload handling
scenario_b = [
    Process(1, 0,  cpu_burst=4,  io_burst=40),
    Process(2, 2,  cpu_burst=3,  io_burst=35),
    Process(3, 4,  cpu_burst=5,  io_burst=30),
    Process(4, 6,  cpu_burst=45, io_burst=3),
    Process(5, 8,  cpu_burst=50, io_burst=2),
]

# Scenario C: Balanced Workload with Priority
# Mixed CPU/I/O with varying priorities - tests balanced/real-world workload
scenario_c = [
    Process(1, 0,  cpu_burst=20, io_burst=15, priority=3),
    Process(2, 5,  cpu_burst=25, io_burst=10, priority=1),
    Process(3, 10, cpu_burst=5,  io_burst=30, priority=2),
    Process(4, 15, cpu_burst=18, io_burst=12, priority=4),
    Process(5, 20, cpu_burst=3,  io_burst=40, priority=1),
]

def reset_processes(processes):
    """Reset process states for a clean simulation run."""
    for p in processes:
        p.state = "new"
        p.waiting_time = 0
        p.turnaround_time = 0
        p.response_time = None
        p.finish_time = None

# Run simulations and collect output
output_lines = []

output_lines.append("\n" + "="*70)
output_lines.append("SCENARIO A: CPU-HEAVY WORKLOAD")
output_lines.append("="*70)

for algo in ["fcfs", "sjf", "priority"]:
    reset_processes(scenario_a)
    result = run_simulation(scenario_a, algo)
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    print_results(result, f"{algo.upper()} - Scenario A")
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    output_lines.append(output)
    print(output, end='')

output_lines.append("\n" + "="*70)
output_lines.append("SCENARIO B: I/O-HEAVY WORKLOAD")
output_lines.append("="*70)

for algo in ["fcfs", "sjf", "priority"]:
    reset_processes(scenario_b)
    result = run_simulation(scenario_b, algo)
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    print_results(result, f"{algo.upper()} - Scenario B")
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    output_lines.append(output)
    print(output, end='')

output_lines.append("\n" + "="*70)
output_lines.append("SCENARIO C: BALANCED WORKLOAD WITH PRIORITY")
output_lines.append("="*70)

for algo in ["fcfs", "sjf", "priority"]:
    reset_processes(scenario_c)
    result = run_simulation(scenario_c, algo)
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    print_results(result, f"{algo.upper()} - Scenario C")
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    output_lines.append(output)
    print(output, end='')

# Save to RESULTS.txt
with open("RESULTS.txt", "w") as f:
    f.write("\n".join(output_lines))

print("\n" + "="*70)
print("Results saved to RESULTS.txt")
print("="*70)