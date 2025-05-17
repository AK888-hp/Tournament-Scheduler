from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    coach_name = models.CharField(max_length=100, null=True, blank=True)  # Add this field

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
    team1 = models.ForeignKey(Team, related_name='team1_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2_matches', on_delete=models.CASCADE)
    match_date = models.DateField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)  # Make sure this is added
    result = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.match_date}"

class PlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='playerstats')
    role = models.CharField(max_length=100)
    runs = models.IntegerField()
    wickets = models.IntegerField()

    def __str__(self):
        return f"{self.player.name} - {self.role} - Runs: {self.runs} - Wickets: {self.wickets}"

