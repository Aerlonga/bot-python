from datetime import datetime
import pandas as pd
import time

# Simulação do Planilha.py
def buscaCNPJ():
    return "12.345.678/0001-90"

def buscaPeriodo():
    return "03/2025"

def buscaDados():
    dados = {
        'CNPJ do beneficiário': ['11.111.111/0001-11', '', '22.222.222/0001-22', None],
        'Data do fato gerador': ['2025-03-01 00:00:00', '2025-03-02 00:00:00', '2025-03-03 00:00:00', '2025-03-04 00:00:00'],
        'Valor bruto': [1000.0, 2000.0, 3000.0, 4000.0],
        'Valor da base de retenção do IR': [900.0, 1800.0, 2700.0, 3600.0],
        'Valor do Imposto de Renda IRRF': [100.0, 200.0, 300.0, 400.0],
    }
    return pd.DataFrame(dados)

# Simulação do bot
class BotSimulado:
    def action(self):
        print("\n=== INÍCIO DA EXECUÇÃO DO BOT SIMULADO ===\n")

        CNPJ = buscaCNPJ()
        periodoEnvio = buscaPeriodo()
        df = buscaDados()

        print(f"[INFO] Período de envio: {periodoEnvio}")
        print(f"[INFO] CNPJ do estabelecimento: {CNPJ}")
        print(f"[INFO] Linhas encontradas na planilha: {len(df)}\n")

        self.navegar_inicial()

        for i, row in df.iterrows():
            cnpj = row['CNPJ do beneficiário']

            if pd.isna(cnpj) or str(cnpj).strip().lower() in ['', 'nan']:
                print(f"[{i + 1}] CNPJ vazio ou inválido. Pulando.")
                continue

            print(f"[{i + 1}] Processando CNPJ: {cnpj}")
            self.processar_lancamento(row, periodoEnvio, CNPJ)
            self.wait(2)

            # Voltar à tela de rendimentos pagos para o próximo lançamento
            self.voltar_rendimentos_pagos_creditados()

        print("\n=== FIM DA EXECUÇÃO DO BOT SIMULADO ===")

    def wait(self, segundos):
        time.sleep(segundos)

    def navegar_inicial(self):
        print("[BOT SIMULADO] Acessando página de login...")
        print("[BOT SIMULADO] Clicando em LOGIN_GOV")
        print("[BOT SIMULADO] Clicando em CERTIFICADO_DIGITAL")
        print("[BOT SIMULADO] Clicando em CERTIFICADO_GOINFRA")
        print("[BOT SIMULADO] Validando certificado e localizando serviço...")
        print("[BOT SIMULADO] Acessando 'reinf'")

    def processar_lancamento(self, row, periodoEnvio, CNPJ):
        cnpj = row['CNPJ do beneficiário']
        print(f"[BOT SIMULADO] Processando lançamento para o CNPJ: {cnpj}")
        print("[BOT SIMULADO] Acessando 'Rendimentos Pagos e Creditados'")
        print("[BOT SIMULADO] Clicando em 'Incluir Pagamento Crédito'")
        print("[BOT SIMULADO] Selecionando 'Beneficiário PJ'")
        self.preencher_dados(row, periodoEnvio, CNPJ, cnpj)

    def preencher_dados(self, row, periodoEnvio, CNPJ, cnpj):
        print(f"[BOT SIMULADO] Preenchendo período: {periodoEnvio}")
        print(f"[BOT SIMULADO] Preenchendo CNPJ do estabelecimento: {CNPJ}")
        print(f"[BOT SIMULADO] Preenchendo CNPJ do beneficiário: {cnpj}")
        print("[BOT SIMULADO] Clicando em 'Novo Beneficiário'")
        print("[BOT SIMULADO] Selecionando grupo de rendimento: Grupo 17")
        print("[BOT SIMULADO] Selecionando natureza do rendimento: Código 17013")
        print("[BOT SIMULADO] Salvando natureza")
        print("[BOT SIMULADO] Clicando em 'Novo Detalhamento de Pagamento'")
        self.preencher_detalhes_pagamento(row)

    def preencher_detalhes_pagamento(self, row):
        data_original = row['Data do fato gerador']
        data_formatada = datetime.strptime(str(data_original), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
        print(f"[BOT SIMULADO] Preenchendo data do fato gerador: {data_formatada}")

        valor_bruto = str(row['Valor bruto'])
        valor_retencao_ir = str(row['Valor da base de retenção do IR'])
        valor_irrf = str(row['Valor do Imposto de Renda IRRF'])

        print(f"[BOT SIMULADO] Preenchendo valor bruto: {valor_bruto}")
        print(f"[BOT SIMULADO] Preenchendo base de retenção IR: {valor_retencao_ir}")
        print(f"[BOT SIMULADO] Preenchendo IRRF: {valor_irrf}")

        print("[BOT SIMULADO] Salvando detalhamento")
        print("[BOT SIMULADO] Salvando rascunho")

    def voltar_rendimentos_pagos_creditados(self):
        print("\n[BOT SIMULADO] Tentando voltar para 'Rendimentos Pagos e Creditados'...")
        print("[BOT SIMULADO] Verificando botão 'Rendimentos_Pagos_Creditados'")
        print("[BOT SIMULADO] Clicando em 'Rendimentos_Pagos_Creditados'")
        self.wait(3)
        print("[BOT SIMULADO] Clicando em 'Incluir Pagamento Crédito'")
        self.wait(3)
        print("[BOT SIMULADO] Clicando novamente em 'Beneficiário PJ'")
        self.wait(5)
        return True


if __name__ == '__main__':
    # Criar planilha de teste antes de rodar o bot
    df_planilha = buscaDados()
    caminho = 'Planilha_Rendimentos_Teste.xlsx'
    df_planilha.to_excel(caminho, index=False)
    print(f"\nArquivo gerado para testes: {caminho}")

    # Rodar o bot simulado
    BotSimulado().action()

