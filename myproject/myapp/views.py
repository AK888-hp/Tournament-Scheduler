from django.shortcuts import render, get_object_or_404, redirect
from .models import Team, Player, Match, PlayerStats
from .forms import PlayerStatsForm, TeamForm, PlayerForm,ScheduleForm
from datetime import datetime, timedelta, time


# -------------------- GENERAL VIEWS --------------------
def home(request):
    return render(request, 'myapp/home.html')


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
    players = Player.objects.all()
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


# -------------------- MATCH VIEWS --------------------
def match_list(request):
    matches = Match.objects.all().order_by('match_date', 'start_time')
    error = None

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            teams = list(Team.objects.all())

            if len(teams) < 4:
                error = 'At least 4 teams are required to schedule matches.'
            else:
                Match.objects.all().delete()

                slot1 = (time(15, 30), time(19, 0))   # 3:30 PM – 7:00 PM
                slot2 = (time(19, 30), time(23, 0))   # 7:30 PM – 11:00 PM

                day = 0
                for i in range(0, len(teams), 4):
                    if i + 3 >= len(teams):
                        break
                    t1, t2, t3, t4 = teams[i], teams[i+1], teams[i+2], teams[i+3]
                    match_day = start_date + timedelta(days=day)

                    Match.objects.create(
                        team1=t1,
                        team2=t2,
                        match_date=match_day,
                        start_time=datetime.combine(match_day, slot1[0]),
                        end_time=datetime.combine(match_day, slot1[1])
                    )
                    Match.objects.create(
                        team1=t3,
                        team2=t4,
                        match_date=match_day,
                        start_time=datetime.combine(match_day, slot2[0]),
                        end_time=datetime.combine(match_day, slot2[1])
                    )
                    day += 1

                return redirect('match_list')
    else:
        form = ScheduleForm()

    return render(request, 'myapp/match-list.html', {
        'form': form,
        'matches': matches,
        'error': error,
    })

def schedule_matches(request):
    teams = list(Team.objects.all())
    if len(teams) < 4:
        return render(request, 'myapp/match-list.html', {'error': 'At least 4 teams required to schedule matches.'})

    Match.objects.all().delete()  # Clear old matches

    current_date = datetime.now().date()
    match_duration_1 = (time(15, 30), time(19, 0))  # 3:30 PM to 7:00 PM
    match_duration_2 = (time(19, 30), time(23, 0))  # 7:30 PM to 11:00 PM

    day = 0
    for i in range(0, len(teams), 4):
        if i + 3 >= len(teams):
            break

        t1, t2, t3, t4 = teams[i], teams[i + 1], teams[i + 2], teams[i + 3]
        match_day = current_date + timedelta(days=day)

        Match.objects.create(
            team1=t1,
            team2=t2,
            match_date=match_day,
            start_time=datetime.combine(match_day, match_duration_1[0]),
            end_time=datetime.combine(match_day, match_duration_1[1])
        )
        Match.objects.create(
            team1=t3,
            team2=t4,
            match_date=match_day,
            start_time=datetime.combine(match_day, match_duration_2[0]),
            end_time=datetime.combine(match_day, match_duration_2[1])
        )

        day += 1

    return redirect('match_list')


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

    return render(request, 'add_player_stats.html', {'form': form, 'player': player})


# -------------------- STANDINGS VIEW --------------------
def standings(request):
    return render(request, 'myapp/standings.html')
