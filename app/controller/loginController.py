from ..database import db
from validate_docbr import CPF
from ..models.userModel import User
from ..forms.loginForm import LoginForm
from ..forms.registerForm import RegisterForm
from ..rotas.loginRout import login_bp
from flask_login import login_user, logout_user
from flask import render_template, request, redirect, url_for, flash, session, jsonify
import requests

class loginController:

    global app_key 
    app_key = '15b1fac5baa876d624e6a7ea70b80d0ec89b5fa99558f275016e651e'
    global institution_external_id
    institution_external_id = '5a88f1a9cbcbccc6da0d942db89b78b7353802fb07d54a74061a3a06'

    @login_bp.route('/register', methods=['GET', 'POST'])
    def register():

        form = RegisterForm(request.form)

        if request.method == 'POST' and form.validate(): 

            name = form.name.data
            email = form.email.data
            txtcpf = form.cpf.data
            pwd = form.password.data

            cpf = CPF()
            if not cpf.validate(txtcpf): 
               flash('Ops. Não nos parece um CPF válido', 'error')
               return render_template('register.html', form=form)

            try:
                
                user = User(name, email, txtcpf, pwd)
                db.session.add(user)
                
                url = 'http://10.82.85.10:8080/api/caa/user/role'
                data = {'institution_external_id': institution_external_id, 'email': email, 'password': pwd, "application_external_id": app_key, "role_name": "URBANMOB_USER", 'type': 'USER'}
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, json=data, headers=headers)
                data = response.json() 
                #print(response.status_code)
                #print(response.json())
                
                if(response.status_code != 201):
                    db.session.rollback()
                    flash('Erro: {}'.format(response.status_code), 'error') 
                    flash('Erro: {}. {}'.format(response.status_code, data['message']), 'error') 
                    return render_template('login.html', form=form)
                else:
                    db.session.commit()
                    return redirect(url_for('login.login')) 
            except Exception as e:
                db.session.rollback()
                flash('Erro: {}'.format(e), 'error')  
        return render_template('register.html', form=form)   

    @login_bp.route('/login', methods=['GET', 'POST'] )
    def login():
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate(): 
            user = User.query.filter_by(email=form.email.data).first()
            session["roles"] = 'URBANMOB_GOVERNO'
            login_user(user)
            return redirect(url_for('solicitacao.prepareSearch')) 
        else:
             return render_template('login.html', form=form)
        # ------------------------------------------------
        form = LoginForm(request.form)

        if request.method == 'POST' and form.validate(): 

            email = form.email.data
            pwd = form.password.data

            try:

                url = 'http://10.82.85.10:8080/api/caa/auth'
                data = {'email': email, 'password': pwd, 'app_key': app_key, 'type': 'WEB'}
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, json=data, headers=headers)
                data = response.json()
                #print(response.status_code)

                if(response.status_code == 200):

                    user = User.query.filter_by(email=email).first()
                    #user.roles = data['roles']

                    #print(data['roles'])

                    session["roles"] = data['roles']
                    login_user(user)
                    return redirect(url_for('solicitacao.prepareSearch')) 
                else:
                    flash('Erro: {}. {}'.format(response.status_code, data['message']), 'error') 
                    return render_template('login.html', form=form)
            except Exception as e:
                flash('Erro: {}'.format(e), 'error')             
        else:
            return render_template('login.html', form=form)
            
    @login_bp.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login.login'))

    @login_bp.route('/site')
    def site():
        logout_user()
        return redirect('/')