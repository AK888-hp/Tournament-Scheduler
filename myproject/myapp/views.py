from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Player, Team, Match
from datetime import datetime, timedelta
from itertools import combinations
from .forms import PlayerForm, PlayerStatsForm, TeamForm

def generate_schedule(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        schedule_matches(start_date)
        return redirect('home')  # or wherever you want

    return render(request, 'myapp/schedule_form.html')


# -------------------- MATCH VIEWS --------------------
from datetime import datetime, timedelta, time
from itertools import combinations
from django.shortcuts import render
from .models import Match, Team

from django.shortcuts import render
from datetime import datetime, timedelta
from itertools import combinations
from .models import Match, Team

def schedule_matches(request):
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

            # Clear old matches and regenerate
            Match.objects.all().delete()

            teams = list(Team.objects.all())
            time_slots = [("15:30", "19:00"), ("19:30", "23:00")]  # 12-hr shown in template

            matchups = list(combinations(teams, 2))  # Round-robin
            day_offset = 0
            slot_index = 0

            for team1, team2 in matchups:
                match_date = start_date + timedelta(days=day_offset)
                start_time = datetime.strptime(time_slots[slot_index][0], "%H:%M").time()
                end_time = datetime.strptime(time_slots[slot_index][1], "%H:%M").time()

                Match.objects.create(
                    team1=team1,
                    team2=team2,
                    match_date=match_date,
                    start_time=start_time,
                    end_time=end_time
                )

                slot_index += 1
                if slot_index >= len(time_slots):
                    slot_index = 0
                    day_offset += 1

    # Always load saved matches from DB for display
    scheduled_matches = Match.objects.all().order_by('match_date', 'start_time')

    return render(request, 'myapp/scheduler.html', {
        'scheduled_matches': scheduled_matches
    })



# -------------------- GENERAL VIEWS --------------------
def home(request):
    return render(request, 'myapp/home.html')
def login(request):
    return render(request, 'myapp/login.html')


def profile(request):
    return render(request, 'myapp/profile.html')


# -------------------- TEAM VIEWS --------------------
def teams(request):
    user_teams = Team.objects.all()
    selected_team_id = request.GET.get('team_id')
    selected_team = None
    players = []

    if selected_team_id:
        selected_team = get_object_or_404(user_teams, id=selected_team_id)
        players = selected_team.player_set.all()

    return render(request, 'myapp/teams.html', {
        'teams': user_teams,
        'selected_team': selected_team,
        'players': players,
    })


def team_list(request):
    teams = Team.objects.all()
    return render(request, 'myapp/team_list.html', {'teams': teams})


def add_team(request):
    teams = Team.objects.all()
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            return redirect('add_team')
    else:
        form = TeamForm()

    return render(request, 'myapp/add_team.html', {'form': form, 'teams': teams})


def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'myapp/team_detail.html', {'team': team})


# -------------------- PLAYER VIEWS --------------------
def player_list(request):
    players = Player.objects.all()  # Fetching all players from the database
    return render(request, 'myapp/player_list.html', {'players': players})


def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save()
            return redirect('player_list')
    else:
        form = PlayerForm()

    return render(request, 'myapp/add_player.html', {'form': form})


# -------------------- PLAYER STATS VIEWS --------------------
def player_stats(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    stats = player.playerstats.all()
    return render(request, 'myapp/view_stats.html', {'player': player, 'stats': stats})


def add_player_stats(request, player_id):
    player = get_object_or_404(Player, id=player_id)

    if request.method == 'POST':
        form = PlayerStatsForm(request.POST)
        if form.is_valid():
            stats = form.save(commit=False)
            stats.player = player
            stats.save()
            return redirect('player_stats', player_id=player.id)
    else:
        form = PlayerStatsForm()

    return render(request, 'myapp/add_player_stats.html', {'form': form, 'player': player})

def match_list(request):
    matches = Match.objects.all()  # Fetch all matches
    return render(request, 'myapp/match_list.html', {'matches': matches})  # Return a template with matches
def team_list(request):
    teams = Team.objects.all()
    selected_team = None
    players = []

    # Handle team selection
    team_id = request.GET.get('team_id')
    if team_id:
        selected_team = get_object_or_404(teams, id=team_id)
        players = selected_team.player_set.all()

    # Handle team creation
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        coach_name = request.POST.get('coach_name')
        team_logo = request.FILES.get('team_logo')

        if team_name:
            Team.objects.create(team_name=team_name, coach_name=coach_name, team_logo=team_logo)
            return render(request, 'myapp/add_player_stats.html', {'form': form, 'player': player})

    return render(request, 'myapp/team_list.html', {
        'teams': teams,
        'selected_team': selected_team,
        'players': players,
    })
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        team.delete()
        messages.success(request, 'Team deleted successfully.')
        return redirect('myapp/team_list')  # Redirect to team list page after deletion
    return redirect('myapp/team_list')