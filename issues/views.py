from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Ticket
from .forms import TicketForm, CommentaireForm


@login_required
def tickets_liste(request):
    qs = Ticket.objects.select_related('projet', 'assigne_a').order_by('-cree_le')
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'issues/tickets.html', {'tickets': page_obj})


@login_required
def ticket_creer(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.rapporteur = request.user
            t.save()
            messages.success(request, 'Ticket créé')
            return redirect('issues:tickets')
    else:
        form = TicketForm()
    return render(request, 'issues/form_ticket.html', {'form': form, 'titre': 'Créer un ticket'})


@login_required
def ticket_editer(request, ticket_id):
    t = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=t)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket mis à jour')
            return redirect('issues:tickets')
    else:
        form = TicketForm(instance=t)
    return render(request, 'issues/form_ticket.html', {'form': form, 'titre': 'Éditer un ticket'})


@login_required
def ticket_supprimer(request, ticket_id):
    t = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        t.delete()
        messages.success(request, 'Ticket supprimé')
        return redirect('issues:tickets')
    return redirect('issues:tickets')
