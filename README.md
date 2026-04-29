# Benchmark Job Scheduling Algorithms

A comprehensive Python simulation that benchmarks three CPU scheduling algorithms across three distinct workload scenarios.

## Overview

This project implements and evaluates CPU scheduling algorithms fundamental to operating systems. The simulation models a single-CPU system where processes arrive at different times and require both CPU execution and I/O operations. 

**Algorithms Implemented:**
- **FCFS** (First Come, First Served) - Executes processes in arrival order, non-preemptive
- **SJF** (Shortest Job First) - Prioritizes processes with shorter CPU bursts
- **Priority** - Executes based on assigned priority levels

## How the Simulation Works

The simulator tracks processes through their lifecycle with the following components:

### Process Model
Each process has:
- **Arrival Time**: When it enters the system
- **CPU Burst**: Duration needed for CPU execution  
- **I/O Burst**: Duration of I/O operation after CPU work
- **Priority**: Importance level (for priority scheduling)
- **State**: new → ready → terminated

### Performance Metrics
Three key metrics are tracked for each process:
- **Wait Time**: Time spent waiting in the ready queue
- **Turnaround Time**: Total time from arrival to completion
- **Response Time**: Time from arrival to first CPU execution

### Scheduling Algorithms

**FCFS (First Come, First Served)**
- Simplest algorithm that maintains process arrival order
- Non-preemptive: once a process starts, it runs to completion
- Fair but potentially high average wait time

**SJF (Shortest Job First)**
- Executes process with shortest CPU burst first
- Minimizes average wait time and turnaround time
- Risk of starvation for longer processes

**Priority Scheduling**
- Executes process with highest priority (lowest priority number)
- Allows important tasks to be prioritized
- Without aging, can cause priority inversion and starvation


## Test Scenarios

### Scenario A: CPU-Heavy Workload

**Characteristics:**
- Long CPU bursts (3-50 time units)
- Minimal I/O waits (3-30 time units)
- Simulates batch processing, scientific computing, image rendering

**Use Case:** Systems where CPU is the bottleneck

**Results:**

| Algorithm | Avg Wait | Avg Turnaround | Avg Response |
|-----------|----------|----------------|--------------|
| FCFS      | 81.6     | 120.6          | 81.6         |
| SJF       | **69.6** | **108.6**      | **69.6**     |
| Priority  | 81.6     | 120.6          | 81.6         |

**Analysis:**
SJF outperforms FCFS by 12% in average wait time. By executing shorter jobs first (P5: 3 units, P4: 5 units, P2: 35 units, P1: 40 units, P3: 50 units), SJF prevents shorter processes from being blocked by longer ones. FCFS suffers because P1's 40-unit burst delays all subsequent processes. Priority scheduling behaves like FCFS here since processes have uniform priorities.

**Conclusion:** When workloads have varying CPU burst lengths, SJF is the clear winner for CPU-heavy scenarios.


### Scenario B: I/O-Heavy Workload

**Characteristics:**
- Short CPU bursts (3-50 time units)
- Long I/O waits (2-40 time units)
- Simulates web servers, database access, file I/O operations

**Use Case:** Systems where I/O is the bottleneck

**Results:**

| Algorithm | Avg Wait | Avg Turnaround | Avg Response |
|-----------|----------|----------------|--------------|
| FCFS      | 77.6     | 121.0          | 77.6         |
| SJF       | 77.6     | 121.0          | 77.6         |
| Priority  | 77.6     | 121.0          | 77.6         |

**Critical Finding:** All algorithms perform identically!

**Analysis:**
This is the most important finding of the project. Why do all algorithms converge?

1. **I/O Dominates:** Each process waits for a long I/O burst after CPU execution
2. **Sequential Model:** In this simulation, a process must complete CPU + I/O before the next process runs
3. **Total Time Is Similar:** Even though SJF would execute shorter jobs first, the I/O wait forces sequential behavior
4. **Scheduling Irrelevant:** The overhead of choosing which process runs next is negligible compared to I/O wait time

**Real-World Implication:** In real operating systems, I/O operations are asynchronous. When one process does I/O, others can use the CPU. This allows parallelism and makes scheduling more impactful. However, this simplified model doesn't capture that benefit.

