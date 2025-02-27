from flask import Flask, render_template, request
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import random

app = Flask(__name__)

def analisar_dados_saude(dados):
    resultados = {}
    
    # Análise de Pressão Arterial
    ps = dados.get('pressao_sistolica', 0)
    pd = dados.get('pressao_diastolica', 0)
    if ps > 140 or pd > 90:
        resultados['pressao'] = {
            'status': 'alerta',
            'mensagem': f"Atenção! Sua pressão {ps}/{pd} mmHg está acima do ideal (120/80).",
            'risco': "Alto risco cardiovascular"
        }
    else:
        resultados['pressao'] = {
            'status': 'normal',
            'mensagem': f"Sua pressão {ps}/{pd} mmHg está dentro dos valores normais.",
            'risco': "Risco cardiovascular normal"
        }

    # Análise de Colesterol
    ldl = dados.get('colesterol_ldl', 0)
    if ldl > 130:
        resultados['colesterol'] = {
            'status': 'alerta',
            'mensagem': f"Atenção! Seu colesterol LDL de {ldl} mg/dL está alto.",
            'risco': "Alto risco cardiovascular"
        }
    else:
        resultados['colesterol'] = {
            'status': 'normal',
            'mensagem': f"Seu colesterol LDL de {ldl} mg/dL está em níveis adequados.",
            'risco': "Risco normal"
        }

    # Análise de Glicose
    glicose = dados.get('glicose_jejum', 0)
    if glicose > 99:
        resultados['glicose'] = {
            'status': 'alerta',
            'mensagem': f"Atenção! Sua glicose em jejum de {glicose} mg/dL está elevada.",
            'risco': "Risco de diabetes"
        }
    else:
        resultados['glicose'] = {
            'status': 'normal',
            'mensagem': f"Sua glicose em jejum de {glicose} mg/dL está normal.",
            'risco': "Risco metabólico normal"
        }

    # Análise de Frequência Cardíaca
    fc = dados.get('freq_cardiaca', 0)
    if fc > 100:
        resultados['freq_cardiaca'] = {
            'status': 'alerta',
            'mensagem': f"Atenção! Sua frequência cardíaca de {fc} bpm está elevada.",
            'risco': "Risco cardiovascular aumentado"
        }
    else:
        resultados['freq_cardiaca'] = {
            'status': 'normal',
            'mensagem': f"Sua frequência cardíaca de {fc} bpm está normal.",
            'risco': "Risco normal"
        }

    return resultados

def criar_dashboard(dados):
    datas = [(datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(30, 0, -5)]
    
    historico = []
    for data in datas:
        historico.append({
            "data": data,
            "pressao_sistolica": dados['pressao_sistolica'] + random.randint(-10, 10),
            "pressao_diastolica": dados['pressao_diastolica'] + random.randint(-5, 5),
            "glicose": dados.get('glicose_jejum', 100) + random.randint(-10, 10),
            "freq_cardiaca": dados.get('freq_cardiaca', 80) + random.randint(-5, 5)
        })
    
    df = pd.DataFrame(historico)
    
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=("Pressão Arterial", "Glicose em Jejum", "Frequência Cardíaca"),
        vertical_spacing=0.12
    )
    
    fig.add_trace(
        go.Scatter(x=df["data"], y=df["pressao_sistolica"], name="Sistólica",
                  line=dict(color="#2196F3")), row=1, col=1)
    fig.add_trace(
        go.Scatter(x=df["data"], y=df["pressao_diastolica"], name="Diastólica",
                  line=dict(color="#E91E63")), row=1, col=1)
    
    fig.add_trace(
        go.Scatter(x=df["data"], y=df["glicose"], name="Glicose",
                  line=dict(color="#4CAF50")), row=2, col=1)
    
    fig.add_trace(
        go.Scatter(x=df["data"], y=df["freq_cardiaca"], name="BPM",
                  line=dict(color="#FF9800")), row=3, col=1)
    
    fig.update_layout(
        height=800,
        showlegend=True,
        title_text="Dashboard de Saúde",
        font=dict(size=14),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig.to_html()

def gerar_recomendacoes(dados):
    recomendacoes = []
    
    if dados.get('pressao_sistolica', 0) > 140 or dados.get('pressao_diastolica', 0) > 90:
        recomendacoes.extend([
            "Reduza o consumo de sal",
            "Pratique atividades físicas moderadas",
            "Monitore sua pressão regularmente",
            "Mantenha uma alimentação equilibrada",
            "Evite o consumo excessivo de álcool"
        ])
    
    if dados.get('colesterol_ldl', 0) > 130:
        recomendacoes.extend([
            "Reduza o consumo de gorduras saturadas",
            "Aumente a ingestão de fibras",
            "Pratique exercícios regularmente",
            "Consuma mais alimentos ricos em ômega-3",
            "Evite alimentos processados"
        ])
    
    if dados.get('glicose_jejum', 0) > 99:
        recomendacoes.extend([
            "Controle o consumo de carboidratos",
            "Mantenha um peso saudável",
            "Faça exercícios regularmente",
            "Monitore sua glicose regularmente",
            "Consulte um endocrinologista"
        ])
    
    if dados.get('freq_cardiaca', 0) > 100:
        recomendacoes.extend([
            "Pratique técnicas de relaxamento",
            "Mantenha uma rotina regular de exercícios",
            "Evite estimulantes como cafeína",
            "Monitore sua frequência cardíaca",
            "Consulte um cardiologista"
        ])
    
    return list(set(recomendacoes))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            dados = {
                'idade': int(request.form.get('idade', 0)),
                'glicose_jejum': int(request.form.get('glicose_jejum', 0)),
                'freq_cardiaca': int(request.form.get('freq_cardiaca', 0)),
                'colesterol_ldl': int(request.form.get('colesterol_ldl', 0)),
                'pressao_sistolica': int(request.form.get('pressao_sistolica', 0)),
                'pressao_diastolica': int(request.form.get('pressao_diastolica', 0))
            }
            
            analises = analisar_dados_saude(dados)
            recomendacoes = gerar_recomendacoes(dados)
            dashboard = criar_dashboard(dados)
            
            return render_template('index.html', 
                                 mostrar_resultados=True,
                                 analises=analises,
                                 recomendacoes=recomendacoes,
                                 dashboard=dashboard)
        except ValueError:
            return render_template('index.html', 
                                 mostrar_resultados=False,
                                 erro="Por favor, preencha todos os campos corretamente.")
    
    return render_template('index.html', mostrar_resultados=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
