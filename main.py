# Algorithm used: Nearest Neighbor

# Importing csv for the csv file reader
import csv

# Importing datetime for time keeping
import datetime

# Creating the HashTable

# The creation of the hashTable below and the functions contained within
# were influenced from the zybooks chaining has table example,
# as well as Dr. Cemal Tepe's webinar

# Welcome message and initial instructions for the interface
print("Welcome, Please enter a time to see package status")

# Try / Except block to validate user input
while True:
    try:
        user_hour = input("Hour (24-hour format): ")  # Gets entered hour from the user
        user_min = input("Minute (0-60): ")  # Gets entered  minute from user
        userTime = datetime.time(int(user_hour), int(user_min), 0)  # sets the entered time to a date.time.time object
    except ValueError:  # Except block if exception is thrown
        print("Entered values are not in correct format, try again")  # asks user to enter valid values again
        continue  # Prompt fields again
    else:
        break  # breaks loop if values are validated


# 0(n) space complexity
# 0(n) time complexity for all functions (insert, lookup, delete)
class HashTable:
    # Constructor for the hash table, 10 buckets
    # all buckets are assigned with empty list
    def __init__(self, initial_capacity=10):
        # Initializes the empty table
        # initializes the hash table with empty bucket lists
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item in Hash table
    def insert(self, key, item):  # Inserts or updates depending on existence of key in the bucket
        # Gets the bucket list where item will be inserted or updated via the hash function
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for packages in bucket_list:  # loops through bucket list
            if packages[0] == key:  # if the key exists --
                packages[1] = item  # inserts the value (i.e. package object)
                return True

        key_value = [key, item]  # if key does not exist--
        bucket_list.append(key_value)  # appends key/package to the end of the list in the bucket
        return True

    # Searches for item in hashtable, returns value or None if it does not find the item
    def lookup(self, key):
        # Gets the bucket where the key would be given the hash function
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:  # Loops through bucket
            if key_value[0] == key:  # If the passed key matches the key for a key value pair
                return key_value[1]  # Returns the value or object for that key
        return None  # Else returns None

    # Remove item and key from hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)  # Gets the bucket where the key/value is located via the Hash function
        bucket_list = self.table[bucket]

        for key_value in bucket_list:  # Loops through the bucket list
            if key_value[0] == key:  # If the key is found in the bucket list
                bucket_list.remove(
                    [key_value[0], key_value[1]])  # removes the key and the value (i.e. package) from the hashTable


# Creating a Package class
# 0(n) space complexity
# 0(n) time complexity for all functions
class Package:
    # Constructor for a package object
    def __init__(self, id, address, city, state, zipcode, time, weight, description, timestamp):
        self.id = id  # Package id
        self.address = address  # Address the package needs to be delivered at
        self.city = city  # City the package needs to be delivered to
        self.state = state  # State the package needs to be delivered to
        self.zipcode = zipcode  # Zipcode the package needs to be delivered to
        self.time = time  # Time the package needs to arrive by
        self.weight = weight  # Weight of the package
        self.description = description  # Description for the package
        self.timestamp = timestamp  # Timestamp of the delivery
        self.status = None  # status of the delivery, i.e. At hub, or en route, or delivered

    def __str__(self):  # overrides the __str__ method, so we can print package object values, not just memory location
        return 'Package Id: ' + str(
            self.id) + ', Delivery Address: ' + self.address + ', Delivery Deadline: ' + self.time + ', Delivery City: ' + self.state + \
               ', Delivery Zipcode: ' + self.zipcode + ', Package Weight: ' + self.weight + ', Status: ' + self.status


# Creating the Hashtable object (myTable)
# Space and time complexity for the below: 0(n)
myTable = HashTable()
# Using the CSV reader to populate myTable with package objects
with open('WGUPS Package File.csv') as file:  # Defining the name/location of the csv file
    reader = csv.reader(file)  # utilizing the csv reader
    for row in reader:  # Looping through rows in the csv File
        # Creating a package object "x" with the values from the columns in the csv file
        x = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], "")
        # Inserting the package object into the hashtable utilizing the package ID as the key
        myTable.insert(int(x.id), x)


# Creating address class
class Address:
    def __init__(self, i):  # constructor for an address, it's index in the csv
        self.index = i


