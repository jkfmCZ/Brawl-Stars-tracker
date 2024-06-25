from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .utils import graph_gen as gen
import pandas as pd
import random
from .utils import get_data
from .utils.loader import restarter, player_log_load,club_checker,battle_log_load,brawles
from .models import Brawl_Tags
def random_tags():
# pl_tag = "#2Q0U9PJLP"
  count = Brawl_Tags.objects.count()
  random_t = Brawl_Tags.objects.all().values()[random.randint(0, count - 1)]["tag"][1:]
  return random_t

restarter()

def index(request):
    if request.method == 'POST':
        tagb = request.POST.get('validation').upper()
        tag= "#"+tagb
        validation = get_data.API_tester(tag)
        print(validation)
        if validation[0] == 'valid':
            restarter, player_log_load(tag),club_checker(tag),battle_log_load(tag),brawles
            return redirect(f'/p?tag={tagb}')
        return render(request, "invalid_tag.html", {"random_t":random_tags, "error":validation[1]})
    return render(request, "index.html",{"random_t":random_tags})

def p_report(request):
  pl_tag = "#"+request.GET.get('tag')
  pl_tag_m = pl_tag[1:]
  validation = get_data.API_tester(pl_tag)
  print(validation)
  if validation[0] == 'invalid':
            return render(request, "invalid_tag.html",{"random_t":random_tags,"error":validation[1]})
  else:
    
    own = gen.own_ornot(pl_tag)
    dict_pre = {"own":own, "tag":pl_tag_m, "random_t":random_tags, "pl_name":gen.player_name(pl_tag)}
    dict_f = dict_pre.copy()
    dict_f.update(gen.player_info(pl_tag))
    return render(request,"report.html", dict_f)

def p_games(request):
  pl_tag = "#"+request.GET.get('tag')
  validation = get_data.API_tester(pl_tag)

  if validation[0] == 'invalid':
            return render(request, "invalid_tag.html",{"random_t":random_tags,"error":validation[1]})
  else:
    pie_plot = gen.lossxwins(pl_tag)
    bar_plot = gen.bar_ratio(pl_tag)
    

    return render(request, "p_games.html",{"pl_name":gen.player_name(pl_tag),"random_t":random_tags,"tag":pl_tag[1:],"pie_plot":pie_plot, "bar_plot":bar_plot })

def p_team(request):
  pl_tag = "#"+request.GET.get('tag')
  validation = get_data.API_tester(pl_tag)
  if validation[0] == 'invalid':
            return render(request, "invalid_tag.html",{"random_t":random_tags,"error":validation[1]})
  else:
    used_b = gen.team_braw(pl_tag)
    trophy = gen.team_braw_trophy(pl_tag)
    return render(request, "p_team.html",{"pl_name":gen.player_name(pl_tag),"random_t":random_tags,"tag":pl_tag[1:],"used_plot":used_b,"trophy_plot":trophy})

def p_club(request):
  pl_tag = "#"+ request.GET.get('tag')
  pl_tagm = pl_tag[1:]
  validation = get_data.API_tester(pl_tag)
  if validation[0] == 'invalid':
            return render(request, "invalid_tag.html",{"random_t":random_tags,"error":validation[1]})
  else:
    club_check = club_checker(pl_tag)
    if club_check == False:
         return render(request, "no_club.html",{"random_t":random_tags,"tag":pl_tagm, "pl_name":gen.player_name(pl_tag)})
    else:
      members = gen.club_members(pl_tag)
      roles = gen.club_roles(pl_tag)
      trophies_plot = gen.clubm_trophies(pl_tag)
      pre_dict = {"random_t":random_tags,"roles":roles,"tag":pl_tagm, "trophies_plot":trophies_plot, "members":members, "pl_name":gen.player_name(pl_tag)}
      dict_f = pre_dict.copy()
      dict_f.update(gen.club_info(pl_tag))
      return render(request, "p_club.html",dict_f)

def p_braw(request):
  pl_tag = "#"+request.GET.get('tag')
  validation = get_data.API_tester(pl_tag)
  if validation[0] == 'invalid':
            return render(request, "invalid_tag.html",{"random_t":random_tags,"error":validation[1]})
  else:
    b_tree = gen.p_braw_wl(pl_tag)
    braw_lvl = gen.p_brawl_lvl(pl_tag)
    braw_trophies = gen.p_brawl_trophy(pl_tag)
    return render (request, "p_brawl.html", {"pl_name":gen.player_name(pl_tag),"random_t":random_tags,"tag":pl_tag[1:],"braw_fig":b_tree, "braw_lvl":braw_lvl, "braw_trophies":braw_trophies})