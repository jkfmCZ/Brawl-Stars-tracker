from django.shortcuts import render

def jkfm_report(request):
    return render(request, "iframes/jkfm_rep.html")

def jkfm_club(request):
    return render(request, "iframes/jkfm_club.html")

def jkfm_games(request):
    return render(request, "iframes/jkfm_games.html")


def jkfm_team(request):
    return render(request, "iframes/jkfm_team.html")

def jkfm_brawler(request):
    return render(request, "iframes/jkfm_brawler.html")
