import dimod
from dwave.system import LeapHybridSampler
import numpy as np

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Parameters
depot = (0, 0)  # Depot location (can be any arbitrary point)
demand = [10, 20]  # Demand at each site
vehicle_capacity = 50  # Capacity of each vehicle
num_vehicles = 1  # Number of vehicles
sites = [(15, 38), (21, -19)]  # Sites locations
num_sites = len(sites)

# Initialize the binary quadratic model (BQM)
bqm = dimod.BinaryQuadraticModel(vartype='BINARY')


# Print the distance between depot and each site
dist_depot_to_sites = [calculate_distance(depot, site) for site in sites]

#sets the lowest value to first index 
lowest_value = dist_depot_to_sites[0]
num_vehicle_index = 0
num_site_index =0
#finds lowest value to deposite site
# print("Distances from depot to sites:")
# for i, dist in enumerate(dist_depot_to_sites):
#     if dist_depot_to_sites[i] < lowest_value:
#         lowest_value = dist_depot_to_sites[i]
#     print(f"Depot to site {i}: {dist:.2f}")

# Add binary variables for vehicle-site assignments with distances as linear terms
for i in range(num_vehicles):
    for j in range(num_sites):
        #var_name = f'x_{i}_{j}'
        #print(var_name)
        #adds the lowest value selected to the deposite site 
        print("num vechicle", i, "num site", j)
       
        distance = dist_depot_to_sites[j]  # Distance from depot to each site
        var_name = f'x_{i}_{j}'
        bqm.add_variable(var_name, distance)
        #print("distance is :", distance )
        if distance < lowest_value:
            lowest_value = distance
            num_vehicle_index = i
            num_sites_index = j


#print("num vechicle", i, "num site", j, "shortest distance:", distance)



print("\nVariables in the BQM:")
print(bqm.variables)

# Add constraint: Each site must be assigned at least one vehicle (no capacity constraint for simplicity)
penalty = 0.0  # Small penalty to encourage assignments
for j in range(num_sites):
    constraint_variables = [f'x_{i}_{j}' for i in range(num_vehicles)]
    # Add quadratic terms to enforce exactly one vehicle per site
    for idx1, v1 in enumerate(constraint_variables):
        for idx2, v2 in enumerate(constraint_variables[idx1+1:], idx1+1):
            bqm.add_interaction(v1, v2, penalty)

for (var1, var2), bias in bqm.quadratic.items():
    print(f"{var1} - {var2}: {bias}")

# Now solve using the LeapHybridSampler
sampler = LeapHybridSampler()
sampleset = sampler.sample(bqm)

# Print the solution
print("\nBest solution (binary values):")
print(sampleset.first.sample)

# Calculate and print the total distance
total_distance = 0
best_solution = sampleset.first.sample
for i in range(num_vehicles):
    for j in range(num_sites):
        var_name = f'x_{i}_{j}'
        if best_solution[var_name] == 1:
            distance = dist_depot_to_sites[j]  
            print("Distance is ", distance)
            # Distance from depot to each site
            total_distance += distance
            print(f"Vehicle {i} assigned to site {j}")
            print(f"  Distance: {distance:.2f}")
            print(f"  Demand: {demand[j]}")
            print()

print(f"Total distance: {total_distance:.2f}")