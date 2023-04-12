from flask import flash, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from ..rotas.send_emailRout import send_email_bp





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

                # Cria uma mensagem de e-mail
                msg = Message(
                        subject = f'{formContato.name} enviou uma mensagem.',
                        sender='urbanpass2@gmail.com',
                        recipients=['urbanpass2@gmail.com'],
                        body = f'Nome: {formContato.name}\nTelefone: {formContato.phone}\n Mensagem: {formContato.message}'
                )
                
                # Envia a mensagem de e-mail
                Mail.send(msg)
                flash('Obrigado pelo seu contato! Sua mensagem foi enviada com sucesso.')
                return redirect(url_for('public.cidadao'))
