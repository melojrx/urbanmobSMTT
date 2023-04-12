from flask import flash, request, redirect, url_for
from flask_mail import Mail, Message
from ..rotas.send_emailRout import send_email_bp
from app import mail

class Contato:
        def __init__(self, name, phone, message):
                self.name = name,
                self.phone = phone, 
                self.message = message

        
        @send_email_bp.route('/send_email', methods=['GET', 'POST'])
        def send_email():
                # Recupera as informações do formulário
                if request.method == 'POST': 
                        formContato = Contato(
                                request.form['name'],
                                request.form['phone'],
                                request.form['message']
                        )
               
                with mail.connect() as conn:
                        msg = Message(
                                subject = f'{formContato.name} enviou uma mensagem.',
                                sender='urbanpass2@gmail.com',
                                recipients=['urbanpass2@gmail.com'],
                                body = f'Nome: {formContato.name}\nTelefone: {formContato.phone}\n Mensagem: {formContato.message}'
                )
                        conn.send(msg)

                # Envia a mensagem de e-mail
                # Mail.send(msg)
                flash('Obrigado pelo seu contato! Sua mensagem foi enviada com sucesso.')
                return redirect(url_for('public.cidadao'))
