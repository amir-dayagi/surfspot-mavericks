from .. import db
from ..common.models import User


def get_users(user, search_query):
    users = db.session.scalars(db.select(User).where((User.first_name+' '+User.last_name).contains(search_query))).all()
    return filter(lambda u: u.id != user.id, users)
    