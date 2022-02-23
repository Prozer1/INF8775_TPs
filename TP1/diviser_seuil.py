import argparse, datetime


# Ouvre le ficher contenant les donnees
def open_file(path):
    args_list = []
    with open(path, 'r') as file:
        index = 0
        range
        for line in file:
            if index == 0:
                index += 1
                continue
            args_list.append(line.split())
    return args_list

# Ecrit le resultat de l'algorithme dans un fichier texte
def write_string(string_list):
    with open('./TP1/data/result_diviser.txt', 'w') as file:
        index = 0
        total_string = len(string_list)
        for string in string_list:
            if index == total_string - 1:
                string = string[:-1]
            file.write(string)
            index += 1

# Genere une liste de points critiques issu de la liste des batiments
def create_crit_point(args_list):
    crit_points = []
    for coords in args_list:  # pour chaque set de coordonees x1, x2, h de la liste de batiments
        crit_points.append((int(coords[0]), int(coords[2])))  # x1, h
        crit_points.append((int(coords[1]), 0))  # x2, 0
    crit_points.sort()
    return crit_points

# Implementation de l'algorithme brute force pour l'algorithme diviser.
# La seule difference avec l'implementation dans brute_force_lent.py est que les points sont
# retournes dans un tableau de points et non de string
def compute_skyline_naive(args_list, crit_points):
    solution_naive = []
    last_point = (-1, -1)
    for coords in crit_points:
        crit_x = int(coords[0])
        crit_y = int(coords[1])
        for buildings in args_list:
            x_1, x_2, h = int(buildings[0]), int(buildings[1]), int(buildings[2])
            if (crit_x >= x_1 and crit_x < x_2) and (crit_y >= 0 and crit_y <= h):
                if crit_y < h:
                    crit_y = h
        if crit_y != last_point[1]:
            solution_naive.append((crit_x, crit_y))
            last_point = (crit_x, crit_y)
    return solution_naive

# Implementation de l'algorithme diviser pour regner
def compute_skyline_divide(args_list):
    solution_divide = []
    if len(args_list) <= 3: # Seuil de recursion a 1 pour l'execution de l'algorithme brute
        crit_points = create_crit_point(args_list)
        solution_divide = compute_skyline_naive(args_list, crit_points)
    else:
        # Phase de division du dataset
        length = len(args_list)
        middle_index = length // 2
        blue_sol = compute_skyline_divide(args_list[:middle_index])
        green_sol = compute_skyline_divide(args_list[middle_index:])
        solution_divide = fusion(blue_sol, green_sol)
    return solution_divide

# Phase de fusion des sous-solutions
def fusion(blue_sol, green_sol):
    solution_fusion = []
    crit_points = []
    # On "colorie" les points critiques en bleu et verts
    for point in blue_sol:
        crit_points.append((point, True))
    for point in green_sol:
        crit_points.append((point, False))
    crit_points.sort(key=getX)

    # Calcule de la nouvelle skyline
    last_point = (-1, -1)
    h_blue, h_green = -1, -1
    for point in crit_points: # On parcoure tous les points critiques
        if point[1]:
            h_blue = point[0][1] # Si le point est bleu on redefinie la hauteur bleue
        else:
            h_green = point[0][1] # Si le point est vert on redefinie la hauteur verte
        current_height = max(h_blue, h_green)
        if current_height != last_point[1]: # Si le point n'est pas a la meme hauteur que le point precedent il est garde
            if point[0][0] == last_point[0]: # On enleve les points ayant la meme abcsisse
                solution_fusion.pop()
            last_point = (point[0][0], current_height)
            solution_fusion.append(last_point)
    return solution_fusion

# Methode lambda pour trier les points critiques "colories" par leur abscisse
def getX(crit_point):
    return crit_point[0][0]

# Renvoit la liste des points critiques en string
def computeSol(sol):
    text_sol = []
    for point in sol:
        text_sol.append(f"{point[0]} {point[1]}\n")
    return text_sol


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", \
                        help="Data file to import", \
                        action='store', required=True, metavar='DATA_FILE')
    parser.add_argument("-t", "--time", help="time display")

    args = parser.parse_args()
    args_list = open_file(args.file)
    now = datetime.datetime.now()
    solution = compute_skyline_divide(args_list)
    write_string(computeSol(solution))
    calculated = datetime.datetime.now() - now
    calculated = calculated.total_seconds() * 1000.0
    if args.time == "True":
        print(calculated)
