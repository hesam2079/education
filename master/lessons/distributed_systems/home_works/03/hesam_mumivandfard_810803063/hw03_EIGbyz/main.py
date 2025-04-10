
"""
in this function we do these things:
1. collect all messages from all processes
2. send messages to processes
3. update the tree of all processes
    - if any message doesn't receive or is garbage then the process add null value to that node
    - the process tree should be full only with null values
4. after f+1 round start making decisions
5. print the decision of all nodes in all trees of all processes

"""
from class_key_server import PublicKeyServer
from class_process import Process




def generate_process(total, faulty):
    processes = []
    for i in range(total-faulty):
        process = Process(process_id=i, initial_decision=1, number_of_processes=total, key_server)
        processes.append(process)
    for i in range(total-faulty, total):
        process = Process(process_id=i, initial_decision=1, number_of_processes=total, am_i_faulty=True, key_server)
        processes.append(process)
    return processes

def simulation_round1(processes):
    messages = []
    for process in processes:
        messages.append(process.send_messages())
    for process in processes:
        process.update_tree(messages)
    return processes

def simulation_other_rounds(processes, number_of_faults):
    for round in range(1, number_of_faults+1):
        messages = []
        for process in processes:
            messages.append(process.send_messages())
        for process in processes:
            process.update_tree(messages)

    processes_decisions = []
    for process in processes:
        processes_decisions.append(process.decision_making())

    return processes, processes_decisions

def print_result(processes, processes_decisions):
    for index, process in enumerate(processes):
        print("level f+1 info: ", process.print_final_info())
        print("final decision:", processes_decisions[index])

if __name__ == '__main__':
    number_of_processes = int(input("enter the number of processes: "))
    number_of_faulty_processes = int(input("enter the number of faulty processes: "))
    key_server = PublicKeyServer(number_of_processes)
    list_of_processes = generate_process(number_of_processes, number_of_faulty_processes)
    list_of_processes = simulation_round1(list_of_processes)
    list_of_processes, decisions = simulation_other_rounds(list_of_processes, number_of_faulty_processes)
    print_result(list_of_processes, decisions)
