INSERT INTO railwayStation(ID, name, altitude) VALUES(1, "Trondheim", 5.1),(2, "Steinkjer", 3.6),
(3, "Mosjøen", 6.8) ,(4, "Mo i Rana", 3.5),(5, "Fauske", 34) , (6, "Bodø", 4.1);

INSERT INTO trackSection(ID, name, direction, drivingEnergy, startsAtID, endsAtID) 
VALUES(1, "Nordlandsbanen", "North", "Electric", 1, 6);

INSERT INTO subSection(ID, distance, isDoubleTrack, trackSectionID, railwayStationOneID, railwayStationTwoID) 
VALUES(1, 120, true, 1, 1, 2), (2, 250, false, 1, 2, 3), (3, 90, false, 1, 3, 4), 
(4, 170, false, 1, 4, 5), (5, 60, false, 1, 5, 6);


INSERT INTO operator(ID, name) VALUES(1, "SJ");

INSERT INTO route(ID, direction, trackSectionID, operatorID, startsAtID, endsAtID) 
VALUES(1, "main", 1, 1, 1, 6), (2, "main", 1, 1, 1, 6), (3, "reverse", 1, 1, 4, 1);

INSERT INTO weekday(ID) VALUES(1),(2),(3),(4),(5),(6),(7);

INSERT INTO routeRunsOnDay(routeID, weekdayID) VALUES(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), 
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5);

INSERT INTO carType(name, operatorID) VALUES("SJ-chair car-1", 1), ("SJ-sleeping car-1", 1);

INSERT INTO chairCar(numberOfSeatRows, numberOfSeatsPerRow, carTypeName) VALUES(3, 4, "SJ-sleeping car-1");

INSERT INTO sleepingCar(numberOfCompartments, numberOfBedsPerCompartment, carTypeName) VALUES(4, 2, "SJ-sleeping car-1");

INSERT INTO carArrangement(number, routeID, carName) VALUES(2, 1, "SJ-chair car-1"), (1, 2, "SJ-chair car-1"), 
(1, 2, "SJ-sleeping car-1"), (1, 3, "SJ-chair car-1");

INSERT INTO timeTable(arrivalTime, departureTime, routeID, stationID) VALUES(NULL, "07:49", 1, 1), ("09:48", "09:51", 1, 2), ("13:17", "13:20", 1, 3), 
("14:28", "14:31", 1, 4), ("16:46", "16:49", 1, 5), ("17:34", NULL, 1, 6), (NULL, "23:05", 2, 1), ("00:54", "00:57", 2, 2), ("04:38", "04:41", 2, 3), 
("05:52", "05:55", 2, 4), ("08:16", "08:19", 2, 5), ("09:05", NULL, 2, 6), (NULL, "08:11", 3, 4), ("09:11", "09:14", 3, 3), ("12:28", "12:31", 3, 2), 
("14:10", NULL, 3, 1);

INSERT INTO trainOccurence(date, routeID) VALUES("2023-04-03", 1), ("2023-04-03", 2), 
("2023-04-03", 3), ("2023-04-04", 1), ("2023-04-04", 2), ("2023-04-04", 3);

INSERT INTO car(ID, trainOccurenceRouteID) VALUES(1, 1), (2, 1), (3, 2), (4, 2), (5, 3);

INSERT INTO seat(seatNumber, carID) VALUES(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), 
(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), 
(7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 5);

INSERT INTO bed(bedNumber, compartmentNumber, carID) VALUES(1, 1, 4), (2, 1, 4), (3, 2, 4), (4, 2, 4), (5, 3, 4), (6, 3, 4), (7, 4, 4), (8, 4, 4);