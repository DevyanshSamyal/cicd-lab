
import toss.app as toss_app

import pytest


@pytest.fixture
def client():
    toss_app.app.config["TESTING"] = True

    with toss_app.app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200


def test_rules(client):
    response = client.get("/rules")

    assert response.status_code == 200
    assert b"If you get HEADS you WIN" in response.data


def test_valid_toss(client):
    response = client.post("/toss")

    assert response.status_code == 200

    data = response.get_json()

    assert data["coin"] in ["heads", "tails"]
    assert data["result"] in ["YOU WIN", "YOU LOSE"]


def test_heads_result(client, monkeypatch):
    monkeypatch.setattr(
        toss_app,
        "choice",
        lambda options: "heads"
    )

    response = client.post("/toss")

    assert response.get_json()["result"] == "YOU WIN"


def test_tails_result(client, monkeypatch):
    monkeypatch.setattr(
        toss_app,
        "choice",
        lambda options: "tails"
    )

    response = client.post("/toss")

    assert response.get_json()["result"] == "YOU LOSE"
