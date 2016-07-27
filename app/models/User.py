from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def register_user(self, user_info):

        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        success = []
        error_free = True

# Validations-------------------------------------------------------------
        if not user_info['name']:
            errors.append('Name cannot be blank')
            error_free = False
        elif len(user_info['name']) < 3:
            errors.append('Name must be at least 2 characters long')
            error_free = False

        if not user_info['username']:
            errors.append('Username cannot be blank')
            error_free = False
        elif len(user_info['username']) < 3:
            errors.append('Username must be at least 2 characters long')
            error_free = False

        if not user_info['email']:
            errors.append('Email cannot be blank')
            error_free = False
        elif not EMAIL_REGEX.match(user_info['email']):
            errors.append('Email format must be valid!')
            error_free = False

        if not user_info['password']:
            errors.append('Password cannot be blank')
            error_free = False
        elif len(user_info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
            error_free = False

        if not user_info['confirm_password']:
            errors.append('Confirm password cannot be blank')
            error_free = False
        elif user_info['password'] != user_info['confirm_password']:
            errors.append('Password and confirmation must match!')
            error_free = False

# if there are errors, return errors...if not, enter user info into the database-------------------
        if error_free == False:
            return {"status": False, "errors": errors}
        else:

            get_user_query = "SELECT * FROM users WHERE users.email = %s ORDER BY id DESC LIMIT 1"
            user = self.db.query_db(get_user_query, [user_info['email']])

            if user:
                success.append('User already exists in the database!') #if user already exists in the database...
                return{"status": True, "success": success}

            else: #if user does not exist in the database...
                hashed_pw = self.bcrypt.generate_password_hash(user_info['password'])
                insert_user_query = "INSERT INTO users (name, username, email, password, updated_at, created_at) VALUES (%s, %s, %s, %s, NOW(), NOW())" #insert user
                data = [user_info['name'], user_info['username'], user_info['email'], hashed_pw]
                self.db.query_db(insert_user_query, data)
           
                get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1" #grab the last inserted user
                user = self.db.query_db(get_user_query)
                success.append('Successfully registered!')
                return { "status": True, "success": success }

    def login_user(self, user_info):

        # EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        error_free = True

# Validations-------------------------------------------------------------
        if not user_info['username']:
            errors.append('Email cannot be blank')
            error_free = False
        # elif not EMAIL_REGEX.match(user_info['email']):
        #     errors.append('Email format must be valid!')
        #     error_free = False
        if not user_info['password']:
            errors.append('Password cannot be blank')
            error_free = False
# Check--------------------------------------------------------------------
        if error_free == True :

            query = "SELECT * FROM users WHERE username = %s";
            data = [user_info['username']]
            matched_user = self.db.query_db(query, data)

            if matched_user:
                password = user_info['password']
                if self.bcrypt.check_password_hash(matched_user[0]['password'], password):
                    return { "status": True, "user": matched_user }
                else:
                    errors.append('User password does not match!')
                    return {"status": False, "errors": errors}
            else:
                errors.append('Username does not match!')
                return {"status": False, "errors": errors} 
        else:
            return {"status": False, "errors": errors}



