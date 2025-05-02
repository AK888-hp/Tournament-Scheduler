# Cricket Tournament Management App

## Overview
This Django-based application helps manage cricket tournaments, allowing users to manage teams, players, matches, and player stats. The app also includes features for scheduling matches, adding new players, and viewing player statistics.

## Features
- **Team Management**: Create and manage cricket teams.
- **Player Management**: Add players to teams, specify player positions, and view player statistics.
- **Match Scheduling**: Schedule and manage matches in a round-robin format with knockout rounds.
- **Player Stats**: Track and manage player stats such as runs and wickets.

## Branch: `final-jnanesh`
This branch contains the latest features and improvements for the Cricket Tournament Management App. Please use this branch for all further developments and deployments.

## Requirements
- Python 3.x
- Django 3.x or higher
- MySQL (or any other database system, though MySQL is recommended)

## Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/AK888-hp/Tournament-Scheduler.git
cd Tournament-Scheduler
Step 2: Checkout to final-jnanesh branch
bash
Copy code
git checkout final-jnanesh
Step 3: Create a virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate  # For Windows use: venv\Scripts\activate
Step 4: Install dependencies
bash
Copy code
pip install -r requirements.txt
Step 5: Configure the database
Set up your MySQL database and update settings.py with the correct database credentials.

Step 6: Apply migrations
bash
Copy code
python manage.py migrate
Step 7: Create a superuser (optional but recommended)
bash
Copy code
python manage.py createsuperuser
Step 8: Run the server
bash
Copy code
python manage.py runserver
You can now access the app at http://127.0.0.1:8000.

Pulling the Latest Changes
To ensure you're working with the latest changes from the final-jnanesh branch, follow these steps:

Step 1: Pull the latest changes
bash
Copy code
git checkout final-jnanesh  # Ensure you're on the final-jnanesh branch
git pull origin final-jnanesh
This will fetch the latest updates to the final-jnanesh branch from the remote repository.

Usage
Login: Users can log in to the app to manage their teams, players, and stats.

Add Players and Teams: From the dashboard, users can add players to teams and track player stats.

Match Scheduling: The system automatically schedules matches based on the given start date and team rosters.

Contributing
Feel free to fork the repository and create a pull request for any improvements, bug fixes, or feature requests.

Fork the repository

Create your branch (git checkout -b feature-name)

Commit your changes (git commit -am 'Add new feature')

Push to the branch (git push origin feature-name)

Create a new Pull Request
