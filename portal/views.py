from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from profiles.models import EngineerProfile, Skill
from projects.models import Project
from .forms import EngineerProfileForm, ProjectForm
from security.permissions import EstManagerOuAdmin


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
def profil_creer(request):
    # Un manager/admin peut créer n'importe quel profil; un utilisateur peut créer le sien si inexistant
    if request.method == 'POST':
        form = EngineerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profil = form.save(commit=False)
            profil.user = request.user
            profil.save()
            return redirect('portal:profils')
    else:
        form = EngineerProfileForm()
    return render(request, 'portal/form_profil.html', {'form': form, 'titre': 'Créer un profil'})


@login_required
def profil_editer(request, profil_id):
    profil = get_object_or_404(EngineerProfile, id=profil_id)
    if profil.user != request.user and not (request.user.is_staff or getattr(request.user, 'role', None) in ('ADMIN', 'MANAGER')):
        return redirect('portal:profils')
    if request.method == 'POST':
        form = EngineerProfileForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            return redirect('portal:profils')
    else:
        form = EngineerProfileForm(instance=profil)
    return render(request, 'portal/form_profil.html', {'form': form, 'titre': 'Éditer un profil'})


@login_required
def projets(request):
    projets_qs = Project.objects.all().order_by('-id')
    paginator = Paginator(projets_qs, 10)
    page = request.GET.get('page')
    projets_page = paginator.get_page(page)
    return render(request, 'portal/projets.html', {'projets': projets_page})


@login_required
def projet_creer(request):
    if not (request.user.is_staff or getattr(request.user, 'role', None) in ('ADMIN', 'MANAGER')):
        return redirect('portal:projets')
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)
            projet.created_by = request.user
            projet.save()
            return redirect('portal:projets')
    else:
        form = ProjectForm()
    return render(request, 'portal/form_projet.html', {'form': form, 'titre': 'Créer un projet'})


@login_required
def projet_editer(request, projet_id):
    projet = get_object_or_404(Project, id=projet_id)
    if not (request.user.is_staff or getattr(request.user, 'role', None) in ('ADMIN', 'MANAGER')):
        return redirect('portal:projets')
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=projet)
        if form.is_valid():
            form.save()
            return redirect('portal:projets')
    else:
        form = ProjectForm(instance=projet)
    return render(request, 'portal/form_projet.html', {'form': form, 'titre': 'Éditer un projet'})


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
