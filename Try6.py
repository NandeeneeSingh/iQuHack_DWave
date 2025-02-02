from dwave.optimization.generators import capacitated_vehicle_routing
from dwave.system import LeapHybridNLSampler

# Define the shelter and demand
depot = (0, 0)
depot_demand = 200  # Depot has demand

# Define the surrounding restaurants and their associated supply
restaurants = [(15, 38, 50), (23, -19, 100), (44, 62, 100)]

# Extract locations and supplies
locations_x = [x for x, y, s in restaurants]
locations_y = [y for x, y, s in restaurants]
supply = [s for x, y, s in restaurants]

# Initialize the demand list with depot demand and zero for restaurant demands
demand = [depot_demand] + [0] * len(supply)  # Depot has demand, restaurants have no demand

# Ensure depot is included in locations
locations_x = [depot[0]] + locations_x  # Add depot coordinates to the list
locations_y = [depot[1]] + locations_y  # Add depot coordinates to the list

# Create the CVRP model to fulfill demands + minimize distance
model = capacitated_vehicle_routing(
    demand=demand,  # Demand list where depot has non-zero demand, others are zero
    number_of_vehicles=3,  # Updated to 3 vehicles
    vehicle_capacity=200,
    locations_x=locations_x, 
    locations_y=locations_y,
    depot_x_y=depot  # Explicitly provide depot_x_y
)

# Use the LeapHybridNLSampler with verbose output to debug
sampler = LeapHybridNLSampler()
results = sampler.sample(model, time_limit=10, num_reads=50)

# Output the results from the sampler
print(f"Results: {results}")

# Extract the routes dynamically
route, = model.iter_decisions()
routes = list(route.iter_successors())  # Convert iterator to list

# Track the demand fulfillment
num_samples = model.states.size()  # This is important to determine how many samples were returned
for i in range(min(3, num_samples)):
    print(f"Objective value {int(model.objective.state(i))} for")
    
    # Initialize variables to track the supply usage
    demand_met = False
    remaining_demand = depot_demand  # Track remaining depot demand dynamically
    
    # Check the routes and calculate if the demand has been met
    for j, r in enumerate(routes):
        print(f"\t Route {j + 1}: {r.state(i)}")
        
        # Subtract the supply from the current demand based on the route
        for restaurant_idx, supply_value in enumerate(supply):
            if restaurant_idx == r.state(i):
                remaining_demand -= supply_value
                
        if remaining_demand <= 0:
            demand_met = True
            break  # Stop processing if demand is met

    # Check if the demand was met
    if demand_met:
        print(f"Demand successfully met after route {i + 1}.\n")
    else:
        print(f"Demand not fully met after route {i + 1}.\n")
