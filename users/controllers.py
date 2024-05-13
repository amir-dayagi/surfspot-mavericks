from .. import db
from ..common.models import User


def get_users(search_query):
    return db.session.scalars(db.select(User).where((User.first_name+' '+User.last_name).contains(search_query))).all()
    