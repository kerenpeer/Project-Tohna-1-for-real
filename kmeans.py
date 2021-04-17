import sys

# calculates the distance between 2 points
def calc_dist(point1, point2):
    sum = 0.0
    for i in range(len(point1)):
        sum += (point1[i] - point2[i]) ** 2
    return sum

# goes over all centroids and returns the closest one to point
def find_closest_centroid(point, curr_centroid, centroids):
    closest = curr_centroid
    if closest == float('inf'):
        closest_dist = float('inf')
    else:
        closest_dist = calc_dist(point, centroids[closest][0])

    for centroid in centroids.keys():
        this_dist = calc_dist(point, centroids[centroid][0])
        if this_dist < closest_dist:
            closest = centroid
            closest_dist = this_dist
    return closest

# removes a point from the centroid it was in
def remove_point_from_centroid(point, centroid, centroids):
    if centroid == float('inf'):
        # x isn't in a centroid, no need to remove
        return
    centroid_point , amount  = centroids[centroid]
    if amount == 1:
        centroids[centroid] = ((0 for i in range(len(point))), 0)
    else:
        for i in range(len(point)):
            centroid_point[i] = (centroid_point[i] * amount - point[i]) / (amount-1)
        centroids[centroid][1] -= 1

# adds a point to a specified centroid
def add_poind_to_centroid(point, centroid, centroids):
    centroid_point , amount  = centroids[centroid]
    for i in range(len(point)):
        centroid_point[i] = (centroid_point[i] * amount + point[i]) / (amount+1)
    centroids[centroid][1] += 1

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
            centroids[index] = [list(point), 1] # [mean , amount of points in the centroid]
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

changes = True
index = 0
while changes:
    # if max_iter was provided, check
    if max_iter:
        if index == max_iter:
            break
        index+=1

    changes = False
    for point , curr_centroid in points_to_centroids.items():
        new_centroid = find_closest_centroid(point, curr_centroid, centroids)
        if new_centroid != curr_centroid:
            remove_point_from_centroid(point, curr_centroid, centroids)
            add_poind_to_centroid(point, new_centroid, centroids)
            points_to_centroids[point] = new_centroid
            changes = True

with open("output.txt", "w") as f:
    for centroid_list in centroids.values():
        output_line = f'{[round(x,4) for x in centroid_list[0]]}'
        output_line = output_line.replace(" ","")
        f.write(f'{output_line[1:-1]}\n')
