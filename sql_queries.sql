select * from users;
select * from users_has_trips;
select * from trips;

SELECT destination, start_date, end_date, plan 
FROM trips 
JOIN users_has_trips ON trips.id = users_has_trips.trip_id
JOIN users ON users_has_trips.user_id = users.id
WHERE users.id = 1;

SELECT destination, start_date, end_date, trips.id as trip_id, username 
FROM trips JOIN users_has_trips ON trips.id = users_has_trips.trip_id 
JOIN users ON trips.added_by_id = users.id 
WHERE users_has_trips.user_id NOT IN (1);

SELECT destination, start_date, end_date, trips.id as trip_id, username 
FROM trips JOIN users_has_trips ON trips.id = users_has_trips.trip_id 
JOIN users ON trips.added_by_id = users.id 
WHERE users_has_trips.user_id NOT IN (1) AND users_has_trips.trip_id NOT IN (3);

SELECT destination, start_date, end_date, trips.id as trip_id, username 
FROM trips JOIN users ON trips.added_by_id = users.id 
JOIN users_has_trips ON trips.id = users_has_trips.trip_id 
WHERE users_has_trips.user_id 
NOT IN (2);

SELECT destination, username FROM trips 
LEFT JOIN users ON trips.added_by_id = users.id
LEFT JOIN users_has_trips ON users_has_trips.trip_id = trips.id
WHERE trips.id NOT IN (SELECT trip_id FROM users_has_trips WHERE user_id = 2) AND added_by_id NOT IN (2);


