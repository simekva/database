-- Group Members: Leo Fredsvik, Anette Abrahamsen, Simen Kvalø
CREATE TABLE railwayStation(
 ID INTEGER PRIMARY KEY NOT NULL,
 name TEXT NOT NULL UNIQUE,
 altitude INTEGER NOT NULL
);
CREATE TABLE trackSection(
 ID INTEGER PRIMARY KEY NOT NULL,
 name TEXT NOT NULL UNIQUE,
 direction TEXT NOT NULL,
 drivingEnergy TEXT NOT NULL,
 startsAtID INTEGER NOT NULL,
 endsAtID INTEGER NOT NULL,
 FOREIGN KEY(startsAtID) REFERENCES railwayStation(ID),
 FOREIGN KEY(endsAtID) REFERENCES railwayStation(ID)
);
CREATE TABLE subSection(
 ID INTEGER PRIMARY KEY NOT NULL,
 distance INTEGER NOT NULL,
 isDoubleTrack BOOLEAN NOT NULL,
 trackSectionID INTEGER NOT NULL,
 railwayStationOneID INTEGER NOT NULL,
 railwayStationTwoID INTEGER NOT NULL,
 FOREIGN KEY(trackSectionID) REFERENCES trackSection(ID),
 FOREIGN KEY(railwayStationOneID) REFERENCES railwayStation(ID),
 FOREIGN KEY(railwayStationTwoID) REFERENCES railwayStation(ID)
);
CREATE TABLE operator(
 ID INTEGER PRIMARY KEY NOT NULL,
 name TEXT NOT NULL UNIQUE
);
CREATE TABLE route(
 ID INTEGER PRIMARY KEY NOT NULL,
 direction BOOLEAN NOT NULL,
 trackSectionID INTEGER NOT NULL,
 operatorID INTEGER NOT NULL,
 startsAtID INTEGER NOT NULL,
 endsAtID INTEGER NOT NULL,
 FOREIGN KEY(trackSectionID) REFERENCES trackSection(ID),
 FOREIGN KEY(operatorID) REFERENCES operator(ID),
 FOREIGN KEY(startsAtID) REFERENCES railwayStation(ID),
 FOREIGN KEY(endsAtID) REFERENCES railwayStation(ID)
);
CREATE TABLE weekday(
 ID INTEGER PRIMARY KEY NOT NULL
);
CREATE TABLE routeRunsOnDay(
 routeID INTEGER NOT NULL,
 weekdayID INTEGER NOT NULL,
 PRIMARY KEY(routeID, weekdayID),
 FOREIGN KEY(routeID) REFERENCES route(ID),
 FOREIGN KEY(weekdayID) REFERENCES weekday(ID)
);
CREATE TABLE timeTable(
 arrivalTime TIME,
 departureTime TIME,
 routeID INTEGER NOT NULL,
 stationID INTEGER,
 PRIMARY KEY (routeID, stationID),
 FOREIGN KEY(routeID) REFERENCES route(ID),
 FOREIGN KEY(stationID) REFERENCES railwayStation(ID)
);
CREATE TABLE carType(
 name TEXT NOT NULL UNIQUE,
 operatorID INTEGER NOT NULL,
 FOREIGN KEY(operatorID) REFERENCES operator(ID)
);
CREATE TABLE sleepingCar(
 numberOfCompartments INTEGER NOT NULL,
 numberOfBedsPerCompartment INTEGER NOT NULL,
 carTypeName TEXT NOT NULL,
 FOREIGN KEY(carTypeName) REFERENCES carType(name)
);
CREATE TABLE chairCar(
 numberOfSeatRows INTEGER NOT NULL,
 numberOfSeatsPerRow INTEGER NOT NULL,
 carTypeName TEXT NOT NULL,
 FOREIGN KEY(carTypeName) REFERENCES carType(name)
);
CREATE TABLE carArrangement(
 number INTEGER NOT NULL,
 routeID INTEGER,
 carName TEXT NOT NULL,
 PRIMARY KEY(routeID, carName),
 FOREIGN KEY(routeID) REFERENCES route(ID),
 FOREIGN KEY(carName) REFERENCES carType(name)
);
CREATE TABLE trainOccurence(
 date DATE NOT NULL,
 routeID INTEGER NOT NULL,
 FOREIGN KEY(routeID) REFERENCES route(ID)
);
CREATE TABLE car (
 ID INTEGER NOT NULL,
 trainOccurenceRouteID INTEGER,
 PRIMARY KEY("ID"),
 FOREIGN KEY("trainOccurenceRouteID") REFERENCES "route"("ID")
);
CREATE TABLE seat(
 seatNumber INTEGER NOT NULL,
 carID INTEGER NOT NULL,
 FOREIGN KEY(carID) REFERENCES car(ID)
);
CREATE TABLE bed(
 bedNumber INTEGER NOT NULL UNIQUE,
 compartmentNumber INTEGER NOT NULL,
 carID INTEGER NOT NULL,
 FOREIGN KEY(carID) REFERENCES car(ID)
);
CREATE TABLE customer(
 customerNumber INTEGER PRIMARY KEY NOT NULL,
 name TEXT NOT NULL UNIQUE,
 email TEXT NOT NULL UNIQUE,
 phoneNumber TEXT NOT NULL UNIQUE
);
CREATE TABLE customerOrder(
 orderNumber INTEGER PRIMARY KEY NOT NULL,
 dateOfPurchase DATE NOT NULL,
 timeOfPurchase TIME NOT NULL,
 customerID INTEGER NOT NULL UNIQUE,
 FOREIGN KEY(customerID) REFERENCES customer(customerNumber)
);
CREATE TABLE chairTicket(
 ID INTEGER PRIMARY KEY NOT NULL,
 orderNumber INTEGER NOT NULL UNIQUE,
 seatID INTEGER NOT NULL,
 carID INTEGER NOT NULL,
 stationToID INTEGER NOT NULL,
 stationFRomID INTEGER NOT NULL,
 date TEXT NOT NULL,
 routeID INTEGER NOT NULL,
 FOREIGN KEY(seatID) REFERENCES seat(seatnumber),
 FOREIGN KEY(stationToID) REFERENCES railwayStation(ID),
 FOREIGN KEY(stationFromID) REFERENCES railwayStation(ID),
 FOREIGN KEY(orderNumber) REFERENCES customerOrder(orderNumber),
 FOREIGN KEY(carID) REFERENCES car(ID)
);
CREATE TABLE bedTicket(
 ID INTEGER PRIMARY KEY NOT NULL,
 orderNumber INTEGER NOT NULL,
 bedID INTEGER NOT NULL,
 carID INTEGER NOT NULL,
 stationToID INTEGER NOT NULL,
 stationFromID INTEGER NOT NULL,
 date TEXT NOT NULL,
 routeID INTEGER NOT NULL,
 FOREIGN KEY(bedID) REFERENCES bed(bedNumber),
 FOREIGN KEY(carID) REFERENCES car(ID),
 FOREIGN KEY(stationToID) REFERENCES railwayStation(ID),
 FOREIGN KEY(stationFromID) REFERENCES railwayStation(ID),
 FOREIGN KEY(orderNumber) REFERENCES customerOrder(orderNumber)
);