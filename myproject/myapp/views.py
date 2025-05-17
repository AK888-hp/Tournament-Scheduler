from django.shortcuts import get_object_or_404, render, redirect
from .models import Player, PlayerStats, Team, Match
from datetime import datetime, timedelta
from itertools import combinations
from .forms import PlayerForm, PlayerStatsForm, TeamForm
import random
from django.http import JsonResponse


# -------------------- SCHEDULING VIEWS --------------------

def generate_schedule(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        schedule_matches(start_date)
        return redirect('home')

    return render(request, 'myapp/schedule_form.html')

# -------------------- MATCH VIEWS --------------------
def schedule_matches(request):
    
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

            teams = list(Team.objects.all())
            if len(teams) < 2:
                return render(request, 'myapp/scheduler.html', {
                    'scheduled_matches': [],
                    'error': 'At least two teams are required to schedule matches.'
                })

            Match.objects.all().delete()

            time_slots = [("15:30", "19:00"), ("19:30", "23:00")]

            random.shuffle(teams)
            matchups = list(combinations(teams, 2))
            random.shuffle(matchups)

            scheduled_matches = []
            team_last_played = {team.id: -2 for team in teams}  # -2 so that all teams can play on day 0
            day_offset = 0

            while matchups:
                for slot_index in range(len(time_slots)):
                    for idx, (team1, team2) in enumerate(matchups):
                        if (day_offset - team_last_played[team1.id] > 1 and
                            day_offset - team_last_played[team2.id] > 1):

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

                            team_last_played[team1.id] = day_offset
                            team_last_played[team2.id] = day_offset
                            matchups.pop(idx)
                            break  # Go to next time slot
                    else:
                        continue
                    break  # A match was scheduled in this slot
                else:
                    day_offset += 1
                    continue
                day_offset += 1

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
    selected_team = None
    players = []

    team_id = request.GET.get('team_id')
    if team_id:
        selected_team = get_object_or_404(teams, id=team_id)
        players = selected_team.player_set.all()

    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        coach_name = request.POST.get('coach_name')
        team_logo = request.FILES.get('team_logo')

        if team_name:
            Team.objects.create(team_name=team_name, coach_name=coach_name, team_logo=team_logo)
            return redirect('team_list')

    return render(request, 'myapp/team_list.html', {
        'teams': teams,
        'selected_team': selected_team,
        'players': players,
    })

def delete_team(request, team_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        team = get_object_or_404(Team, id=team_id)
        team.delete()  # Will cascade delete players if your model uses on_delete=models.CASCADE
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
def add_team(request):
    teams = Team.objects.all()
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_team')
    else:
        form = TeamForm()

    return render(request, 'myapp/add_team.html', {'form': form, 'teams': teams})

def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'myapp/team_detail.html', {'team': team})

# -------------------- PLAYER VIEWS --------------------
def player_list(request):
    players = Player.objects.all()
    return render(request, 'myapp/player_list.html', {'players': players})

def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
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

# -------------------- MATCH LIST VIEW --------------------
def match_list(request):
    matches = Match.objects.all()
    return render(request, 'myapp/match-list.html', {'matches': matches})

def delete_player(request, player_id):
    if request.method == 'POST':
        player = get_object_or_404(Player, id=player_id)
        player.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
def delete_player_stat(request, stat_id):
    if request.method == 'POST':
        stat = get_object_or_404(PlayerStats, id=stat_id)
        stat.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
