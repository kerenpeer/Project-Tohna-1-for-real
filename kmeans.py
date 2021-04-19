import sys

# truncate the decimals of a float
def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)

# calculates the distance between 2 points
def calc_dist(point1, point2):
    sum = 0.0
    for i in range(len(point1)):
        sum += (point1[i] - point2[i]) ** 2
    return sum

# goes over all centroids and returns the closest one to point
def find_closest_centroid(point, curr_centroid, centroids):
    closest = curr_centroid
    # print(f'find_closest_centroid: closest centroid is: {closest}')
    if closest == float('inf'):
        closest_dist = float('inf')
    else:
        # print(f'find_closest_centroid: calc dist between {point} , {centroids[closest][0]}')
        closest_dist = calc_dist(point, centroids[closest][0])
    # print(f'find_closest_centroid: closest_dist is: {closest_dist}')

    for centroid in centroids.keys():
        # print(f'find_closest_centroid: calc dist between {point} , {centroids[centroid][0]}')
        this_dist = calc_dist(point, centroids[centroid][0])
        # (f'find_closest_centroid: this_dist is: {this_dist}')
        if this_dist < closest_dist:
            # print (f'find_closest_centroid: found closer centroid. Dist is: {this_dist}, centroid is: {centroid}')
            closest = centroid
            closest_dist = this_dist
            # print(f'find_closest_centroid: new closest is: {closest} , closest_dist is: {closest_dist}')
    return closest

# removes a point from the centroid it was in
def remove_point_from_centroid(point, centroid, centroids):
    # print(f'remove_point_from_centroid: removing point {point} from centroid {centroid}')
    if centroid == float('inf'):
        # x isn't in a centroid, no need to remove
        # print(f'remove_point_from_centroid: centroid is inf, nowhere to remove from')
        return
    centroid_point , amount  = centroids[centroid]
    # print(f'remove_point_from_centroid: centroid_point is {centroid_point}, amount is: {amount}')
    # if amount == 1:
    #     centroids[centroid] = ((0 for i in range(len(point))), 0)
    # else:
    for i in range(len(point)):
        centroid_point[i] = (centroid_point[i] * amount - point[i]) / (amount-1)
    centroids[centroid][1] -= 1
    # print(f'remove_point_from_centroid: centroid after removal is: {centroids[centroid]}')

# adds a point to a specified centroid
def add_point_to_centroid(point, centroid, centroids):
    # print(f'add_point_to_centroid: adding point {point} to centroid {centroid}')
    centroid_point , amount  = centroids[centroid]
    # print(f'add_point_to_centroid: centroid_point is {centroid_point}, amount is: {amount}')
    for i in range(len(point)):
        centroid_point[i] = (centroid_point[i] * amount + point[i]) / (amount+1)
    centroids[centroid][1] += 1
    # print(f'add_point_to_centroid: centroid after addition is: {centroids[centroid]}')

# initialises first k points to centroids 1,...,k and the rest to centroid 'inf'
# initialises centroids 1,...,k to contain points 1,...,k accordingly
def initialise():
    points_to_centroids = {}
    centroids = {}
    index = 0
    while (True):
        try:
            input_point = input()
        except EOFError:
            # no more points in file
            break
        point = [float(x) for x in input_point.split(',')]
        point = tuple(point) # turn point to immutable do it can be a dict key
        if index<k:
            points_to_centroids[point] = index
            centroids[index] = [list(point), 1] # [point , amount of points in the centroid]
        else:
            points_to_centroids[point] = float('inf')
        index+=1
    return points_to_centroids, centroids, index


# main
k = int(sys.argv[1])
try:
    max_iter = int(sys.argv[2])
except IndexError:
    max_iter = None

points_to_centroids , centroids, n = initialise()

# print(f'points_to_centroids:\n{points_to_centroids}')
# print(f'centroids:\n{centroids}')

changes = True
index = 0
while changes:
    # if max_iter was provided, check
    if max_iter:
        if index == max_iter:
            # print('max iterations acheived')
            break
        index+=1

    changes = False
    for point , curr_centroid in points_to_centroids.items():
        # print(f'going over point: {point}, in centroid {curr_centroid}')
        new_centroid = find_closest_centroid(point, curr_centroid, centroids)
        # print(f'new_centroid is: {new_centroid}')
        if new_centroid != curr_centroid:
            # print(f'centroids are different')
            remove_point_from_centroid(point, curr_centroid, centroids)
            add_point_to_centroid(point, new_centroid, centroids)
            points_to_centroids[point] = new_centroid
            changes = True
            # print(f'points_to_clusters = {points_to_centroids}')
            # print(f'centroids are: {centroids}')

# print('\n\n')
# print(f'points_to_clusters = {points_to_centroids}')
# print(f'centroids are: {centroids}')

with open("output.txt", "w") as f:
    for i in range(len(centroids)):
        four_decimals = ['%.4f' % x for x in centroids[i][0]]
        output_line = f'{four_decimals}'
        output_line = output_line.replace(" ","").replace("'", "")
        f.write(f'{output_line[1:-1]}\n')
