from system.core.model import Model
import re
import time

class Trip(Model):

    def __init__(self):
        super(Trip, self).__init__()

    def add_process(self, trip_info, user_id):
        today_date = time.strftime("%Y-%m-%d")
        error_free = True
        errors = []
        if not trip_info['destination']: 
            errors.append('Destination must not be blank')
            error_free = False
        if not trip_info['plan']:
            errors.append('Description must not be blank')
            error_free = False
        if not trip_info['start_date']:
            errors.append('Travel date from must not be blank')
            error_free = False
        if not trip_info['end_date']:
            errors.append('Travel date to must not be blank')
            error_free = False
        if trip_info['start_date'] <= today_date or trip_info['end_date'] <= today_date:
            errors.append('Travel dates must be future-dated')
            error_free = False
        elif trip_info['start_date'] > trip_info['end_date']:
            errors.append('Travel date to should not be before travel date from')
            error_free = False

        if error_free == True: 
            query = "INSERT INTO trips (added_by_id, destination, start_date, end_date, plan, updated_at, created_at) VALUES (%s, %s, %s, %s, %s, NOW(), NOW())"
            data = [user_id, trip_info['destination'], trip_info['start_date'], trip_info['end_date'], trip_info['plan']]
            self.db.query_db(query, data)

            query = "SELECT trips.id FROM trips ORDER BY id DESC LIMIT 1"
            trip_id = self.db.query_db(query)

            query = "INSERT INTO users_has_trips (user_id, trip_id, updated_at, created_at) VALUES (%s, %s, NOW(), NOW())"
            data = [user_id, trip_id[0]['id']]
            self.db.query_db(query, data)
            return {"status": True}
        else:
            return {"status": False, "errors": errors}


    def select_my_trips(self, user_id):
    	query = "SELECT destination, start_date, end_date, plan, trips.id as trip_id FROM trips JOIN users_has_trips ON trips.id = users_has_trips.trip_id JOIN users ON users_has_trips.user_id = users.id WHERE users.id = %s"
    	data = [user_id]
    	return self.db.query_db(query, data)

    def select_other_trips(self, user_id):

    	# query = "SELECT destination, start_date, end_date, trips.id as trip_id, username FROM trips JOIN users ON trips.added_by_id = users.id JOIN users_has_trips ON trips.id = users_has_trips.trip_id WHERE users_has_trips.user_id NOT IN (%s)"
        query = "SELECT distinct destination, username, start_date, end_date, trips.id as trip_id, username FROM trips LEFT JOIN users ON trips.added_by_id = users.id LEFT JOIN users_has_trips ON users_has_trips.trip_id = trips.id WHERE trips.id NOT IN (SELECT trip_id FROM users_has_trips WHERE user_id = %s) AND added_by_id NOT IN (%s)"
    	data = [user_id, user_id]
    	return self.db.query_db(query, data)

    def join_trip(self, trip_id, user_id):
        query = "INSERT INTO users_has_trips (user_id, trip_id, updated_at, created_at) VALUES (%s, %s, NOW(), NOW())"
        data  = [user_id, trip_id]
        return self.db.query_db(query, data)

    def select_trip_info(self, trip_id):
        query = "SELECT added_by_id FROM trips WHERE trips.id = (%s)"
        added_by_id = self.db.query_db(query, [trip_id])

        query = "SELECT username, destination, plan, start_date, end_date FROM trips JOIN users ON trips.added_by_id = users.id WHERE trips.id = (%s)"
        data = [trip_id]
        trip_info = self.db.query_db(query, data)

        query = "SELECT username FROM users JOIN users_has_trips ON users.id = users_has_trips.user_id WHERE users.id NOT IN (%s) AND users_has_trips.trip_id = (%s)"
        data = [added_by_id[0]['added_by_id'], trip_id]
        others= self.db.query_db(query, data)

        return {"trip_info": trip_info, "others": others}


