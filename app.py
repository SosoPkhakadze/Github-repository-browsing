import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template, session, request
from authlib.integrations.flask_client import OAuth
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

if not os.environ.get('GITHUB_CLIENT_ID') or not os.environ.get('GITHUB_CLIENT_SECRET'):
    raise ValueError("GitHub OAuth credentials must be set in .env file")

oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id=os.environ.get('GITHUB_CLIENT_ID'),
    client_secret=os.environ.get('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'repo read:user'},
)

@app.route('/')
def index():
    if 'github_token' not in session:
        return render_template('login.html')

    all_repos = []
    page = 1
    technologies = set()

    try:
        while True:
            try:
                url = f'https://api.github.com/user/repos?page={page}&per_page=100'
                headers = {'Authorization': f'Bearer {session["github_token"]["access_token"]}'}
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                repos_page = response.json()

                if not repos_page:
                    break

                for repo in repos_page:
                    if repo.get('language'):
                        technologies.add(repo['language'])

                all_repos.extend(repos_page)
                page += 1
            except requests.exceptions.RequestException as e:
                app.logger.error(f"GitHub API error: {e}")
                return render_template('error.html', message="Failed to fetch repositories")

    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return render_template('error.html', message="An unexpected error occurred")

    technologies = sorted(list(technologies))
    return render_template(
        'index.html', 
        user_info=session.get('user_info', {}), 
        repos=all_repos, 
        technologies=technologies
    )

@app.route('/login')
def login():
    redirect_uri = url_for('callback', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    try:
        token = github.authorize_access_token()
        if not token:
            return redirect('/')

        resp = github.get('user', token=token)
        profile = resp.json()

        session['github_token'] = token
        session['user_info'] = {
            'username': profile.get('login'),
            'avatar_url': profile.get('avatar_url')
        }
        return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f"Callback error: {e}")
        return render_template('error.html', message="Authentication failed")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()