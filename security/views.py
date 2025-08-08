from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import AuditConnexion


# Create your views here.


class AuditsConnexionView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        audits = AuditConnexion.objects.order_by('-cree_le')[:200]
        data = [
            {
                'utilisateur': (a.utilisateur.username if a.utilisateur else None),
                'adresse_ip': a.adresse_ip,
                'user_agent': a.user_agent,
                'succes': a.succes,
                'cree_le': a.cree_le,
            }
            for a in audits
        ]
        return Response(data)
