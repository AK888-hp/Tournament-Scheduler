from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('team_owner', 'Team Owner'),
        ('player', 'Player'),
        ('guest', 'Guest'),
    ]
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Default to user with ID 1
    team_name = models.CharField(max_length=100)
    team_logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)

    def __str__(self):
        return self.team_name


class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    age = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_matches')
    match_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.match_date}"

# ✅ Properly placed at the top level
class PlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='playerstats')
    role = models.CharField(max_length=100)
    runs = models.IntegerField()
    wickets = models.IntegerField()

    def __str__(self):
        return f"{self.player.name} - {self.role} - Runs: {self.runs} - Wickets: {self.wickets}"