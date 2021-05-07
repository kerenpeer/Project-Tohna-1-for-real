import sys

def initialise(k: int):
    points = []
    points_to_clusters = []
    clusters_to_points = []
    clusters_to_centroids = []
    index = 0
    while (True):
        try:
            input_point = input()
        except EOFError:
            # no more points in file
            break
        point = [float(x) for x in input_point.split(',')]
        points.append(point) # this point's id is "index"
        if index<k:
            points_to_clusters.append(index) # asign cluster "index" to point "index" 
            clusters_to_points.append([index]) # asign point "index" to cluster "index"
            clusters_to_centroids.append(point) # set "point" as cluster "index"'s centroid
        else:
            points_to_clusters.append(None) # asign cluster "None" to point "index" 
        index+=1
    return points, points_to_clusters, clusters_to_points, clusters_to_centroids, index

def calc_centroid(cluster_id: int):
    sum = [0.0 for i in range(dim)]
    amount_points_in_cluster = len(clusters_to_points[cluster_id])
    for point_id in clusters_to_points[cluster_id]:
        point = points[point_id]
        for i in range(dim):
            sum[i] += point[i]
    for i in range(dim):
        sum[i] = sum[i]/amount_points_in_cluster
    return sum

def get_centroid(cluster_id: int):
    return clusters_to_centroids[cluster_id]

# calculates the distance between 2 points
def calc_dist(point1: list, point2: list):
    sum = 0.0
    for i in range(len(point1)):
        sum += (point1[i] - point2[i]) ** 2
    return sum

def find_closest_cluster(point: list, curr_cluster: int):
    closest_cluster = curr_cluster
    if closest_cluster is None:
        closest_dist = float('inf')
    else:
        centroid = get_centroid(curr_cluster)
        closest_dist = calc_dist(point, centroid)
    for cluster_id in range(len(clusters_to_points)):
        centroid = get_centroid(cluster_id)
        this_dist = calc_dist(point, centroid)
        if this_dist < closest_dist:
            closest_dist = this_dist
            closest_cluster = cluster_id
    return closest_cluster

def move_point(point_id: int, curr_cluster:int, new_cluster: int):
    if curr_cluster is not None:
        clusters_to_points[curr_cluster].remove(point_id)    
    clusters_to_points[new_cluster].append(point_id)
    points_to_clusters[point_id] = new_cluster

# main
try:
    k = int(sys.argv[1])
except:
    print ("invalid input")
try:
    max_iter = int(sys.argv[2])
except Exception as e:
    if type(e) == IndexError:
        max_iter = 200
    else:
        print ("invalid input")

points, points_to_clusters, clusters_to_points, clusters_to_centroids, n = initialise(k)

changes = True
index = 0
dim = len(points[0])
while changes:
    if index == max_iter:
        break
    index+=1

    changes = False
    for i in range(len(points)):
        point = points[i]
        curr_cluster = points_to_clusters[i]
        new_cluster = find_closest_cluster(point, curr_cluster)
        if new_cluster != curr_cluster:
            move_point(i, curr_cluster, new_cluster)
            changes = True
    for i in range(len(clusters_to_points)):
        new_centroid = calc_centroid(i)
        clusters_to_centroids[i] = new_centroid

# print to cmd
for i in range(len(clusters_to_points)):
    centroid = get_centroid(i)
    four_decimals = ['%.4f' % x for x in centroid]
    output_line = f'{four_decimals}'
    output_line = output_line.replace(" ","").replace("'","")
    print(f'{output_line[1:-1]}')