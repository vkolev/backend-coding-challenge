from flask import Blueprint, request, jsonify

from gistapi.service import GistService

api = Blueprint("gistapi", __name__, url_prefix="/api/v1")


@api.route("/search", methods=["POST"])
def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    post_data = request.get_json()
    gist_service = GistService()

    result = {}

    gists = [item for sublist in gist_service.get_gists_for_user(post_data.get('username')) for item in sublist]
    matches = gist_service.search(gists=gists, pattern=post_data.get("pattern"))

    result['status'] = 'success'
    result['username'] = post_data.get("username")
    result['pattern'] = post_data.get("pattern")
    result['matches'] = matches

    return jsonify(result)