**Conclusion:** Scheduling algorithm choice is irrelevant when I/O dominates. OS improvements to I/O handling (asynchronous I/O, buffering, multiple queues) would have more impact than algorithm selection.

### Scenario C: Balanced Workload with Priority

**Characteristics:**
- Mixed CPU/I/O (CPU: 3-25, I/O: 10-40)
- Varying priorities (1-4, lower = higher priority)
- Staggered arrivals (every 5 time units)
- Simulates real-world multitasking systems

**Use Case:** Mixed workload systems where both CPU and I/O matter

**Results:**

| Algorithm | Avg Wait | Avg Turnaround | Avg Response |
|-----------|----------|----------------|--------------|
| **FCFS**  | **59.0** | **94.6**       | **59.0**     |
| SJF       | 63.8     | 99.4           | 63.8         |
| Priority  | 63.2     | 98.8           | 63.2         |

**Surprising Finding:** FCFS wins!

**Analysis:**

FCFS outperforms optimized algorithms in this scenario:

1. **Staggered Arrivals Help FCFS:** Processes arrive every 5 time units (P1 at 0, P2 at 5, P3 at 10, P4 at 15, P5 at 20). FCFS maintains arrival order, naturally spreading load.

2. **SJF Creates Problems:** By executing P5 (3 CPU units) before P2 (25 CPU units), SJF causes priority inversion. P2 (priority=1, high) must wait while lower-priority work completes.

3. **Priority Fails Too:** Execution order becomes P1(pri 3) → P2(pri 1) → P5(pri 1) → P3(pri 2) → P4(pri 4). P4 (lowest priority) still waits 133 units, causing starvation risk. Real systems use aging to prevent this.

**Conclusion:** When process arrival is distributed and workloads are balanced, FCFS's simplicity and fairness prove superior to complex optimizations.

## Performance Summary

### Wait Time (Lower is Better)

| Scenario      | FCFS | SJF  | Priority |
|---------------|------|------|----------|
| CPU-Heavy     | 81.6 | 69.6*| 81.6     |
| I/O-Heavy     | 77.6*| 77.6*| 77.6*    |
| Balanced      | 59.0*| 63.8 | 63.2     |

### Turnaround Time (Lower is Better)

| Scenario      | FCFS  | SJF   | Priority |
|---------------|-------|-------|----------|
| CPU-Heavy     | 120.6 | 108.6*| 120.6    |
| I/O-Heavy     | 121.0*| 121.0*| 121.0*   |
| Balanced      | 94.6* | 99.4  | 98.8     |

*Best performer

## Key Findings and Conclusions

### Finding 1: No Universal Winner
Each algorithm excels in different contexts:
- **SJF:** Best for CPU-bound, variable-length workloads
- **FCFS:** Best for fair, predictable distributed arrivals
- **Priority:** Requires additional mechanisms (aging, preemption) to work well

### Finding 2: I/O Is the Dominant Factor
When I/O dominates the workload, scheduling becomes irrelevant. This suggests:
- Focus on asynchronous I/O handling in OSes
- Implement I/O buffering and caching
- Use multiple queues for different process types
- Consider memory utilization for performance gains

### Finding 3: Priority Inversion Is Real
Priority scheduling can actually harm performance without:
- Aging mechanisms to increase priority over time
- Preemption to interrupt lower-priority work
- Careful priority assignment

### Finding 4: SJF Carries Starvation Risk
Long-running processes can be indefinitely delayed by steady arrivals of short jobs. This is why real systems need:
- SJF variant with remaining time calculation (SRTF)
- Preemption to prevent indefinite delays
- Fairness guarantees

### Finding 5: Process Arrival Pattern Matters
- Clustered arrivals: Complex algorithms help more
- Distributed arrivals: FCFS simplicity is competitive
- Random arrivals: Varies case by case

## Real-World Algorithm Selection

### Use FCFS When:
- Process arrival times are relatively distributed
- Fairness and predictability are priorities
- CPU usage is moderate (not extremely heavy)
- System is simple, low-cost microcontroller