# Creating the Graph class (adjacency matrix)
# 0(n^2) Space complexity
# 0(n^2) Time complexity
class Graph:
    # Initializing with empty adjacency list
    def __init__(self):
        # Dictionary for this distances and the adjacency list
        self.adjacency_list = {}
        self.distances = {}

    # Creates address object and adds to the graph
    def add_address(self, address):
        self.adjacency_list[address] = []

    # Adds weighted edges to graph
    def add_directed_distances(self, address1, address2, distance=1.0):
        self.distances[(address1, address2)] = distance
        self.adjacency_list[address1].append(address2)

    # Calls above function twice to add both of the edge versions (symmetric i.e. undirected)
    def add_distances(self, address1, address2, distance):
        self.add_directed_distances(address1, address2, distance)
        self.add_directed_distances(address2, address1, distance)


distanceGraph = Graph()
# parsing the csv file that holds the distances and adding them to the graph
# Time and Space complexity was defined above
# 0(n^2) space and time complexity
with open('WGUPS Distance Table (1).csv') as file:  # defining the name/file location of the csv file
    lines = 27
    for x in range(lines):
        distanceGraph.add_address(x + 1)  # Adding that index as an address

    reader = csv.reader(file)  # setting the reader
    for row in reader:  # looping through rows in csv file
        index = reader.line_num  # setting the index of the line to the row number
        for x in range(26):
            distanceGraph.add_distances(index, x + 1, row[x])  # adding distance values for the address id's

# Creates a dictionary address that will allow the return of the address ID associated with the address string
# 0(n) time and space complexity
address_dict = {}


# 0(n) time and space complexity
def populate_address_dictionary(dict):  # Populating the dictionary with values from the csv
    with open('addresses.csv') as file2:  # opening the csv file
        reader2 = csv.reader(file2)  # setting the reader
        for row in reader2:  # iterating through the rows in the reader
            index = reader2.line_num  # setting the index equal to the line number
            dict[row[0]] = index  # setting the value of the dictionary to the key (index)


populate_address_dictionary(address_dict)  # calling the above function


# Big 0 defined above (i.e. 0(n) for both time and space complexity)
def get_id_from_address(address):  # function to return the address id from the address string
    for key in address_dict.keys():  # looping through dictionary keys
        if key == address:  # if key is equal to the address string
            return address_dict.get(key)  # returns address id (value)
    return None  # if not found returns None


# Creating a truck class
# Time and space is 0(n)
class Truck:
    # Truck Constructor
    def __init__(self):
        self.package_list = []  # empty list to contain package id's
        self.mileage = 0  # will store traveled mileage for the truck
        self.return_time = 0  # will store the time the truck returned to the hub

    def __str__(self):  # Overriding __str__ function, so we can print values
        return 'Mileage: ' + str(self.mileage) + ' Returned At: ' + str(self.return_time)


# creating trucks
truckA = Truck()
truckB = Truck()
truckC = Truck()

# MANUALLY LOADING TRUCKS WITH PACKAGE ID's
truckA.package_list.append(13) #
truckA.package_list.append(29) #
truckA.package_list.append(15) #
truckA.package_list.append(19) #
truckA.package_list.append(20) #
truckA.package_list.append(16) #
truckA.package_list.append(14) #
truckA.package_list.append(21) #
truckA.package_list.append(7) #
truckA.package_list.append(10) #
truckA.package_list.append(1)


truckA.package_list.append(30)
truckA.package_list.append(37)

truckB.package_list.append(38) #can only be on truck 2
truckB.package_list.append(36) #can only be on truck 2
truckB.package_list.append(18) #can only be on truck 2
truckB.package_list.append(3) #can only be on truck 2
truckB.package_list.append(23)
truckB.package_list.append(12)
truckB.package_list.append(33)
truckB.package_list.append(27)
truckB.package_list.append(31)
truckB.package_list.append(26)
truckB.package_list.append(2)
truckB.package_list.append(4)
truckB.package_list.append(5)
truckB.package_list.append(40)
truckB.package_list.append(34)
truckB.package_list.append(22)

truckC.package_list.append(25)
truckC.package_list.append(28)
truckC.package_list.append(9)
truckC.package_list.append(32)
truckC.package_list.append(11)
truckC.package_list.append(24)
truckC.package_list.append(39)
truckC.package_list.append(6)
truckC.package_list.append(8)
truckC.package_list.append(35)
truckC.package_list.append(17)
# Creating a copy of truck C list so we can later reference what packages were on truck C
truckC_list_copy = truckC.package_list.copy()


# 18 miles/hour = .3miles / min

