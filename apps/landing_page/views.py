from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


def landing_page(request):
    """
    View principal da landing page da ByteNest
    """
    context = {
        'page_title': 'ByteNest - Transforme Seu Negócio com Tecnologia',
        'meta_description': (
            'Descubra como a ByteNest pode revolucionar seu negócio com '
            'soluções tecnológicas inovadoras. Desenvolvimento web, apps '
            'mobile, automação e muito mais.'
        ),
    }
    return render(request, 'landing_page/landing_page.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def contact_form(request):
    """
    View para processar o formulário de contato
    """
    try:
        data = json.loads(request.body)

        # Aqui você pode adicionar lógica para:
        # - Salvar no banco de dados
        # - Enviar email
        # - Integrar com CRM
        # - Etc.

        name = data.get('name', '')
        email = data.get('email', '')
        message = data.get('message', '')

        # Validação básica
        if not name or not email or not message:
            return JsonResponse({
                'success': False,
                'message': (
                    'Por favor, preencha todos os campos obrigatórios.'
                )
            }, status=400)

        # Aqui você pode implementar a lógica de envio
        # Por exemplo, salvar no banco ou enviar email

        return JsonResponse({
            'success': True,
            'message': (
                'Mensagem enviada com sucesso! Entraremos em contato em '
                'breve.'
            )
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Erro ao processar os dados. Tente novamente.'
        }, status=400)
    except Exception:  # noqa: BLE001
        return JsonResponse({
            'success': False,
            'message': (
                'Ocorreu um erro interno. Tente novamente mais tarde.'
            )
        }, status=500)
