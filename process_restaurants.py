import csv

# Open and read CSV file
def process_restaurants_csv(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)  
        headers = next(reader)  # Read the header row

        headers = [h for h in headers if h]

        # data = {column: [] for column in headers}
        restaurant_names, capacities, sites = [], [], []

        for row in reader:
                row = [value for value in row if value]  # Remove empty strings
                
                name = row[0]
                latitude = float(row[1])
                longitude = float(row[2])
                capacity = int(row[3])
                
                restaurant_names.append(name)
                sites.append((latitude, longitude))
                capacities.append(capacity)

    # # Print extracted column data
    # for col, values in data.items():
    #     print(f"{col}: {values}")
        # print(data.items())
    
    return (restaurant_names, sites, capacities)

process_restaurants_csv('IQuHack Data - Sheet3 2.csv')
