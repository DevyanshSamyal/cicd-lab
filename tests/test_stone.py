
from stone.app import app

import pytest


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200


def test_rules(client):
    response = client.get("/rules")

    assert response.status_code == 200
    assert b"STONE beats scissors" in response.data


def test_valid_game(client):
    response = client.post(
        "/play-game",
        json={"player_move": "stone"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["player_move"] == "stone"
    assert data["computer_move"] in ["stone", "paper", "scissors"]
    assert data["result"] in ["DRAW", "Computer WINS", "You WIN"]


def test_invalid_move(client):
    response = client.post(
        "/play-game",
        json={"player_move": "banana"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid move"
