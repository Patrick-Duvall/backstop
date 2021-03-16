import functools
import json
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from oauthlib.oauth2 import WebApplicationClient
import requests

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import db
from app.models import User

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_TEST_CLIENT", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_TEST_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

bp = Blueprint('auth', __name__, url_prefix='/auth')

# # User session management setup
# # https://flask-login.readthedocs.io/en/latest
# login_manager = LoginManager()
# login_manager.init_app(app)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
# TODO ADD ERROR HANDLING

@bp.route('/google_login', methods=['GET'])
def google_login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@bp.route("/google_login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        username = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

      # Create a user in your db with the information provided by Google
    user = User(
        id_=unique_id, username=username, email=users_email
    )
    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, username, users_email)
    login_user(user)

    return redirect(url_for('alerts.index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.google_login'))

        return view(**kwargs)

    return wrapped_view
