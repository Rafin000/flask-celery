from project import db
from project.tdd.factories import MemberFactory


def test_model(db):
    member = MemberFactory.build()

    db.session.add(member)
    db.session.commit()

    assert member.id