from datetime import datetime

from .. import db
from .models import Group, Session, session_user, Message
from ..common.models import User, group_user, UserLocation, Spot
from ..common.utils import JsonException

def get_groups(user):
    return user.groups

def create_group(user, group_request):
    # assert that json includes all required fields
    if 'name' not in group_request:
        raise JsonException('Missing required fields!', 400)

    new_group = Group(name = group_request['name'])
    user.groups.append(new_group)
    db.session.add(new_group)
    db.session.commit()
    db.session.refresh(new_group)
    return new_group

def get_group_users(user, group_id):
    for group in user.groups:
        if group.id == group_id:
            return group.users
    
    raise JsonException('User is not in given group!', 400)

def add_to_group(user, group_id, added_user_id):
    # assert that added user exsits
    added_user = db.session.scalar(db.select(User).where(User.id == added_user_id))
    if not added_user:
        raise JsonException('The user that you are trying to add does not exist!', 400)
    
    # assert that added user is not already in group
    if group_id in [group.id for group in added_user.groups]:
        raise JsonException('The user that you are trying to add is already in the group!', 400)

    # assert that requesting user is in group
    group = None
    for group_ in user.groups:
        if group_.id == group_id:
            group = group_
            break
    if not group:
        raise JsonException('User is not in given group!', 400)
    
    group.users.append(added_user)
    db.session.commit()

def start_session(user, group_id, session_request):
    # assert that json includes all required fields
    if not all(key in session_request for key in ('start_datetime', 'spot_id')):
        raise JsonException('Missing required fields!', 400)
    
    # assert that user in group
    group = None
    for group_ in user.groups:
        if group_.id == group_id:
            group = group_
            break
    if not group:
        raise JsonException('User is not in given group!', 400)

    # assert that spot exists
    if not db.session.scalar(db.select(Spot).where(Spot.id == int(session_request['spot_id']))):
        raise JsonException('Given spot does not exist!', 400)

    # assert that group doesn't already have sesion
    if group.session:
        raise JsonException('Group already has an active session', 400)

    # assert that time is valid format and after right now
    try:
        start_datetime = datetime.fromisoformat(session_request['start_datetime'])
    except:
        raise JsonException('Invliad start datetime format', 400)

    new_session = Session(
                          start_datetime = start_datetime,
                          spot_id = int(session_request['spot_id'])
                         )
    group.session = new_session
    db.session.add(new_session)
    db.session.commit()
    db.session.refresh(new_session)

    db.session.execute(
        session_user.insert().values(user_id = user.id,
                                     group_id = group_id,
                                     session_id = new_session.id)
    )
    db.session.commit()
    return new_session

def join_session(user, group_id):
    # assert that user is in group
    group = None
    for group_ in user.groups:
        if group_.id == group_id:
            group = group_
            break
    if not group:
        raise JsonException('User is not in given group!', 400)

    # assert that group has active session
    session = group.session
    if not session:
        raise JsonException('Cannot join session in group that doesnt have an active session!', 400)

    # assert that user is not in active_session already
    if db.session.scalar(
                         db.select(session_user).where((session_user.c.user_id == user.id) &
                                                       (session_user.c.group_id == group.id) &
                                                       (session_user.c.session_id == session.id))
                        ):
        raise JsonException('User is already in session!', 400)

    db.session.execute(
        session_user.insert().values(user_id = user.id,
                                     group_id = group.id,
                                     session_id = session.id)
    )
    db.session.commit()

def leave_session(user, group_id):
    # assert that user is in group
    group = None
    for group_ in user.groups:
        if group_.id == group_id:
            group = group_
            break
    if not group:
        raise JsonException('User is not in given group!', 400)

    # assert that group has active session
    session = group.session
    if not session:
        raise JsonException('Cannot leave session in group that doesnt have an active session!', 400)
    
    res = db.session.execute(db.delete(session_user).where((session_user.c.user_id == user.id) &
                                                           (session_user.c.group_id == group.id) &
                                                           (session_user.c.session_id == session.id)))
    if res.rowcount != 1:
        raise JsonException('Cannot leave session that user doesnt participate in!', 400)
    db.session.commit()
    
def get_session_users(user, group_id):
    # assert that user is in group
    group = None
    for group_ in user.groups:
        if group_.id == group_id:
            group = group_
            break
    if not group:
        raise JsonException('User is not in given group!', 400)

    # assert that group has active session
    if not group.session:
        raise JsonException('Cannot access session users when there is no active session!', 400)

    session_users = db.select(session_user.c.user_id).where(session_user.c.group_id == group_id)

    return db.session.scalars(db.select(User)
                                .where(User.id.in_(session_users))).all()

def get_latest_messages(user, group_id, limit):
    # assert that user is in group
    group = None
    for group_ in user.groups:
        if group_.id == group_id:
            group = group_
            break
    if not group:
        raise JsonException('User is not in given group!', 400)

    return db.session.scalars(db.select(Message)
                                .where(Message.group_id == group_id)
                                .order_by(Message.send_datetime.desc())).all()[:limit]


def send_message(user, group_id, message_request):
    # assert that json includes all required fields
    if 'context' not in message_request:
        raise JsonException('Missing required fields!', 400)
    
    # assert that user in group
    if group_id not in [group.id for group in user.groups]:
        raise JsonException('The user is not in given group!', 400)

    new_message = Message(
                          user_id = user.id,
                          group_id = group_id,
                          context = message_request['context'],
                         )
    db.session.add(new_message)
    db.session.commit()
    db.session.refresh(new_message)
    return new_message