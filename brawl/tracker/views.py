from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .utils import graph_gen as gen
from django.http import QueryDict
from .utils import get_data

# pl_tag = "#2Q0U9PJLP"

def index(request):
    if request.method == 'POST':
        tagb = request.POST.get('validation')
        tag= "#"+tagb
        validation = get_data.API_tester(tag)
        print(validation)
        if validation == 'valid':
            return redirect(f'/p?tag={tagb}')
        return render(request, "invalid_tag.html")
    return render(request, "index.html")

def p_report(request):
  pl_tag = "#"+request.GET.get('tag')
  
  validation = get_data.API_tester(pl_tag)
  print(validation)
  if validation == 'invalid':
            return render(request, "invalid_tag.html")
  else:
    own = gen.own_ornot(pl_tag)
    dict_pre = {"own":own, "tag":pl_tag[1:]}
    dict_f = dict_pre.copy()
    dict_f.update(gen.player_info(pl_tag))
    return render(request,"report.html", dict_f)

def p_games(request):
  pl_tag = "#"+request.GET.get('tag')
  validation = get_data.API_tester(pl_tag)

  if validation == 'invalid':
            return render(request, "invalid_tag.html")
  else:
    pie_plot = gen.lossxwins(pl_tag)
    bar_plot = gen.bar_ratio(pl_tag)
    

    return render(request, "p_games.html",{"tag":pl_tag[1:],"pie_plot":pie_plot, "bar_plot":bar_plot })

def p_team(request):
  pl_tag = "#"+request.GET.get('tag')
  validation = get_data.API_tester(pl_tag)
  if validation == 'invalid':
            return render(request, "invalid_tag.html")
  else:
    used_b = gen.team_braw(pl_tag)
    trophy = gen.team_braw_trophy(pl_tag)
    return render(request, "p_team.html",{"tag":pl_tag[1:],"used_plot":used_b,"trophy_plot":trophy})

def p_club(request):
  pl_tag = "#"+ request.GET.get('tag')
  validation = get_data.API_tester(pl_tag)
  if validation == 'invalid':
            return render(request, "invalid_tag.html")
  else:
    members = gen.club_members(pl_tag)
    roles = gen.club_roles(pl_tag)
    trophies_plot = gen.clubm_trophies(pl_tag)
    pre_dict = {"roles":roles,"tag":pl_tag[1:], "trophies_plot":trophies_plot, "members":members}
    dict_f = pre_dict.copy()
    dict_f.update(gen.club_info(pl_tag))
    return render(request, "p_club.html",dict_f)

def p_braw(request):
  pl_tag = "#"+request.GET.get('tag')
  validation = get_data.API_tester(pl_tag)
  if validation == 'invalid':
            return render(request, "invalid_tag.html")
  else:
    b_tree = gen.p_braw_wl(pl_tag)
    braw_lvl = gen.p_brawl_lvl(pl_tag)
    braw_trophies = gen.p_brawl_trophy(pl_tag)
    return render (request, "p_brawl.html", {"tag":pl_tag[1:],"braw_fig":b_tree, "braw_lvl":braw_lvl, "braw_trophies":braw_trophies})