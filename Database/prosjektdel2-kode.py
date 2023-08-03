#DEL 1 FUNKSJONER:

import sqlite3
from datetime import datetime



    #Assume the station argument to a String with the name of the station, 
    #and weekday to be an integer 1-7 representing said weekday 
def find_train_routes(station, weekday):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT DISTINCT timetable.routeID \
                     FROM railwayStation INNER JOIN timeTable on stationID = railwayStation.ID \
                     WHERE railwayStation.name='{station}' AND timeTable.routeID IN \
                         (SELECT routeID FROM routeRunsOnDay WHERE routeRunsOnDay.weekdayID = {weekday})")
    result = cursor.fetchall()
    connection.close()
    return result


def register_customer(name, email, phone_number):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
 
    cursor.execute(f"INSERT INTO customer (name, email, phoneNumber) \
                     VALUES ('{name}', '{email}', '{phone_number}')")
    connection.commit()
    connection.close()

def search_for_train_routes(start, end, date):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    #Finding the ID of the specified railway stations
    cursor.execute(f"SELECT id FROM railwayStation WHERE name = '{start}'")
    startID = cursor.fetchone()[0]
    cursor.execute(f"SELECT id FROM railwayStation WHERE name = '{end}'")
    endID = cursor.fetchone()[0]
    #Fetch timetable rows with routes that go there, as well as train occurrences for these routes, join on routeID
    #Filter out all rows where starting station ID and ending station ID match
    #Filter out all rows where the date is the desired one, or the day after
    #Filter out all rows that depart from start before they arrive at end, to make sure that the route is going in the desired direction
        #Does not work for trains that go past midnight
    #Ordered such that the train departing first will show first in the results
    cursor.execute(f"SELECT TTStart.arrivalTime, TTStart.departureTime, TTStart.stationID, trainOccurence.routeID, trainOccurence.date, TTEnd.arrivalTime, TTEnd.departureTime, TTEnd.stationID \
                     FROM timeTable AS TTStart INNER JOIN trainOccurence ON TTStart.routeID = trainOccurence.routeID INNER JOIN timeTable AS TTEnd ON TTEnd.routeID = trainOccurence.routeID INNER JOIN route ON TTEnd.routeID = route.ID\
                     WHERE (TTStart.stationID = '{startID}' AND TTEnd.stationID = '{endID}') \
                     AND ((date = '{date}') OR (date = (SELECT DATE('{date}', '+1 days'))))\
                     AND ((TTStart.stationID < TTEnd.stationID AND route.direction = 'main') OR (TTStart.stationID > TTEnd.stationID AND route.direction = 'reverse')) \
                     ORDER BY trainOccurence.date ASC, TTStart.departureTime ASC")
    result = cursor.fetchall()
    connection.close()
    return result

def find_customerID(email):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT customerNumber FROM customer WHERE email = '{email}'") 
    result = cursor.fetchall()
    connection.close()
    return result

