from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


def login_view(request):
    """
    View para login por email
    """
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            password = data.get('password', '')
            
            if not email or not password:
                return JsonResponse({
                    'success': False,
                    'message': 'Email e senha são obrigatórios.'
                }, status=400)
            
            # Autenticar usuário por email
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login realizado com sucesso!',
                    'redirect_url': '/dashboard/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Email ou senha incorretos.'
                }, status=400)
                
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
    
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """
    View para logout
    """
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    """
    Dashboard do usuário logado
    """
    context = {
        'user': request.user,
        'page_title': 'Dashboard - ByteNest',
    }
    return render(request, 'accounts/dashboard.html', context)
