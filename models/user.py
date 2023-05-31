class User:
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    @staticmethod
    def fetch_one_by_email(email, db):
        user_data = db.users.find_one({'email': email})
        if user_data:
            return User(user_data['email'], user_data['name'], user_data['password'])
        else:
            return None
