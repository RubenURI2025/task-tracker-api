import os
import tempfile
import pytest
import app as app_module

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app_module.DB_NAME = db_path
    app_module.init_db()
    app_module.app.config["TESTING"] = True

    yield app_module.app

    os.close(db_fd)
    os.unlink(db_path)
