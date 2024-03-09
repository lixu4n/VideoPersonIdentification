# Read data from resultcleaned.txt
with open('result.txt', 'r') as file:
    data = file.readlines()

# Define a dictionary to store data for each object
object_data = {}

# Extract object information and percentages
for line in data:
    if line.startswith("Object"):
        current_object = line.strip()
        object_data[current_object] = []
    elif line.startswith("- Similar image"):
        object_data[current_object].append(line.strip())

# Sort percentages for each object
for obj, similarities in object_data.items():
    object_data[obj] = sorted(similarities, key=lambda x: float(x.split(":")[-1][:-1]), reverse=True)

# Write sorted data to sortdata.txt
with open('sortdata.txt', 'w') as file:
    for obj, similarities in object_data.items():
        file.write(obj + '\n')
        for sim in similarities:
            file.write(sim + '\n')
        file.write('\n')

#this allow us to  sorte the %