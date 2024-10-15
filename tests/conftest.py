import pytest
from datetime import datetime, timedelta
from main.app import create_app
from main.models import db as _db, Client, Parking, ClientParking


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "parking: маркер для тестов «Заезд на парковку» и «Выезд с парковки»"
    )


@pytest.fixture
def app():
    app = create_app(test_config=True)
    app.config['TESTING'] = True
    with app.app_context():

        _db.create_all()
        client = Client(name="Петр", surname="Петров", credit_card="222222", car_number="43210")
        client_2 = Client(name="Иван", surname="Иванов", credit_card="111111", car_number="98765")
        parking = Parking(
            address="Minsk, Belarus, Nezavisimosty, 1", opened=True, count_places=20, count_available_places=19
        )
        time_in = datetime.now()
        client_parking = ClientParking(
            client_id=1, parking_id=1, time_in=time_in, time_out=(time_in + timedelta(hours=8))
        )
        _db.session.add_all([client, client_2, parking, client_parking])
        _db.session.commit()
        yield app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db



