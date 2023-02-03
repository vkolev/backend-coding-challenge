import json
import re

import pytest

from gistapi.service import GistService


@pytest.fixture
def expected_list_result():
    return json.dumps(
        [
            {
                "url": "https://api.github.com/gists/7d7218b569014139f74e27a75ffc5293",
                "id": "7d7218b569014139f74e27a75ffc5293",
                "node_id": "G_kwDOACDaydoAIDdkNzIxOGI1NjkwMTQxMzlmNzRlMjdhNzVmZmM1Mjkz",
                "files": {
                    "keybase.md": {
                        "filename": "keybase.md",
                        "type": "text/markdown",
                        "raw_url": "https://gist.githubusercontent.com/justdionysus/7d7218b569014139f74e27a75ffc5293/raw/bb1568518c57171a04fa7dfca7bbaa6c8c6fe891/keybase.md",
                        "size": 2189,
                    }
                },
            },
            {
                "url": "https://api.github.com/gists/c8693981025287ea858d2ca5a93ec103",
                "id": "c8693981025287ea858d2ca5a93ec103",
                "node_id": "MDQ6R2lzdGM4NjkzOTgxMDI1Mjg3ZWE4NThkMmNhNWE5M2VjMTAz",
                "files": {
                    "bflt.py": {
                        "filename": "bflt.py",
                        "type": "application/x-python",
                        "raw_url": "https://gist.githubusercontent.com/justdionysus/c8693981025287ea858d2ca5a93ec103/raw/a1352c102b8d47e580cc773e56af9968f7fca03a/bflt.py",
                        "size": 3593,
                    }
                },
            },
            {
                "url": "https://api.github.com/gists/65e6162d99c2e2ea8049b0584dd00912",
                "id": "65e6162d99c2e2ea8049b0584dd00912",
                "node_id": "MDQ6R2lzdDY1ZTYxNjJkOTljMmUyZWE4MDQ5YjA1ODRkZDAwOTEy",
                "files": {
                    "john_waters.py.nosecrets": {
                        "filename": "john_waters.py.nosecrets",
                        "type": "text/plain",
                        "raw_url": "https://gist.githubusercontent.com/justdionysus/65e6162d99c2e2ea8049b0584dd00912/raw/956c62609ab7ea695731bc836ccf85290809a59e/john_waters.py.nosecrets",
                        "size": 3606,
                    }
                },
            },
            {
                "url": "https://api.github.com/gists/6b2972aa971dd605f524",
                "id": "6b2972aa971dd605f524",
                "node_id": "MDQ6R2lzdDZiMjk3MmFhOTcxZGQ2MDVmNTI0",
                "files": {
                    "gistfile1.txt": {
                        "filename": "gistfile1.txt",
                        "type": "text/plain",
                        "raw_url": "https://gist.githubusercontent.com/justdionysus/6b2972aa971dd605f524/raw/eef9ff9d900272ff2a6320cf824523e23a21737d/gistfile1.txt",
                        "size": 43,
                    }
                },
            },
            {
                "url": "https://api.github.com/gists/6b2972aa971dd605f524",
                "id": "6b2972aa971dd605f524",
                "node_id": "MDQ6R2lzdDZiMjk3MmFhOTcxZGQ2MDVmNTI0",
                "files": {
                    "image.png": {
                        "filename": "image.png",
                        "type": "image/png",
                        "raw_url": "https://gist.githubusercontent.com/justdionysus/6b2972aa971dd605f524/raw/eef9ff9d900272ff2a6320cf824523e23a21737d/gistfile1.txt",
                        "size": 43,
                    }
                },
            },
        ]
    )


def test_get_user_justdionysus(response_mock):
    expected_result = json.dumps([{}, {}, {}, {}])
    with response_mock(
        f"GET https://api.github.com/users/justdionysus/gists?per_page=100&page=1 -> 200 :{expected_result}"
    ):
        service = GistService()
        result = [
            item for sublist in service.get_gists_for_user("justdionysus") for item in sublist
        ]
        assert len(result) == 4


def test_get_unexisting_user(response_mock):
    with response_mock(
        f"GET https://api.github.com/users/asd89sdh98qhd9quhdw9uhdq/gists?per_page=100&page=1 -> 404 :[]"
    ):
        service = GistService()
        result = list(service.get_gists_for_user("asd89sdh98qhd9quhdw9uhdq"))
        assert result == []


def test_search(response_mock, expected_list_result):
    with response_mock(
        [
            f"GET https://api.github.com/users/justdionysus/gists?per_page=100&page=1 -> 200 :{expected_list_result}",
            f"GET https://gist.githubusercontent.com/justdionysus/7d7218b569014139f74e27a75ffc5293/raw/bb1568518c57171a04fa7dfca7bbaa6c8c6fe891/keybase.md -> 200 :test",
            f"GET https://gist.githubusercontent.com/justdionysus/c8693981025287ea858d2ca5a93ec103/raw/a1352c102b8d47e580cc773e56af9968f7fca03a/bflt.py -> 200 :import requests",
            f"GET https://gist.githubusercontent.com/justdionysus/65e6162d99c2e2ea8049b0584dd00912/raw/956c62609ab7ea695731bc836ccf85290809a59e/john_waters.py.nosecrets -> 200 :test",
            f"GET https://gist.githubusercontent.com/justdionysus/6b2972aa971dd605f524/raw/eef9ff9d900272ff2a6320cf824523e23a21737d/gistfile1.txt -> 200 :test",
        ]
    ):
        service = GistService()
        gists = [
            item for sublist in service.get_gists_for_user("justdionysus") for item in sublist
        ]
        results = list(service.search(gists, r"import requests"))
        assert results is not None
        assert len(results) == 1
        assert "bflt.py" in results[0].get("files").keys()
