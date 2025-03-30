import pandas as pd

def buscaCNPJ():
    return "12.345.678/0001-90"  # valor fixo só pra simular

def buscaPeriodo():
    return "01/2025"  # valor fixo também

def buscaDados():
    # Simula uma planilha com 2 registros de teste
    dados = {
        'CNPJ do beneficiário': ['11.222.333/0001-44', '55.666.777/0001-88'],
        'Data do fato gerador': ['2025-01-10 00:00:00', '2025-01-15 00:00:00'],
        'Valor bruto': [1000.0, 2000.0],
        'Valor da base de retenção do IR': [800.0, 1600.0],
        'Valor do Imposto de Renda IRRF': [150.0, 300.0]
    }
    df = pd.DataFrame(dados)
    return df
