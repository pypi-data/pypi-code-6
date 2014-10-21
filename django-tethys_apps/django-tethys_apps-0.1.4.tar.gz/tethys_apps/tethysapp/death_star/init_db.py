from .model import Base, engine, CrewMember, SessionMaker


def init_example_db(first_time):
    """
    An example persistent store initializer function
    """
    # Create tables
    Base.metadata.create_all(engine)

    if first_time:
        # Make session
        session = SessionMaker()

        # Create some crew members
        darth = CrewMember(name='Darth Vadar', age=54)
        palpatine = CrewMember(name='Emperor Palpatine', age=89)

        # Add them to the session and commit
        session.add(darth)
        session.add(palpatine)
        session.commit()