def search_for_route(routeID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT ID\
                    FROM route\
                    WHERE (ID = '{routeID}')") 
    result = cursor.fetchall()
    connection.close()
    return result

def find_trainOccurence(routeID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT date\
                    FROM trainOccurence\
                    WHERE (routeID = '{routeID}')") 
    result = cursor.fetchall()
    connection.close()
    return result


def find_route_direction(routeID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT direction\
                     FROM route\
                     WHERE (ID = '{routeID}')")
    result = cursor.fetchall()
    connection.close()
    return result

def find_timetable_for_route(routeID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT t.arrivalTime, t.departureTime, r.name, r.ID\
                     FROM timeTable AS t INNER JOIN railwayStation AS r ON t.stationID = r.ID INNER JOIN route ON t.routeID = route.ID\
                     WHERE (t.routeID = '{routeID}')")
    result = cursor.fetchall()
    
    connection.close()
    return result

def find_timetable_for_reverse_route(routeID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT t.arrivalTime, t.departureTime, r.name, r.ID\
                     FROM timeTable AS t INNER JOIN railwayStation AS r ON t.stationID = r.ID INNER JOIN route ON t.routeID = route.ID\
                     WHERE (t.routeID = '{routeID}')\
                        ORDER BY t.stationID DESC")
    result = cursor.fetchall()
    
    connection.close()
    return result
    

def get_carArrangement(routeID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT carName FROM carArrangement WHERE routeID = '{routeID}'") 
    result = cursor.fetchall()
    connection.close()
    return result

def get_stationID(stationName):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT ID FROM railwayStation WHERE name = '{stationName}'") 
    result = cursor.fetchall()
    connection.close()
    return result

def get_new_orderNo():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(orderNumber) FROM customerOrder")
    highest_orderNo = cursor.fetchone()
    connection.close()
    if (highest_orderNo[0] is None):
        orderNo = 1
    else:
        orderNo =  (highest_orderNo[0]) + 1
    result = orderNo
    return result

def add_to_customerOrder(orderNo, dateOfPurchase, timeOfPurchase, customerID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO customerOrder (orderNumber, dateOfPurchase, timeOfPurchase, customerID) \
                     VALUES ('{orderNo}', '{dateOfPurchase}', '{timeOfPurchase}', '{customerID}')")
    connection.commit()
    connection.close()

    

def find_available_chairs(route, date):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT seat.seatNumber, car.ID, trainOccurence.date, trainOccurence.routeID \
                     FROM seat INNER JOIN car ON seat.carID = car.ID INNER JOIN trainOccurence ON trainOccurence.routeID = car.trainOccurenceRouteID \
                     WHERE trainOccurence.routeID = '{route}' AND trainOccurence.date = '{date}'\
                     EXCEPT \
                     SELECT chairTicket.seatID, chairTicket.carID, chairTicket.date, chairTicket.routeID \
                     FROM chairTicket")
    result = cursor.fetchall()
    connection.close()
    return result


def purchase_chairTicket(orderNo, seat, car, startStation, endStation, date, routeID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    #Finding the ID of the specified railway stations
    cursor.execute(f"SELECT id FROM railwayStation WHERE name = '{startStation}'")
    startID = cursor.fetchone()[0]
    cursor.execute(f"SELECT id FROM railwayStation WHERE name = '{endStation}'")
    endID = cursor.fetchone()[0]
    
    cursor.execute(f"INSERT INTO chairTicket (orderNumber, seatID, carID, stationToID, StationFromID, date, routeID) \
                     VALUES ('{orderNo}', '{seat}', '{car}', '{endID}', '{startID}', '{date}', '{routeID}')")
    connection.commit()
    connection.close()


    
def find_available_beds(route, date):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT bed.bedNumber, car.ID, trainOccurence.date, trainOccurence.routeID \
                     FROM bed INNER JOIN car ON bed.carID = car.ID INNER JOIN trainOccurence ON trainOccurence.routeID = car.trainOccurenceRouteID \
                     WHERE trainOccurence.routeID = '{route}' AND trainOccurence.date = '{date}' \
                     EXCEPT \
                     SELECT bedTicket.bedID, bedTicket.carID, bedTicket.date, bedTicket.routeID \
                     FROM bedTicket")
    result = cursor.fetchall()
    connection.close()
    return result


def purchase_bedTicket(orderNo, bed, car, startStation, endStation, date, routeID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    #Finding the ID of the specified railway stations
    cursor.execute(f"SELECT id FROM railwayStation WHERE name = '{startStation}'")
    startID = cursor.fetchone()[0]
    cursor.execute(f"SELECT id FROM railwayStation WHERE name = '{endStation}'")
    endID = cursor.fetchone()[0]
    
    cursor.execute(f"INSERT INTO bedTicket (orderNumber, bedID, carID, stationToID, StationFromID, date, routeID) \
                     VALUES ('{orderNo}', '{bed}', '{car}', '{endID}', '{startID}', '{date}', '{routeID}')")
    connection.commit()
    connection.close()
    
def previous_chair_purchases(customerID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT c.dateOfPurchase, c.timeOfPurchase, ch.stationFromID, ch.stationToID, ch.date, ch.seatID, ch.carID, ch.routeID\
                     FROM customerOrder AS c INNER JOIN chairTicket AS ch ON c.orderNumber = ch.orderNumber")
    result = cursor.fetchall()
    connection.close()
    return result

def previous_bed_purchases(customerID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT c.dateOfPurchase, c.timeOfPurchase, b.stationFromID, b.stationToID, b.date, b.bedID, b.carID, b.routeID\
                     FROM customerOrder AS c INNER JOIN bedTicket AS b ON c.orderNumber = b.orderNumber")
    result = cursor.fetchall()
    connection.close()
    return result

def get_stationName(stationID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT name FROM railwayStation WHERE ID = '{stationID}'") 
    result = cursor.fetchall()
    connection.close()
    return result

def get_departuretime(stationID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT DISTINCT departureTime FROM timeTable INNER JOIN chairTicket ON timeTable.routeID = chairTicket.routeID WHERE stationID = '{stationID}'") 
    result = cursor.fetchall()
    connection.close()
    return result






# DEL 2 UI:
exit = False
while (not(exit)):
    number = int(input(
       """1 - Find train routes that stop on a given station, on a given weekday 
        \n2 - Search for train routes going between a starting station and an ending station based on date and time
        \n3 - Register in the customer registry
        \n4 - Find and purchase available tickets for a desired train route
        \n5 - Info about previous purchases
        \n6 - Exit
        \n"""))
    
    if number == 1:
        station = input("Enter the name of the desired station:\n")
        day = input("Enter desired day of the week(1-7):\n")
        routes = find_train_routes(station, day)
        week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        if not routes:
            print("There are no routes to this station on this weekday")
        else:
            print(f"The following routes stop at this station on {week[int(day)+1]}:")
            for route in routes:
                print(route[0])
    
    elif number == 2:
        start = input("Enter start station:\n")
        end = input("Enter end station:\n")
        date = input("Enter the date of your journey:\n")
        routes = search_for_train_routes(start, end, date)
        if not routes:
            print("There are no routes going between these stations on the specified date")
        else:
            print("Departure  Arrival  Date         Route:")
            for route in routes:
                print(f"{route[1]}      {route[5]}    {route[4]}    {route[3]}")
                
    elif number == 3:
        name = input("Enter name:\n")
        email = input("Enter email:\n")
        pnr = input("Enter phone number:\n")
        register_customer(name, email, pnr)
        print("Customer registered.")
    
    elif number == 4:
        #Checks that the customer is already in the customer registry
        email = input("What is your email?\n")
        customer = find_customerID(email)
        if not customer:
            print("Please register as a customer before attempting to purchase tickets.")
        else:
            customerID = customer[0][0]
            #Checks that the requested route is operated
            routeID = input("Which route would you like to go on?\n")
            route = search_for_route(routeID)
            if not route:
                print("Route not operating.")
            else:
                #Presents available dates, and verifies inputs
                trainOccurence = find_trainOccurence(routeID)
                print(trainOccurence)
                date = input("From the dates shown, which date do you want to go on?\n")
                validDate = False 
                for i in trainOccurence:
                    if (date == i[0]):
                        validDate = True
                        
                #Presents available stations, and verifies inputs
                if (validDate):
                    reverse = False
                    if (find_route_direction(routeID)[0][0] == 'reverse'):
                        timetable = find_timetable_for_reverse_route(routeID)
                        reverse = True
                    else:
                        timetable = find_timetable_for_route(routeID)
                    print(timetable)
                    startStation = input("Which station do you want to go from?\n")
                    validStart = False
                    
                    for i in timetable:
                        if (startStation == i[2]):
                            startID = i[3]
                            validStart = True
                    
                    if (validStart):
                        endStation = input("Which station do you want to go to?\n")
                        validEnd = False
                     
                        for i in timetable:
                            if (reverse):
                                if (endStation == i[2] and endStation != startStation and startID > i[3]):
                                    validEnd = True
                            else:    
                                if (endStation == i[2] and endStation != startStation and startID < i[3]):
                                    validEnd = True
                        
                        if (validEnd):
                            carArr = get_carArrangement(routeID)
                            
                            validBed = False
                            for i in carArr:
                                if("SJ-sleeping car-1" == i[0]):
                                    validBed = True
                            
                            numSeat = 0
                            
                            if (validBed):
                                bed = input("Would you like to purchase any bed tickets? (y/n)\n")
                                if (bed == 'y'):
                                    numBed = input("How many bed tickets would you like?\n")
                                    available_beds = find_available_beds(routeID, date)
                                    if len(available_beds) < int(numBed):
                                        print(f"We only have {len(available_beds)} beds available for this train")
                                    else:
                                        orderNo = get_new_orderNo()
                                            
                                        now = datetime.now()
                                        dateOfPurchase = now.strftime("%d/%m/%Y")
                                        timeOfPurchase = now.strftime("%H:%M:%S")
                                            
                                        add_to_customerOrder(orderNo, dateOfPurchase, timeOfPurchase, customerID)
                                        
                                        for i in range(int(numBed)):
                                            availableBedID = find_available_beds(routeID, date)[0][0]
                                            availableCarID = find_available_beds(routeID, date)[0][1]
                                        
                                            purchase_bedTicket(orderNo, availableBedID, availableCarID, startStation, endStation, date, routeID)
                                        
                                        
                                        print(numBed+" bed ticket(s) are succesfully purchased")
                                        
                                else:
                                    numSeat = input("How many chair tickets would you like?\n")
                                    
                            else:
                                numSeat = input("How many chair tickets would you like?\n")
                            
                            if (int(numSeat) > 0):
                                available_seats = find_available_chairs(routeID, date)
                                if len(available_seats) < int(numSeat):
                                        print(f"We only have {len(available_seats)} seats available for this train")
                                else:
                                    orderNo = get_new_orderNo()
                                                    
                                    now = datetime.now()
                                    dateOfPurchase = now.strftime("%d/%m/%Y")
                                    timeOfPurchase = now.strftime("%H:%M:%S")
                                                        
                                    add_to_customerOrder(orderNo, dateOfPurchase, timeOfPurchase, customerID)
                                                    
                                    for i in range(int(numSeat)):
                                        availableSeatID = find_available_chairs(routeID, date)[0][0]
                                        availableCarID = find_available_chairs(routeID, date)[0][1]
                                                    
                                        purchase_chairTicket(orderNo, availableSeatID, availableCarID, startStation, endStation, date, routeID)
                                            
                                    print(numSeat+" chair ticket(s) are succesfully purchased")
                                
                      
                        
                        else:
                            print("Station not in timetable\n")
                    else:
                        print("Station not in timetable\n")
                else:
                    print("Date not available\n")


    elif number == 5:
        
        email = input("What is your email?\n")
        customers = find_customerID(email)
        if not customers:
            print("Your email is not in our register.")
        else:
            print(" ")
            customerID = customers[0][0]
            chair_purchases = previous_chair_purchases(customerID)
            
            for i in chair_purchases:
                print("Date of purchase: "+ i[0])
                print("Time of purchase: "+ i[1])
                
                start = get_stationName(i[2])[0][0] 
                print("From station: "+ start)
                
                end = get_stationName(i[3])[0][0]
                print("To station: "+ end)
                
                departureTime = get_departuretime(i[2])[0][0]
                print("Date of departure: "+i[4]+" Time of departure: "+departureTime)
                print("Seatnumber: "+str(i[5])+" Carnumber: "+str(i[6])+"\n")
                
            bed_purchases = previous_bed_purchases(customerID)
            for i in bed_purchases:
                print("Date of purchase: "+ i[0])
                print("Time of purchase: "+ i[1])
                
                start = get_stationName(i[2])[0][0] 
                print("From station: "+ start)
                
                end = get_stationName(i[3])[0][0]
                print("To station: "+ end)
                
                departureTime = get_departuretime(i[2])[0][0]
                print("Date of departure: "+i[4]+" Time of departure: "+departureTime)
                print("Bednumber: "+str(i[5])+" Carnumber: "+str(i[6])+"\n")
            
                
  
    elif number == 6:
        break
    if (input("Continue? (y/n):\n") == "n"):
        break