from flask import Flask, render_template, request, send_file, jsonify
import plotly.express as px
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import os
import requests
from sklearn.ensemble import RandomForestClassifier
import joblib
from twilio.rest import Client

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
login_manager = LoginManager(app)

def validar_dados(dados):
    erros = []
    
    if not (70 <= dados.get('pressao_sistolica', 0) <= 250):
        erros.append("Pressão sistólica fora do intervalo válido (70-250 mmHg)")
    
    if not (40 <= dados.get('pressao_diastolica', 0) <= 130):
        erros.append("Pressão diastólica fora do intervalo válido (40-130 mmHg)")
    
    if not (50 <= dados.get('colesterol_ldl', 0) <= 300):
        erros.append("Colesterol LDL fora do intervalo válido (50-300 mg/dL)")
    
    if not (0.5 <= dados.get('creatinina', 0) <= 5.0):
        erros.append("Creatinina fora do intervalo válido (0.5-5.0 mg/dL)")
    
    return erros

def prever_risco_cardiaco(dados):
    try:
        modelo = joblib.load('modelo_risco_cardiaco.pkl')
        features = [[
            dados['idade'], 
            dados['pressao_sistolica'], 
            dados['colesterol_ldl']
        ]]
        return modelo.predict_proba(features)[0][1]
    except:
        return 0.5  # valor padrão se o modelo falhar

def enviar_alerta_sms(numero, mensagem):
    try:
        account_sid = os.environ.get('TWILIO_SID')
        auth_token = os.environ.get('TWILIO_TOKEN')
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=mensagem,
            from_=os.environ.get('TWILIO_PHONE'),
            to=numero
        )
        return message.sid
    except Exception as e:
        print(f"Erro ao enviar SMS: {e}")
        return None

def obter_dicas_nutricao():
    try:
        response = requests.get('https://api.nutritionix.com/v1_1/search', 
            params={
                'appId': os.environ.get('NUTRITION_APP_ID'),
                'appKey': os.environ.get('NUTRITION_APP_KEY'),
                'query': 'dietas para idosos'
            })
        return response.json()['hits'][:3]
    except:
        return []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        dados = {
            'idade': int(request.form.get('idade', 0)),
            'colesterol_ldl': int(request.form.get('colesterol_ldl', 0)),
            'pressao_sistolica': int(request.form.get('pressao_sistolica', 0)),
            'pressao_diastolica': int(request.form.get('pressao_diastolica', 0)),
            'creatinina': float(request.form.get('creatinina', 0))
        }
        
        erros = validar_dados(dados)
        if erros:
            return render_template('index.html', erros=erros)
        
        analises = analisar_dados_saude(dados)
        recomendacoes = gerar_recomendacoes(dados)
        dashboard = criar_dashboard_avancado(dados)
        risco_cardiaco = prever_risco_cardiaco(dados)
        dicas_nutricao = obter_dicas_nutricao()
        
        if current_user.is_authenticated:
            historico = Historico(
                user_id=current_user.id,
                parametros=dados
            )
            db.session.add(historico)
            db.session.commit()
        
        return render_template('index.html', 
                             mostrar_resultados=True,
                             analises=analises,
                             recomendacoes=recomendacoes,
                             dashboard=dashboard,
                             risco_cardiaco=risco_cardiaco,
                             dicas_nutricao=dicas_nutricao)
    
    return render_template('index.html', mostrar_resultados=False)

@app.route('/historico')
def historico():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    historico = Historico.query.filter_by(user_id=current_user.id).all()
    return render_template('historico.html', historico=historico)

if __name__ == '__main__':
    app.run(debug=True)
