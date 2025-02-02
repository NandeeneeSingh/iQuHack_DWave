import dimod
from dwave.system import LeapHybridSampler
import numpy as np

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return float(np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2))

# Parameters
demand = [200, 400, 300, 400, 500]
vehicle_capacity = 200
num_vehicles = 3
sites = [(15, 38), (23, -19), (44, 62), (3, 12), (-56, -21)]
num_shelters = len(demand)

# Create Binary Quadratic Model instead of Quadratic Model
bqm = dimod.BinaryQuadraticModel(vartype='BINARY')

# Define binary variables and their coefficients directly in the model
for i in range(num_vehicles):
    for j in range(num_shelters):
        var_name = f'x_{i}_{j}'
        distance = calculate_distance(sites[i], sites[j])
        bqm.add_variable(var_name, distance)

# Add constraints as penalties
penalty = 1000.0

# Each shelter must be served by exactly one vehicle
for j in range(num_shelters):
    constraint_variables = [f'x_{i}_{j}' for i in range(num_vehicles)]
    
    # Add quadratic terms to enforce exactly one vehicle per shelter
    for idx1, v1 in enumerate(constraint_variables):
        for idx2, v2 in enumerate(constraint_variables[idx1+1:], idx1+1):
            bqm.add_interaction(v1, v2, 2 * penalty)
        bqm.add_variable(v1, -2 * penalty)
    bqm.offset += penalty

# Each vehicle can serve at most one shelter
for i in range(num_vehicles):
    constraint_variables = [f'x_{i}_{j}' for j in range(num_shelters)]
    
    # Add quadratic terms to enforce at most one shelter per vehicle
    for idx1, v1 in enumerate(constraint_variables):
        for idx2, v2 in enumerate(constraint_variables[idx1+1:], idx1+1):
            bqm.add_interaction(v1, v2, 2 * penalty)

# Capacity constraints
for i in range(num_vehicles):
    for j in range(num_shelters):
        if demand[j] > vehicle_capacity:
            bqm.add_variable(f'x_{i}_{j}', penalty * 10)  # Heavy penalty for exceeding capacity

# Solve using D-Wave's hybrid sampler
sampler = LeapHybridSampler()
sampleset = sampler.sample(bqm)

# Process and print results
best_solution = sampleset.first.sample
print("\nBest solution found:")
print("-" * 50)

total_distance = 0
for i in range(num_vehicles):
    for j in range(num_shelters):
        var_name = f'x_{i}_{j}'
        if best_solution[var_name] == 1:
            distance = calculate_distance(sites[i], sites[j])
            total_distance += distance
            print(f"Vehicle {i} assigned to shelter {j}")
            print(f"  Distance: {distance:.2f}")
            print(f"  Demand: {demand[j]}")
            print()

print(f"Total distance: {total_distance:.2f}")

# Verify constraints
print("\nConstraint verification:")
print("-" * 50)

# Check capacity constraints
for i in range(num_vehicles):
    total_load = sum(demand[j] for j in range(num_shelters) 
                    if best_solution[f'x_{i}_{j}'] == 1)
    print(f"Vehicle {i} load: {total_load}/{vehicle_capacity}")

# Check shelter assignments
for j in range(num_shelters):
    assigned_vehicles = sum(best_solution[f'x_{i}_{j}'] for i in range(num_vehicles))
    print(f"Shelter {j} assigned to {assigned_vehicles} vehicles")