# nearest neighbor algorithm
# 0(n) time complexity
# 0(1) space complexity
def algo(truck, start_hour, start_min):  # truck object is passed in, along with starting hour, and starting minuete
    total_time = datetime.datetime(1, 1, 1, start_hour, start_min,
                                   0)  # creating a time- this will be the starting time for
    # deliveries for this truck
    total_mileage = 0  # starting mileage for truck
    current_address = 1  # Starting the truck at the hub
    next_address_id = -1  # Some non-existent address id for the next address
    current_package = -1  # setting the package id to non-existent package id

    while truck.package_list.__len__() != 0:  # While there are packages in the truck
        min_distance = 1000000.0  # set minimum distance to arbitrarily high value
        for packageId in truck.package_list:  # looping through packages on the truck
            # getting the package object from the hashTable given the key (package id)
            package = myTable.lookup(packageId)
            look_up_address = package.address  # getting address for that package
            look_up_id = get_id_from_address(look_up_address)  # getting that address Id for the address string
            # setting a distance float variable to the returned distance from the adjacency matrix given the addresses
            distance = float(distanceGraph.distances[current_address, look_up_id])
            if distance < min_distance:  # if that distance is less than the min distance
                min_distance = distance  # setting the min distance to that distance
                next_address_id = look_up_id  # setting the next addressid to the addressid from the current package
                current_package = packageId  # setting the current_package to the id of the current package in the loop
                time = datetime.timedelta(minutes=(min_distance / 0.3))
            package.timestamp = (total_time + time).time()  # setting the timestamp of the package
        total_time += time  # incrementing the total time
        current_address = next_address_id  # moving addresses
        total_mileage += min_distance  # incrementing distance
        truck.package_list.remove(current_package)  # removing package from list (was delivered)
    # getting distance to return home (hub, last address)
    return_home_dist = float(distanceGraph.distances[1, next_address_id])
    total_mileage += return_home_dist  # incrementing distance with the return home distance
    total_time += datetime.timedelta(minutes=(return_home_dist / 0.3))  # incrementing the time for the return to hub
    truck.mileage = total_mileage  # setting truck mileage to the round trip mileage
    truck.return_time = total_time  # setting truck time to round trip time
    return truck  # returning truck


algo(truckA, 8, 0)  # passing truck A into the algorithm with a start time of 8:00
algo(truckB, 8, 0)  # passing truck B into the algorithm with a start time of 8:00

# evaluating which truck returned first
if truckB.return_time.hour > truckA.return_time.hour:  # If truck A returned at a sooner hour than truck B
    first_truck_hour = truckA.return_time.hour  # Setting a variable to the hour TruckA returned
    first_truck_minute = truckA.return_time.minute  # Setting a variable to the min TruckA returned
elif truckB.return_time.hour == truckA.return_time.hour:  # else iff both trucks got back at the same hour
    if truckB.return_time.minute > truckA.return_time.minute:  # if truck A arrived at an earlier minute
        first_truck_hour = truckA.return_time.hour  # setting the var to the hour both trucks got back
        first_truck_minute = truckA.return_time.minute  # Setting a variable the TruckA minute of return
    else:  # Else truck B arrived at a sooner minute, so var gets set to truckB minute
        first_truck_minute = truckB.return_time.minute
else:  # Else truck B arrived sooner
    first_truck_hour = truckB.return_time.hour  # Set var hour to truckB returned hour
    first_truck_minute = truckB.return_time.minute  # Set var minute to truckB returned min


# Calls the algorithm for truckC, it will leave the hub whenever the first truck gets back to account for only 2 drivers
algo(truckC, first_truck_hour, first_truck_minute)

# Calculating the total mileage traveled by all trucks
total_miles = truckA.mileage + truckB.mileage + truckC.mileage

# Printing the entered time back out to the user
print("Entered Time: ", userTime)

# Printing the total mileage that will be traveled by all trucks given the algorithm
print("Total Mileage of trucks for the planned routes: ", total_miles, " miles")

# Loops through all the package Id numbers (1-40)
for x in range(1, 41):
    package = (myTable.lookup(x))  # getting the package object from the hashtable
    if userTime < datetime.time(8, 0, 0, ):  # evaluating whether the user entered a time before 08:00:00
        package.status = 'at the hub'  # if they did all packages are at the hub
    # if the entered time is before the departure time of the third truck, and the package is on the third truck
    elif int(package.id) in truckC_list_copy and userTime < datetime.time(first_truck_hour, first_truck_minute, 0):
        package.status = 'at the hub'  # sets package status to still be at the hub
    elif userTime >= package.timestamp:  # else if the user time is greater that the delivery time of the package
        package.status = 'Delivered at: ' + str(package.timestamp)  # outputs delivered message with timestamp
    else:
        package.status = 'en route'  # else the package is still in route (not at hub or delivered)

    print(package)  # Prints the list of all the packages
