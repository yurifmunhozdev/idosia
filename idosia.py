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

    # Análise de Glicemia
    glicemia = dados.get('glicemia', 0)
    if glicemia > 126:
        resultados['glicemia'] = {
            'mensagem': f"Glicemia elevada ({glicemia} mg/dL) - possível diabetes",
            'status': 'alerta',
            'risco': 'Risco de complicações metabólicas'
        }
    elif glicemia > 99:
        resultados['glicemia'] = {
            'mensagem': f"Glicemia alterada ({glicemia} mg/dL) - monitorar",
            'status': 'atenção',
            'risco': 'Pré-diabetes'
        }
    else:
        resultados['glicemia'] = {
            'mensagem': f"Glicemia normal ({glicemia} mg/dL)",
            'status': 'normal',
            'risco': 'Baixo risco metabólico'
        }

    # Análise Renal
    creatinina = dados.get('creatinina', 0)
    resultados['renal'] = {
        'mensagem': f"Creatinina: {creatinina} mg/dL",
        'status': 'alerta' if creatinina > 1.2 else 'normal',
        'risco': "Função renal comprometida" if creatinina > 1.2 else "Função renal normal"
    }

    # Análise de Depressão
    depressao = dados.get('depressao', 0)
    if depressao > 5:
        resultados['depressao'] = {
            'mensagem': f"Escala de depressão: {depressao}/15 (risco elevado)",
            'status': 'alerta',
            'risco': 'Possível depressão geriátrica'
        }
    else:
        resultados['depressao'] = {
            'mensagem': f"Escala de depressão: {depressao}/15 (normal)",
            'status': 'normal',
            'risco': 'Baixo risco depressivo'
        }

    return resultados

def calcular_escore_risco(analises):
    pesos = {
        'pressao': 2,
        'colesterol': 1.5,
        'glicemia': 1.5,
        'renal': 1,
        'depressao': 1.2
    }
    
    escore = 0
    for key, valor in analises.items():
        if valor['status'] == 'alerta':
            escore += pesos.get(key, 1)
    return min(escore, 10)

def classificar_fragilidade(dados):
    criterios = 0
    if dados['imc'] < 22: criterios += 1
    if dados['depressao'] > 5: criterios += 1
    if dados['creatinina'] > 1.2: criterios += 1
    
    return {
        0: "Robusto",
        1: "Pré-frágil",
        2: "Frágil"
    }.get(criterios, "Muito frágil")

def criar_dashboard(dados):
    historico = [
        {"data": "2024-01-01", "pressao_sistolica": 130, "glicemia": 110, "imc": 25},
        {"data": "2024-02-01", "pressao_sistolica": dados['pressao_sistolica'], 
         "glicemia": dados['glicemia'], "imc": dados['imc']}
    ]
    
    df = pd.DataFrame(historico)
    
    fig = px.line(df, x="data", y=["pressao_sistolica", "glicemia", "imc"], 
                 title="Monitoramento Geriátrico",
                 labels={"value": "Valores", "variable": "Parâmetro"},
                 line_dash="variable")
    
    fig.update_layout(
        font_size=14,
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#ffffff',
        height=500,
        margin=dict(l=50, r=50, t=60, b=50),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    
    return fig.to_html(include_plotlyjs='cdn')

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

    if dados.get('imc', 0) < 22:
        recomendacoes.append("Avaliação nutricional urgente - risco de desnutrição")
    elif dados.get('imc', 0) > 27:
        recomendacoes.append("Programa de controle de peso para idosos")

    if dados.get('creatinina', 0) > 1.2:
        recomendacoes.extend([
            "Aumentar ingestão de água",
            "Evitar anti-inflamatórios",
            "Consultar nefrologista"
        ])

    if dados.get('depressao', 0) > 5:
        recomendacoes.extend([
            "Avaliação psiquiátrica recomendada",
            "Atividades sociais diárias",
            "Monitoramento do humor"
        ])

    if dados.get('glicemia', 0) > 126:
        recomendacoes.append("Teste de hemoglobina glicada (HbA1c) necessário")
    
    return recomendacoes

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        dados = {
            'idade': int(request.form.get('idade', 0)),
            'colesterol_ldl': int(request.form.get('colesterol_ldl', 0)),
            'pressao_sistolica': int(request.form.get('pressao_sistolica', 0)),
            'pressao_diastolica': int(request.form.get('pressao_diastolica', 0)),
            'glicemia': int(request.form.get('glicemia', 0)),
            'imc': float(request.form.get('imc', 0)),
            'creatinina': float(request.form.get('creatinina', 0)),
            'depressao': int(request.form.get('depressao', 0))
        }
        
        analises = analisar_dados_saude(dados)
        recomendacoes = gerar_recomendacoes(dados)
        dashboard = criar_dashboard(dados)
        escore_risco = calcular_escore_risco(analises)
        classificacao = classificar_fragilidade(dados)
        
        return render_template('index.html', 
                             mostrar_resultados=True,
                             analises=analises,
                             recomendacoes=recomendacoes,
                             dashboard=dashboard,
                             escore_risco=escore_risco,
                             classificacao=classificacao)
    
    return render_template('index.html', mostrar_resultados=False)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
