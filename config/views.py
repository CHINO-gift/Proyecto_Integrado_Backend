
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from delegacionesApp.models import Delegacion
from funcionariosApp.models import Funcionario


# ==========================================
# EVA 3 - PANEL PRINCIPAL DE SIGED
# ==========================================

@login_required
def panel_principal(request):

    total_delegaciones = Delegacion.objects.count()
    total_funcionarios = Funcionario.objects.count()

    contexto = {
        'total_delegaciones': total_delegaciones,
        'total_funcionarios': total_funcionarios,
    }

    return render(request, 'panel/inicio.html', contexto)
