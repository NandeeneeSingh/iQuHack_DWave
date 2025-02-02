import dimod
from dwave.system import LeapHybridSampler

# Parameters
demand = [100, 200, 300, 400, 500]
vehicle_capacity = 200
num_vehicles = 2
sites = [(15, 38), (23, -19), (44, 62), (3, 12), (-56, -21)]
num_shelters = len(demand)

# Create a constrained quadratic model
qm = dimod.ConstrainedQuadraticModel()

# Define the variables (this can represent vehicle-shelter assignments)
# For simplicity, we'll use x_ij where i = vehicle index, j = shelter index
x = {}
for i in range(num_vehicles):
    for j in range(num_shelters):
        var_name = f'x_{i}_{j}'
        qm.add_variable(dimod.BINARY, var_name)  # Define variable type

# Create distance matrix (example: Euclidean distance between shelters)
distance_matrix = [[(15 - x)**2 + (38 - y)**2 for (x, y) in sites] for (x, y) in sites]

# Step 1: Add the quadratic coefficients (distances between vehicle-shelter pairs)
quadratic = {}
for i in range(num_vehicles):
    for j in range(num_shelters):
        for k in range(i, num_vehicles):
            if i != k:
                var_name_i = f'x_{i}_{j}'
                var_name_k = f'x_{k}_{j}'
                distance_cost = distance_matrix[i][j] + distance_matrix[k][j]
                quadratic[(var_name_i, var_name_k)] = distance_cost  # Add the interaction cost

# Step 2: Set the linear coefficients (cost of assigning a vehicle to a shelter)
linear = {}
for i in range(num_vehicles):
    for j in range(num_shelters):
        var_name = f'x_{i}_{j}'
        linear_cost = distance_matrix[i][j]
        linear[var_name] = linear_cost  # Add linear cost (distance)

# Add quadratic coefficients to the quadratic model using add_interaction
for (u, v), cost in quadratic.items():
    qm.add_quadratic(u, v, cost)

# Add linear coefficients to the quadratic model using set_linear
for var, cost in linear.items():
    qm.set_linear(var, cost)

# Add constraints to the quadratic model (vehicle constraint: each vehicle must visit exactly one shelter)
for i in range(num_vehicles):
    linear_terms = [f'x_{i}_{j}' for j in range(num_shelters)]
    qm.add_constraint(linear_terms, operator='==', value=1)

# Each shelter's demand must be met
for j in range(num_shelters):
    linear_terms = [f'x_{i}_{j}' for i in range(num_vehicles)]
    qm.add_constraint(linear_terms, operator='>=', value=demand[j] / vehicle_capacity)

# Step 3: Sample from the Quadratic Model using the sampler
sampler = LeapHybridSampler()
sample_set = sampler.sample(qm)

# Print the results
for sample in sample_set:
    print(sample)
