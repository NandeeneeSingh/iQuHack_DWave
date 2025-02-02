from dwave.optimization.generators import capacitated_vehicle_routing
from dwave.system import LeapHybridNLSampler

# Define the shelter and demand
depot = (0, 0)
depot_demand = 200

# Define the surrounding restaurants and their associated supply
restaurants = [(15, 38, 50), (23, -19, 100), (44, 62, 100)]

# Extract locations and supplies 
locations_x = [x for x, y, s in restaurants]
locations_y = [y for x, y, s in restaurants]
supply = [s for x, y, s in restaurants]

# Track demand of depot 
remaining_demand = depot_demand

# Ensure depot is considered a location truck travels to
locations_x = [depot[0]] + locations_x  # Add depot coordinates to list
locations_y = [depot[1]] + locations_y # Add depot coordinates to list

# Create the CVRP model to fulfill demands + minimize distance
model = capacitated_vehicle_routing(
    demand = [remaining_demand] + [0] * len(supply), # Restuarants don't have demand
    number_of_vehicles = 3,  # Updated to 3 vehicles
    vehicle_capacity = 200,
    locations_x=locations_x,
    locations_y=locations_y, 
    depot_x_y=depot)

# Use the LeapHybridNLSampler
sampler = LeapHybridNLSampler()
results = sampler.sample(model, time_limit=10, num_reads = 50)
print(f"Results: {results}")

# Extract the routes dynamically
route, = model.iter_decisions()
routes = list(route.iter_successors())  # Convert iterator to list

# Print results for up to 3 best solutions
num_samples = model.states.size()
for i in range(min(3, num_samples)):
    print(f"Objective value {int(model.objective.state(i))} for")

    # Track supply usage
    demand_met = False
    current_demand = remaining_demand

    for j, r in enumerate(routes):
        print(f"\t Route {j + 1}: {r.state(i)}")
        if current_demand <= 0: #Check demands met after route
            demand_met = True
            break

        for restaurant_idx, supply_value in enumerate(supply):
            if restaurant_idx == r.state(i):
                current_demand -= supply_value # Subtract visited supply from demand of depot
    # Check if demand met    
    if demand_met: 
        print(f"Demand successfully met after route {i + 1}.\n")
    else: 
        print(f"Demand not fully met after route {i + 1}.\n")

