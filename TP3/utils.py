def sum_line(energy_matrix):
    """Get an energy matrix, sum the value for each line and return the list of summed values

    Args:
        energy_matrix (list): a list of all the sum of each line
    """
    sum_list = []
    for line in energy_matrix:
        sum_list.append(sum(line))
    return sum_list

def get_node_connection(line_list):
    """Get a list of all the lines in the graph and 
    return a list of all the nodes with its decreasing amount of neighbours.

    Args:
        line_list (list of list): list of all the lines in the graph

    Returns:
        list of tuple: dict of all the nodes with its decreasing amount of neighbours
    """
    position_dict = {}
    for item in line_list:
        a,b  = item[0], item[1]
        try:
            position_dict[a] += 1
        except:
            position_dict.update({a: 1})
        try:
            position_dict[b] += 1
        except:
            position_dict.update({b: 1})
    return (sorted(position_dict.items(),
                   key=lambda item: item[1], reverse=True))


def compute_energy(sol, energy_matrix, line_list):
    """compute the energy of each nodes in the graph

    Args:
        sol (dict): dict of all node with it's type
        energy_matrix (list of list): energy matrix based on atom type
        line_list (list): list of all the lines in the graph
    """
    energy = 0
    for line in line_list:
        a,b = sol[line[0]], sol[line[1]]
        if a != None and b != None:
            energy += energy_matrix[a][b]
    return energy