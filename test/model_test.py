import pytest
from app import app
from app import index, predict
import requests
from flask import url_for
#import app


@pytest.fixture
def client():
    return app.test_client()


def test_index(client):
    # we check when a client sends a get request to "/" is should be succesful
    resp = client.get('/')
    assert resp.status_code == 200
    # when a client sends a post request to "/" it should show method not allowed
    resp2 = client.post('/')
    assert resp2.status_code == 405


def test_predict(client):
    # if client makes a get request to the /predict route, it should redict the page to /Predict/
    resp = client.get('/predict')
    assert resp.status_code == 308

    # if client makes a get request to the /predict/ route, it should return status okay
    resp2 = client.get('/predict/')
    assert resp2.status_code == 200

    # if client makes a post request to the /predict/ route,it should return status okay
    resp3 = client.post('/predict/')
    assert resp3.status_code == 200

    # if client makes a post request to the /predict route,it should  redirict
    resp4 = client.post('/predict')
    assert resp4.status_code == 308
