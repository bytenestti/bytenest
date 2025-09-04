from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json


@login_required
def dashboard_home(request):
    """
    Dashboard principal do usuário
    """
    context = {
        'user': request.user,
        'page_title': 'Dashboard - ByteNest',
        'stats': {
            'total_projects': 0,
            'active_projects': 0,
            'completed_projects': 0,
            'pending_tasks': 0,
        }
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def profile_view(request):
    """
    Visualização e edição do perfil do usuário
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Atualizar informações do usuário
            user = request.user
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Perfil atualizado com sucesso!'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Erro ao processar os dados.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Erro interno do servidor.'
            }, status=500)
    
    context = {
        'user': request.user,
        'page_title': 'Perfil - ByteNest',
    }
    return render(request, 'dashboard/profile.html', context)


@login_required
def settings_view(request):
    """
    Configurações do usuário
    """
    context = {
        'user': request.user,
        'page_title': 'Configurações - ByteNest',
    }
    return render(request, 'dashboard/settings.html', context)


@login_required
def projects_view(request):
    """
    Visualização de projetos
    """
    # Simular dados de projetos (em produção viria do banco)
    projects = [
        {
            'id': 1,
            'name': 'Site Corporativo',
            'status': 'Em andamento',
            'progress': 75,
            'deadline': '2024-12-15',
            'client': 'TechCorp',
        },
        {
            'id': 2,
            'name': 'App Mobile',
            'status': 'Planejamento',
            'progress': 25,
            'deadline': '2025-02-20',
            'client': 'StartupXYZ',
        },
        {
            'id': 3,
            'name': 'Sistema de Vendas',
            'status': 'Concluído',
            'progress': 100,
            'deadline': '2024-11-30',
            'client': 'RetailMax',
        },
    ]
    
    context = {
        'user': request.user,
        'page_title': 'Projetos - ByteNest',
        'projects': projects,
    }
    return render(request, 'dashboard/projects.html', context)


@login_required
def analytics_view(request):
    """
    Analytics e relatórios
    """
    # Simular dados de analytics (em produção viria do banco)
    analytics_data = {
        'monthly_revenue': 45000,
        'projects_completed': 12,
        'client_satisfaction': 98,
        'team_productivity': 92,
        'revenue_chart': [
            {'month': 'Jan', 'revenue': 35000},
            {'month': 'Fev', 'revenue': 42000},
            {'month': 'Mar', 'revenue': 38000},
            {'month': 'Abr', 'revenue': 45000},
            {'month': 'Mai', 'revenue': 48000},
            {'month': 'Jun', 'revenue': 45000},
        ]
    }
    
    context = {
        'user': request.user,
        'page_title': 'Analytics - ByteNest',
        'analytics': analytics_data,
    }
    return render(request, 'dashboard/analytics.html', context)
