import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Leitura da feature flag via variável de ambiente (Default: False (Desativado))
# Permitirá alterar o comportamento da aplicação

FEATURE_DESCONTO_PROMO = os.getenv('FEATURE_DESCONTO_PROMO', 'False').lower() == 'true'

@app.route('/')
def home():
    return jsonify({"mensagem": "Bem-vindo à API integracao!"})

@app.route('/api/status')
def status():
    return jsonify({
        "status": "operacional",
        "servico": "integracao-Web",
        "flags" : {
            "desconto_promo": FEATURE_DESCONTO_PROMO
        }
    })
# TODO: Missão 5.1 - Criar uma nova rota chamada /api/soma
# Ela deve receber dois parâmetros via Query String (?a=2&b=3)
# E retornar um JSON no formato {"resultado": 5}

@app.route('/api/soma')
def soma():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    
    if a is None or b is None:
        return jsonify({"erro": "Parâmetros 'a' e 'b' são obrigatórios."}), 400
    
    resultado = a + b
    return jsonify({"resultado": resultado})

# Nova rota - Protegida pela Feature Flag
@app.route('/api/desconto')
def desconto():
    if not FEATURE_DESCONTO_PROMO:
        return jsonify({
            "erro": "Funcionalidade em construção ou desativada temporariamente.",
            "flag_status": False
        }), 403

    try:
        valor_total = float(request.args.get('valor', 0))
        porcentagem = float(request.args.get('porcentagem', 10))
    
        if valor_total <= 0:
            return jsonify({"erro": "Valor deve ser maior que zero."}), 400
        valor_com_desconto = valor_total - (valor_total * (porcentagem / 100))
        return jsonify({
            "valor_original": valor_total,
            "porcentagem": f"{porcentagem}%",
            "valor_final": valor_com_desconto
        })

    except (ValueError, TypeError):
        return jsonify({"erro": "Parâmetros de desconto inválidos."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  