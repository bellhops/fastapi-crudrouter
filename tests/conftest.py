import pytest
from fastapi.testclient import TestClient

from .implementations import *

implementations = [
    memory_implementation,
    sqlalchemy_implementation,
    databases_implementation,
    tortoise_implementation
]


@pytest.fixture(params=implementations)
def client(request):
    impl = request.param

    if impl is tortoise_implementation:
        from tortoise.contrib.test import initializer, finalizer

        initializer(["tests.implementations.tortoise"])
        with TestClient(impl()) as c:
            yield c
        finalizer()
    else:
        yield TestClient(impl())


@pytest.fixture(params=[sqlalchemy_implementation_custom_ids, databases_implementation_custom_ids])
def custom_id_client(request):

    yield TestClient(request.param())


@pytest.fixture
def overloaded_client():

    yield TestClient(overloaded_app())




