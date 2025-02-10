# GitHub Repository Browser

## Overview

A Flask-based web application that allows users to authenticate with GitHub and browse their repositories with an intuitive, modern interface.

## Features

- GitHub OAuth Authentication
- Responsive, professional UI
- Repository listing with details
- Technology-based repository filtering
- Error handling and user-friendly messages

## Prerequisites

- Python 3.8+
- GitHub OAuth Application

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SosoPkhakadze/Github-repository-browsing.git
cd Github-repository-browsing
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. GitHub OAuth Setup
   - Go to GitHub Developer Settings
   - Create a new OAuth App
   - Get Client ID and Client Secret

5. Create a `.env` file in project root:
```
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
```

## Running the Application

```bash
python app.py
```

Navigate to `http://localhost:5000` in your browser.

## Project Structure

- `app.py`: Main Flask application
- `templates/`: HTML templates
  - `index.html`: Main repository listing page
  - `error.html`: Error handling template
  - `404.html`: Not found page
- `.env`: Environment configuration
- `requirements.txt`: Python dependencies

## Technologies

- Flask
- GitHub API
- Tailwind CSS
- Python requests library
- Authlib for OAuth

## Security Considerations

- Uses secure session management
- Implements error handling
- Protects against unauthorized access

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## Author

Soso Pkhakadze
