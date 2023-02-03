import pytest

from gistapi import create_app


@pytest.fixture
def application():
    app = create_app()
    app.config.update(
        {
            "TESTING": True
        }
    )
    yield app


@pytest.fixture
def client(application):
    return application.test_client()


def test_ping_request(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.text == "pong"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {"username": "justdionysus", "pattern": ""},
            {"errors": [{"field": "pattern", "error": "is required"}], "status": "failed"},
        ),
        (
            {"username": "", "pattern": ""},
            {
                "errors": [
                    {
                        "field": "username",
                        "error": "is required"
                    },
                    {
                        "field": "pattern",
                        "error": "is required"
                    },
                ],
                "status": "failed",
            },
        ),
        (
            {"username": "justdionysus", "pattern": "[.*"},
            {
                "errors": [
                    {
                        "field": "pattern",
                        "error": "invalid pattern: unterminated character set at position 0"
                    }
                ],
                "status": "failed"
            },
        ),
    ],
)
def test_search_validation(client, test_input, expected):
    response = client.post("/api/v1/search", json=test_input)
    assert response.is_json is True
    assert response.json == expected


def test_search_with_one_result(client, mocker):
    mocker.patch("gistapi.service.GistService.get_gists_for_user", return_value=[])
    mocker.patch(
        "gistapi.service.GistService.search",
        return_value=[
            {
                "url": "https://api.github.com/gists/2decf6c462d9b4418f2",
                "id": "2decf6c462d9b4418f2",
                "files": {
                    "result.py": {
                        "filename": "result.py",
                        "type": "application/python",
                        "raw_url": "https://gists.githubusercontent.com/justdionysus/2decf6c462d9b4418f2/raw/result.py",
                    }
                },
            }
        ],
    )
    response = client.post(
        "/api/v1/search",
        json={"username": "justdionysus", "pattern": "import requests"},
    )
    assert response.status_code == 200
    assert len(response.json.get("matches")) == 1