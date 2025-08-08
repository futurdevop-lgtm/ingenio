from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from profiles.models import EngineerProfile, Skill
from projects.models import Project


def accueil_app(request):
    return redirect('portal:tableau')


@login_required
def tableau(request):
    stats = {
        'nb_ingenieurs': EngineerProfile.objects.count(),
        'nb_projets': Project.objects.count(),
    }
    return render(request, 'portal/tableau.html', {'stats': stats})


@login_required
def profils(request):
    q = request.GET.get('q', '')
    profils_qs = EngineerProfile.objects.select_related('user')
    if q:
        profils_qs = profils_qs.filter(user__username__icontains=q)
    paginator = Paginator(profils_qs, 10)
    page = request.GET.get('page')
    profils_page = paginator.get_page(page)
    return render(request, 'portal/profils.html', {'profils': profils_page, 'q': q})


@login_required
def projets(request):
    projets_qs = Project.objects.all().order_by('-id')
    paginator = Paginator(projets_qs, 10)
    page = request.GET.get('page')
    projets_page = paginator.get_page(page)
    return render(request, 'portal/projets.html', {'projets': projets_page})


@login_required
def recherche(request):
    competence = request.GET.get('competence', '')
    stack = request.GET.get('pile', '')
    qs = EngineerProfile.objects.all()
    if competence:
        qs = qs.filter(skills__name__icontains=competence)
    if stack:
        stacks = {
            'MEAN': ['MongoDB', 'Express', 'Angular', 'Node.js'],
            'MERN': ['MongoDB', 'Express', 'React', 'Node.js'],
            'LAMP': ['Linux', 'Apache', 'MySQL', 'PHP'],
            '.NET': ['C#', 'ASP.NET', 'SQL Server'],
        }
        for s in stacks.get(stack.upper(), []):
            qs = qs.filter(skills__name__iexact=s)
    skills = Skill.objects.order_by('name')[:50]
    paginator = Paginator(qs.distinct(), 12)
    page = request.GET.get('page')
    profils_page = paginator.get_page(page)
    return render(request, 'portal/recherche.html', {'profils': profils_page, 'skills': skills, 'competence': competence, 'pile': stack})