### Use SJF When:
- Process lengths vary significantly
- CPU workload is heavy and consistent
- You can estimate or predict job duration
- System is mostly compute-bound

### Use Priority When:
- Different processes have different importance
- Implementing with **aging** to prevent starvation
- Combined with **preemption** (not just selection)
- Real-time systems with mixed workloads
- Combined with other techniques (round-robin, multiple queues)

### Recommended for Production Systems:
Modern operating systems use **hybrid approaches:**
- Multi-level feedback queues (different priority levels, different time quanta)
- Dynamic priority adjustment (aging + boost for I/O completion)
- Preemption (interrupt lower-priority work when high-priority arrives)
- Separate I/O and CPU scheduling
- Adaptive algorithms that adjust based on system state


## Running the Simulation

### Requirements
- Python 3.6+
- No external dependencies

### Execution
```bash
python main.py
```

The program will:
1. Run all three algorithms on CPU-heavy scenario (Scenario A)
2. Run all three algorithms on I/O-heavy scenario (Scenario B)  
3. Run all three algorithms on balanced scenario with priority (Scenario C)
4. Display formatted output with individual process metrics and averages
5. Save results to RESULTS.txt

### Output Format

For each algorithm and scenario combination:
```
ALGORITHM - Scenario X
PID   Wait     Turnaround   Response
P1    0        45           0
P2    43       82           43
...
Averages: Wait=81.6  TAT=120.6  Response=81.6
```

## Project Files

- **main.py** - Main simulation runner and benchmarking script
- **simulation.py** - Core simulation engine with Process class and scheduling algorithms
- **RESULTS.txt** - Complete experimental results from all 9 scenarios
- **README.md** - Project documentation and analysis

## Algorithm Implementation Details

### FCFS Implementation
- Sorts queue by arrival time
- Non-preemptive: processes run to completion
- Time Complexity: O(n log n) per scheduling decision

### SJF Implementation
- Sorts queue by CPU burst length
- Non-preemptive: processes run to completion
- Time Complexity: O(n log n) per scheduling decision
- Note: Real SJF requires predicting burst length (via exponential averaging or user input)

### Priority Implementation
- Sorts queue by priority value (ascending)
- Non-preemptive: processes run to completion
- Time Complexity: O(n log n) per scheduling decision
- Note: Without aging, can cause indefinite starvation

## Simulation Assumptions

1. **Single CPU:** Only one processor available
2. **Non-preemptive:** Once started, process runs to completion (no interrupts)
3. **Sequential I/O:** I/O operations happen sequentially (not concurrent)
4. **No Memory Constraints:** All processes fit in memory
5. **Deterministic Bursts:** CPU and I/O times are known in advance
6. **Instant Context Switch:** No switching overhead modeled
7. **No Priority Aging:** Priority values don't change over time

## Potential Improvements

To make the simulation more realistic:

1. **Preemption:** Implement time-quantum based switching
2. **Asynchronous I/O:** Allow CPU usage while another process does I/O
3. **Priority Aging:** Increase priority for processes waiting too long
4. **Memory Model:** Track memory usage and implement page replacement
5. **Real Statistics:** Use actual process traces instead of synthetic data
6. **Multi-CPU:** Model multiple processors and load balancing
7. **Stochastic Bursts:** Use probability distributions for burst times
8. **Predictive Algorithms:** Implement machine learning for job length estimation


## Conclusion

This benchmarking study demonstrates that **CPU scheduling algorithm selection is highly workload-dependent.** There is no universally optimal algorithm. Instead, operating system designers must:

1. **Understand their workload:** Is it CPU-bound? I/O-bound? Mixed?
2. **Choose appropriately:** Match algorithm to workload characteristics
3. **Implement carefully:** Add aging, preemption, and fairness guarantees
4. **Measure continuously:** Monitor real system behavior and adjust
5. **Combine techniques:** Modern systems use hybrid approaches with multiple queues and dynamic adjustment

The findings align with decades of operating system research and justify why modern schedulers (Linux CFS, Windows Scheduler, macOS scheduler) are sophisticated, adaptive, and tuned to their specific use cases.
