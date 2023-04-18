from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
import time

from apichat.models import ChatMessage


def chat(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = 'response placeholder'
        nonce = int(time.time())
        chat_message = ChatMessage(prompt=prompt, response=response, nonce=nonce)
        chat_message.save()
    else:
        prompt = ''

    # Return a list of all chats, in reverse order
    chats = ChatMessage.objects.all().order_by('-id')

    return render(request, 'apichat/chat.html', {'prompt': prompt, 'chats': chats})

# This is the command that is about to be send to ChatPlug
@csrf_exempt
def command(request):

    # Get the most recent ChatMessage
    chat_message = ChatMessage.objects.last()

    response_data = {
        'nonce': chat_message.nonce,
        'command': chat_message.prompt,
    }

    json_response = JsonResponse(response_data)

    return json_response


@csrf_exempt
def response(request):
    # create your response

    response = HttpResponse()

    if request.method == 'POST':
        data = json.loads(request.body)

        # Get the nonce from the request
        nonce = data['nonce']

        # Get the ChatMessage with the matching nonce
        chat_message = ChatMessage.objects.get(nonce=nonce)

        # Update the ChatMessage with the response
        chat_message.response = data['response']
        chat_message.save()

    return response


@csrf_exempt
def input(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # do something with the input data
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def output(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # generate the output data
        output_data = {'result': 'Hello, ' + data['name'] + '!'}
        return JsonResponse(output_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})


def update_chat_message(request):
    # Get the ChatMessage object to update
    chat_message = ChatMessage.objects.last()

    if request.method == 'POST':
        # If the form has been submitted, update the ChatMessage object with the form data
        chat_message.prompt = request.POST.get('prompt')
        chat_message.response = request.POST.get('response')
        chat_message.nonce = request.POST.get('nonce')
        chat_message.save()
        # return redirect('chat_message_detail', chat_message_id=chat_message.id)

    # Render the chat message update form with the existing data pre-populated
    form = {
        'prompt': chat_message.prompt,
        'response': chat_message.response,
        'nonce': chat_message.nonce,
    }

    return render(request, 'apichat/update_chat_message.html', {'form': form})
