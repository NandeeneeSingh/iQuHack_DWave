from dwave.optimization.generators import capacitated_vehicle_routing
from dwave.system import LeapHybridNLSampler
from process_restaurants import process_restaurants_csv

# demand = [0, 34, 12, 65, 10, 43, 27, 55, 61, 22]
# sites = [(15, 38), (23, -19), (44, 62), (3, 12), (-56, -21), (-53, 2),
#          (33, 63), (14, -33), (42, 41), (13, -62)]

# initialize shelter data 
# Family-Aid Boston,42.2981,,-71.1166
capacities = [0]
sites = [(42.2981, -71.1166)]
res_data = process_restaurants_csv('IQuHack Data - Sheet3 2.csv')
sites.extend(res_data[1])
capacities.extend(res_data[2])



model = capacitated_vehicle_routing(
    demand=capacities,
    number_of_vehicles=2,
    vehicle_capacity=200,
    locations_x=[x for x,y in sites],
    locations_y=[y for x,y in sites])

sampler = LeapHybridNLSampler()                  

results = sampler.sample(
    model,
    time_limit=10)  

num_samples = model.states.size()
route, = model.iter_decisions()      
print("route: ", route.iter_successors())              
route1, route2 = route.iter_successors()            
for i in range(min(3, num_samples)):
    print(f"Objective value {int(model.objective.state(i))} for \n" \
    f"\t Route 1: {route1.state(i)} \t Route 2: {route2.state(i)} \n" \
    f"\t Feasible: {all(sym.state(i) for sym in model.iter_constraints())}")

