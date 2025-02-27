from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd
import os

app = Flask(__name__)

def analisar_dados_saude(dados):
    resultados = {}
    
    # Análise de Pressão Arterial
    ps = dados.get('pressao_sistolica', 0)
    pd = dados.get('pressao_diastolica', 0)
    if ps > 140 or pd > 90:
        resultados['pressao'] = {
            'mensagem': f"Sua pressão {ps}/{pd} mmHg está acima do ideal (120/80).",
            'status': 'alerta',
            'risco': 'Risco aumentado para problemas cardiovasculares'
        }
    else:
        resultados['pressao'] = {
            'mensagem': f"Sua pressão {ps}/{pd} mmHg está dentro dos valores normais.",
            'status': 'normal',
            'risco': 'Risco cardiovascular dentro do esperado'
        }

    # Análise de Colesterol
    ldl = dados.get('colesterol_ldl', 0)
    if ldl > 130:
        resultados['colesterol'] = {
            'mensagem': f"Seu colesterol LDL de {ldl} mg/dL está alto.",
            'status': 'alerta',
            'risco': 'Risco aumentado para doenças cardiovasculares'
        }
    else:
        resultados['colesterol'] = {
            'mensagem': f"Seu colesterol LDL de {ldl} mg/dL está em níveis adequados.",
            'status': 'normal',
            'risco': 'Risco cardiovascular dentro do esperado'
        }

    return resultados

def criar_dashboard(dados):
    # Criar dados históricos simulados
    historico = [
        {"data": "2024-02-01", "pressao_sistolica": dados['pressao_sistolica'], 
         "pressao_diastolica": dados['pressao_diastolica']},
        {"data": "2024-02-15", "pressao_sistolica": dados['pressao_sistolica']-5, 
         "pressao_diastolica": dados['pressao_diastolica']-3}
    ]
    
    df = pd.DataFrame(historico)
    fig = px.line(df, x="data", y=["pressao_sistolica", "pressao_diastolica"], 
                  title="Histórico de Pressão Arterial")
    fig.update_layout(
        font_size=16,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    return fig.to_html()

def gerar_recomendacoes(dados):
    recomendacoes = []
    
    if dados.get('colesterol_ldl', 0) > 130:
        recomendacoes.extend([
            "Reduza o consumo de gorduras saturadas",
            "Aumente a ingestão de fibras",
            "Pratique exercícios regularmente"
        ])
    
    if dados.get('pressao_sistolica', 0) > 140 or dados.get('pressao_diastolica', 0) > 90:
        recomendacoes.extend([
            "Reduza o consumo de sal",
            "Pratique atividades físicas moderadas",
            "Monitore sua pressão regularmente"
        ])
    
    return recomendacoes

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        dados = {
            'idade': int(request.form.get('idade', 0)),
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
    
    return render_template('index.html', mostrar_resultados=False)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
