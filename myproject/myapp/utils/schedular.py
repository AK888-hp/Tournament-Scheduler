from datetime import datetime, timedelta, time
from models import Team, Match

def schedule_matches(start_date_str, user):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    time_slots = [
        (time(15, 30), time(19, 0)),   # 3:30 PM to 7:00 PM
        (time(19, 30), time(23, 0))    # 7:30 PM to 11:00 PM
    ]

    teams = list(Team.objects.filter(user=user))
    matches = []

    # Generate all round-robin matchups
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            matches.append((teams[i], teams[j]))

    match_day = start_date
    slot_index = 0

    for team1, team2 in matches:
        start, end = time_slots[slot_index]
        Match.objects.create(
            team1=team1,
            team2=team2,
            match_date=match_day,
            start_time=start,
            end_time=end,
            is_playoff=False
        )
        slot_index += 1
        if slot_index == len(time_slots):
            slot_index = 0
            match_day += timedelta(days=1)
