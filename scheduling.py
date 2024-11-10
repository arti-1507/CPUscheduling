def fcfs(n, processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time

    st = [0] * n  
    ct = [0] * n  
    wt = [0] * n  
    tat = [0] * n  

    st[0] = processes[0][1]  
    ct[0] = st[0] + processes[0][2]  
    tat[0] = ct[0] - processes[0][1]  
    wt[0] = tat[0] - processes[0][2]  

    for i in range(1, n):
        st[i] = max(ct[i - 1], processes[i][1])
        ct[i] = st[i] + processes[i][2]
        tat[i] = ct[i] - processes[i][1]
        wt[i] = tat[i] - processes[i][2]

    display_results(n, processes, st, ct, wt, tat)

def sjf_preemptive(n, processes):
    remaining_time = [p[2] for p in processes]  
    st = [-1] * n  
    ct = [0] * n  
    wt = [0] * n  
    tat = [0] * n  
    completed = 0  
    current_time = 0  
    shortest = -1  
    check = False  

    processes.sort(key=lambda x: x[1])  

    while completed != n:
        for i in range(n):
            if processes[i][1] <= current_time and remaining_time[i] > 0:
                if shortest == -1 or remaining_time[i] < remaining_time[shortest]:
                    shortest = i
                    check = True

        if not check:
            current_time += 1
            continue

        if st[shortest] == -1:
            st[shortest] = current_time

        remaining_time[shortest] -= 1
        current_time += 1

        if remaining_time[shortest] == 0:
            completed += 1
            check = False
            ct[shortest] = current_time  
            tat[shortest] = ct[shortest] - processes[shortest][1]  
            wt[shortest] = tat[shortest] - processes[shortest][2]  

            if wt[shortest] < 0:
                wt[shortest] = 0

        shortest = -1  

    display_results(n, processes, st, ct, wt, tat)

def priority_non_preemptive(n, processes):
    processes.sort(key=lambda x: (x[1], x[3]))  # Sort by arrival time, then by priority

    st = [0] * n  # Start times
    ct = [0] * n  # Completion times
    wt = [0] * n  # Waiting times
    tat = [0] * n  # Turnaround times
    completed = 0  # Count of completed processes
    current_time = 0  # Current time in the scheduling timeline
    is_completed = [False] * n  # Track which processes are completed

    while completed != n:
        idx = -1
        highest_priority = float('inf')
        
        # Select the process with the highest priority that has arrived
        for i in range(n):
            if processes[i][1] <= current_time and not is_completed[i]:
                if processes[i][3] < highest_priority:
                    highest_priority = processes[i][3]
                    idx = i

        # If no process is ready, increment time
        if idx == -1:
            current_time += 1
        else:
            st[idx] = current_time
            ct[idx] = st[idx] + processes[idx][2]
            tat[idx] = ct[idx] - processes[idx][1]
            wt[idx] = tat[idx] - processes[idx][2]

            is_completed[idx] = True
            completed += 1
            current_time = ct[idx]

    display_results(n, processes, st, ct, wt, tat)

def round_robin(n, processes, time_quantum):
    remaining_time = [p[2] for p in processes]  
    wt = [0] * n  
    tat = [0] * n  
    st = [-1] * n  
    ct = [0] * n  
    ready_queue = []  
    current_time = 0  
    completed = 0  

    processes.sort(key=lambda x: x[1])  

    for i in range(n):
        if processes[i][1] == 0:
            ready_queue.append(i)

    while completed != n:
        if not ready_queue:
            current_time = processes[completed][1]
            for i in range(n):
                if processes[i][1] == current_time and i not in ready_queue:
                    ready_queue.append(i)

        current_process = ready_queue.pop(0)

        if st[current_process] == -1:
            st[current_process] = current_time

        if remaining_time[current_process] > time_quantum:
            current_time += time_quantum
            remaining_time[current_process] -= time_quantum
        else:
            current_time += remaining_time[current_process]
            ct[current_process] = current_time  
            tat[current_process] = ct[current_process] - processes[current_process][1]  
            wt[current_process] = tat[current_process] - processes[current_process][2]  
            remaining_time[current_process] = 0
            completed += 1

        for i in range(n):
            if processes[i][1] <= current_time and remaining_time[i] > 0 and i not in ready_queue:
                ready_queue.append(i)

        if remaining_time[current_process] > 0:
            ready_queue.append(current_process)

    display_results(n, processes, st, ct, wt, tat)

def display_results(n, processes, st, ct, wt, tat):
    print("\nProcess\tArrival Time\tBurst Time\tStart Time\tCompletion Time\tWaiting Time\tTurnaround Time")
    for i in range(n):
        print(f"P{processes[i][0]}\t\t{processes[i][1]}\t\t{processes[i][2]}\t\t{st[i]}\t\t{ct[i]}\t\t{wt[i]}\t\t{tat[i]}")

    avg_waiting_time = sum(wt) / n
    avg_turnaround_time = sum(tat) / n

    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")

def main():
    while True:
        print("\nCPU Scheduling Algorithms")
        print("1. First-Come, First-Served (FCFS)")
        print("2. Shortest Job First (SJF) - Preemptive")
        print("3. Priority Scheduling - Preemptive")
        print("4. Round Robin")
        print("5. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 5:
            break

        n = int(input("Enter the number of processes: "))
        processes = []
        for i in range(n):
            at = int(input(f"Enter arrival time for process {i+1}: "))
            bt = int(input(f"Enter burst time for process {i+1}: "))
            if choice == 3:  # Priority Scheduling
                priority = int(input(f"Enter priority for process {i+1} (lower number = higher priority): "))
                processes.append([i+1, at, bt, priority])
            else:
                processes.append([i+1, at, bt])

        if choice == 1:
            fcfs(n, processes)
        elif choice == 2:
            sjf_preemptive(n, processes)
        elif choice == 3:
            priority_preemptive(n, processes)
        elif choice == 4:
            time_quantum = int(input("Enter the time quantum: "))
            round_robin(n, processes, time_quantum)

if __name__ == "__main__":
    main()