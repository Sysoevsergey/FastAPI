# mypy: disable-error-code="attr-defined"
import os

from alembic.command import downgrade, upgrade
from alembic.config import Config
from api_client import ApiClient
from config import API_URL
from pytest import fixture


@fixture()
def api_client():
    return ApiClient(API_URL)


@fixture(autouse=True)
def setup_db():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(current_dir, "..", "app"))
    config_path = "alembic.ini"
    downgrade(Config(config_path), "base")
    upgrade(Config(config_path), "head")
    os.chdir(current_dir)
