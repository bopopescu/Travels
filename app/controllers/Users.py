from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Trip')

    def index(self):
        return self.load_view('index.html')

    def join(self, trip_id):
        self.models['Trip'].join_trip(trip_id, session['user_id'])
        return redirect('display_success')

    def display_trip(self, trip_id):
        info = self.models['Trip'].select_trip_info(trip_id)
        trip_info = info['trip_info']
        others = info['others']
        return self.load_view('trip_profile.html', trip_info=trip_info, others=others)

    def logout(self):
        session.clear()
        return redirect('/')
        
    def add_process(self):
        trip_info = {
            "destination":  request.form['destination'],
            "plan": request.form['plan'],
            "start_date": request.form['start_date'],
            "end_date": request.form['end_date']
        }
        user_status = self.models['Trip'].add_process(trip_info, session['user_id'])
        if user_status['status'] == True: 
            return redirect('/display_success')
        else:
            for message in user_status['errors']:
                flash(message, 'errors')
            return redirect('/add_a_trip')

    def add_a_trip(self):
        return self.load_view('add_a_trip.html')

    def display_success(self):
        user_id = session['user_id']
        username = session['username']
        my_trips = self.models['Trip'].select_my_trips(session['user_id'])
        other_trips = self.models['Trip'].select_other_trips(session['user_id'])
        print my_trips
        return self.load_view('success.html', user_id=user_id, username=username, my_trips=my_trips, other_trips=other_trips)

    def register_user(self):

        user_info = {
            "name" : request.form['name'],
            "username" : request.form['username'],
            "email" : request.form['email'],
            "password" : request.form['password'],
            "confirm_password" : request.form['confirm_password'],
        }

        user_status = self.models['User'].register_user(user_info) # directs to validations + database

        if user_status['status'] == True: #user either exists in the database or is inserted
            for message in user_status['success']:
                flash(message, 'success')
            return redirect('/')
        else: #validations errors 
            for message in user_status['errors']:
                flash(message, 'errors')
            return redirect('/')

    def login_user(self):

        user_info = {
            "username" : request.form['username'],
            "password" : request.form['password']
        }

        user_status = self.models['User'].login_user(user_info) # directs to validations + database 

        if user_status['status'] == True:

            session['user_id'] = user_status['user'][0]['id']
            session['username'] = user_status['user'][0]['username']

            return redirect('/display_success')
        else:

            for message in user_status['errors']:
                flash(message, 'errors')

            return redirect('/')

