from django.shortcuts import render,redirect
from django.db import transaction
from django.contrib import messages
from .models import Producto, Ticket,TicketItem
from .forms import TicketForm,TicketItemFormSet
from django.core.mail import send_mail
from django.conf import settings

# Vistas Ticket y descontar stock
def crear_ticket(request):
    if request.method=='POST':
        ticket_form=TicketForm(request.POST)
        formset=TicketItemFormSet(request.POST)
        if ticket_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                ticket=ticket_form.save()
                for item_form in formset:
                    producto=item_form.cleaned_data.get('producto')
                    cantidad=item_form.cleaned_data.get('cantidad') or 0
                    if producto and cantidad>0:
                        #verificar stock disponible
                        if producto.stock < cantidad:
                            messages.error(request=f'NO hay suficiente stock de {producto.nombre}. Disponible:{producto.stock}')
                                
                    transaction.set_rollback(True)
                    return redirect('crear_ticket')
#Crear Item
        TicketItem.objects.create(ticket=ticket, producto=producto, cantidad=cantidad)  
#Desconatar stock
        producto.stock-=cantidad
        producto.save()
        messages.success(request,'Ticket creado y stock actualizado correctamente')
        return redirect('lista_tickets')
    else:
        ticket_form= TicketForm()
        formset= TicketItemFormSet()
        return render(request,'crear_ticket.html',{'ticket_form':ticket_form,'formset':formset})
    
                                

#Funcion la cual utilizo para luego de finalizar la compra se envie un email a su correo eletronico

def enviar_ticket_compra(email_cliente, contenido_ticket):
    asunto= 'Tu Ticket de Compra'
    mensaje=contenido_ticket
    email_desde= settings.EMAIL_HOST_USER
    destinatarios=[email_cliente]
    
    send_mail(asunto,mensaje,email_desde,destinatarios)
    
#despues de confirmar compra utilizo la funcion para enviar el email
def procesar_compra(request):    
    email_cliente='cliente@example.com'
    contenido_ticket="Gracias por su Compra! Tu pedido es #1234... "
    
    enviar_ticket_compra(email_cliente,contenido_ticket)
    
    
    



