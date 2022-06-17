from app import User


async def test_app(client, db_session):
    db_session.add(User(username='aoe', email='test_user@mail.com', password='aoe'))
    await db_session.commit()
    resp = client.get('/')
    assert resp.status_code == 200, resp
    assert resp.json() == ['test_user@mail.com']
