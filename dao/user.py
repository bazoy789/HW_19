from dao.model.user import User


class UserDAO:

    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create(self, data_user):
        user = User(**data_user)
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, data_user):
        user = self.get_one(data_user.get('id'))
        update_user = self.session.query(User).filter(User.id == user).update(data_user)
        self.session.commit()
        return update_user

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()
