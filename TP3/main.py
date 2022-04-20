import argparse
import datetime
import random
from utils import *

def open_file(path):
    """Open data file, read it and parse data

    Args:
        path (string): data file path

    Returns:
        total_atoms : int
        total_types : int
        total_lines : int
        type_list : list of atoms types (size is based on total_types)
        energy_matrix : list of lists of energy values (size is based on total_types)
        args_list : list of lists of graph lines (size is based on total_lines)
    """
    args_list = []
    with open(path, 'r') as file:
        energy_matrix = []
        for count, line in enumerate(file):
            splitted_line = line.split()
            if count == 0:
                total_atoms, total_types, total_lines = (int(x) for x in splitted_line)
            elif count == 2:
                type_list = list(int(x) for x in splitted_line)
            elif count > 3 and count < total_types + 4:
                energy_matrix.append(list(int(x) for x in splitted_line))
            elif count > total_types + 5:
                args_list.append(line.strip().split(' '))
            if line == '\n':
                continue

    return total_atoms, total_types, total_lines, type_list, energy_matrix, args_list

def glouton(energy_matrix, line_list, type_list):
    sum_list = sum_line(energy_matrix)
    node_list = get_node_connection(line_list)
    
    sol = {}
    for node in node_list:
        current_node = node[0]
        min_index = min(range(len(sum_list)), key=sum_list.__getitem__)
        type_list[min_index] -= 1
        if type_list[min_index] < 0:
            found = False
            while not(found):
                sum_list[min_index] = float('inf')
                min_index = min(range(len(sum_list)), key=sum_list.__getitem__)
                type_list[min_index] -= 1
                if type_list[min_index] >= 0:
                    found = True
        sol[current_node] = min_index
    return dict(sorted(sol.items(), key=lambda item:item[0]))

def findBetterSolution(sol, energy_matrix, line_list, param):
    best_sol = sol.copy()
    best_sol_energy = compute_energy(best_sol, energy_matrix, line_list)
    current_sol = sol.copy()
    displaySol(best_sol,best_sol_energy,param)
    lines_tested = []
    lines_to_test = line_list.copy()
    while True:
        if not lines_to_test:
            lines_to_test = line_list.copy()
            lines_tested = []
        line_to_switch = random.choice(lines_to_test)
        lines_to_test.remove(line_to_switch)
        lines_tested.append(line_to_switch)

        #We swap the values of neighbouring nodes
        a, b = current_sol[line_to_switch[0]], current_sol[line_to_switch[1]]
        current_sol[line_to_switch[0]], current_sol[line_to_switch[1]] = b, a

        current_sol_energy = compute_energy(current_sol, energy_matrix, line_list)

        #We check if our newfound solution has a better energy
        if current_sol_energy < best_sol_energy:
            best_sol = current_sol.copy()
            best_sol_energy = current_sol_energy
            displaySol(best_sol, best_sol_energy, param)
        else:
            a, b = current_sol[line_to_switch[0]], current_sol[line_to_switch[1]]
            current_sol[line_to_switch[0]], current_sol[line_to_switch[1]] = b, a

def displaySol(best_sol, best_sol_energy, param):
    if param:
        index = 0
        string_to_return = ''
        while index != len(best_sol):
            string_to_return += str(best_sol[str(index)]) + ' '
            index += 1
        print(string_to_return, flush=True)
    else:
        print(best_sol_energy, flush=True)

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", \
                        help="Data file to import", \
                        action='store', required=True, metavar='DATA_FILE')
    parser.add_argument("-p", "--parametre", \
                        help="Display energy solution", \
                        action='store', choices=['True', 'False'], default='False')

    args = parser.parse_args()
    total_atoms, total_types, total_lines, type_list, energy_matrix, args_list = open_file(args.file)
    now = datetime.datetime.now()
    sol = glouton(energy_matrix.copy(), args_list.copy(), type_list.copy())
    energy = compute_energy(sol, energy_matrix, args_list)
    if args.parametre == 'True':
        findBetterSolution(sol, energy_matrix.copy(), args_list.copy(), True)
    else :
        findBetterSolution(sol, energy_matrix.copy(), args_list.copy(), False)
