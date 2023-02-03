import re
from concurrent.futures import ThreadPoolExecutor
from string import Template
from typing import List, Dict, Optional, Pattern, Tuple

import requests


class GistService:

    BASE_URL = Template("https://api.github.com/users/$username/gists")

    def get_gists_for_user(self, username: str, per_page: int = 100):
        """Get gists for a given user

        This method will get all gists cycling through pages. It will stop cycling pages when the result length
        is smaller the per_page parameter.

        :param username: String - the username we are searching
        :param per_page: Integer - Results per page (default 100)

        :returns: List of JSON pages
        """
        page = 1
        while True:
            gist_url = self.BASE_URL.safe_substitute(username=username)
            response = requests.get(
                gist_url,
                params={"per_page": per_page, "page": page},
                timeout=10
            )
            if not response.ok or not response.json():
                break
            yield response.json()
            if len(response.json()) < per_page:
                break
            page += 1

    def find_gist(self, request_tuple: Tuple[Dict, Pattern]) -> Optional[Dict]:
        """Finds a gist matching a given pattern.

        Gets the contents of a Gist and matches it against a pattern and returns a Dict of the gist
        on success. otherwise None

        :param request_tuple: A Tuple containing a Gist JSON description and Regex Pattern
        :return: A matching Gist or None
        """
        gist, pattern = request_tuple
        for _, file in gist.get("files").items():
            if "image" in file.get("type"):
                # We are not interested in images, since they don't contain text
                continue
            content = requests.get(file.get("raw_url"), stream=True, timeout=10)
            for chunk in content.iter_content(chunk_size=512):
                # Read file in chunks to speed up reading larger files
                if re.search(pattern, chunk.decode("utf-8")) is not None:
                    return gist
        return None

    def search(self, gists: List[Dict], pattern: str) -> List[Dict]:
        """Search in list of gists for a given pattern

        :param gists: List of gists to search into
        :param pattern: Regex pattern to match against a gist

        :return: List of matching gists or empty list
        """
        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            for result in executor.map(
                self.find_gist, [(gist, pattern) for gist in gists],
                timeout=10
            ):
                if result:
                    results.append(result)
        return results