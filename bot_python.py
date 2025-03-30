from botcity.core import DesktopBot
import Planilha
import time
from datetime import datetime
import pandas as pd

# Caminho do arquivo da planilha
planilha = r'C:\Python\Planilha\2025 - EFD-REINF - Rendimentos Pagos_Creditados (Trivalle).xlsx'
print(planilha)

class Bot(DesktopBot):
    def action(self, execution=None):
        # Obtenha todos os dados da planilha
        CNPJ = Planilha.buscaCNPJ()  # CNPJ do Estabelecimento
        periodoEnvio = Planilha.buscaPeriodo()
        df = Planilha.buscaDados()

        # Iniciar o navegador para envio de NF
        self.browse("https://cav.receita.fazenda.gov.br/autenticacao/login")
        self.wait(2)

        # Navegação inicial
        self.navegar_inicial()

        # Processar todas as linhas da planilha
        for i, row in df.iterrows():  # Loop para percorrer todas as linhas da planilha
            cnpj = row['CNPJ do beneficiário']

            # Se o CNPJ for NaN, pula para a próxima linha
            if pd.isna(cnpj):
                print(f"Encontrou um valor NaN na linha {i + 1} na coluna 'CNPJ do beneficiário'. Pulando para a próxima linha.")
                continue  # Pula para a próxima linha

            print(f'Processando CNPJ: {cnpj}')

            # Chama a função para processar o lançamento para o beneficiário
            self.processar_lancamento(row, periodoEnvio, CNPJ)

            # Aguardar para evitar sobrecarga de requisições
            self.wait(2)

    def navegar_inicial(self):
        
        # Realiza a navegação inicial
        self.wait(2)
        if not self.find("LOGIN_GOV", matching=0.97, waiting_time=10000):
            self.not_found("LOGIN_GOV")
        self.click()
        self.wait(2)

        # Acessa o Certificado Digital, Valida e Localiza o Serviço
        if not self.find("CERTIFICADO_DIGITAL", matching=0.97, waiting_time=10000):
            self.not_found("CERTIFICADO_DIGITAL")
        self.click()
        self.wait(2)

        if not self.find("CERTIFICADO_GOINFRA", matching=0.97, waiting_time=10000):
            self.not_found("CERTIFICADO_GOINFRA")
        self.click()
        self.wait(2)

        if not self.find("VALIDA_CERTIFICADO_GOINFRA", matching=0.97, waiting_time=10000):
            self.not_found("VALIDA_CERTIFICADO_GOINFRA")
        self.click()
        self.wait(2)

        if not self.find("LOCALIZAR_SERVICO", matching=0.97, waiting_time=10000):
            self.not_found("LOCALIZAR_SERVICO")
        self.click()
        self.wait(2)
        self.paste('reinf')

        if not self.find("ACESSO_REINF", matching=0.97, waiting_time=10000):
            self.not_found("ACESSO_REINF")
        self.click()

    def processar_lancamento(self, row, periodoEnvio, CNPJ):
        cnpj = row['CNPJ do beneficiário']

        # Acessando a opção rendimentos pagos e creditados
        if not self.find("RendimentosPAGOSeCreditados", matching=0.97, waiting_time=20000):
            self.not_found("RendimentosPAGOSeCreditados")
        self.click()
        self.wait(5)

        # Clicando no ícone Incluir Pagamento Crédito
        self.click_at(601, 440)

        # Procurando o ícone beneficiário PJ
        if not self.find("Beneficiario_PJ", matching=0.97, waiting_time=10000):
            self.not_found("Beneficiario_PJ")
        self.click()
        self.wait(5)

        # Preenchendo dados
        self.preencher_dados(row, periodoEnvio, CNPJ, cnpj)

    def preencher_dados(self, row, periodoEnvio, CNPJ, cnpj):
        # Preenchendo Período de Apuração e CNPJ do Estabelecimento
        if not self.find("PERIODO_APURACAO", matching=0.97, waiting_time=10000):
            self.not_found("PERIODO_APURACAO")
        self.click()
        self.paste(periodoEnvio)  # Período de Apuração
        self.tab()
        self.paste(CNPJ)  # CNPJ do Estabelecimento
        self.tab()
        self.paste(cnpj)  # CNPJ do beneficiário
        self.tab()
        self.tab()
        self.enter()
        self.wait(1)

        # Incluir um novo beneficiário
        if not self.find("Novo_Beneficiario", matching=0.97, waiting_time=10000):
            self.not_found("Novo_Beneficiario")
        self.click()

        # Informando natureza do rendimento (Grupo de Rendimento)
        if not self.find("Grupo_de_Rendimento", matching=0.97, waiting_time=10000):
            self.not_found("Grupo_de_Rendimento")
        self.click()

        # Informando o Grupo 17
        if not self.find("Informando o Grupo 17", matching=0.97, waiting_time=10000):
            self.not_found("Informando o Grupo 17")
        self.click()

        # Natureza do Rendimento
        if not self.find("Natureza_Rendimento", matching=0.97, waiting_time=10000):
            self.not_found("Natureza_Rendimento")
        self.click_relative(28, 34)

        # Informando o código 17013
        if not self.find("Informando_17013", matching=0.97, waiting_time=10000):
            self.not_found("Informando_17013")
        self.click()

        # Salvar Natureza
        if not self.find("Salvar_Natureza", matching=0.97, waiting_time=10000):
            self.not_found("Salvar_Natureza")
        self.click()

        # Novo detalhamento de pagamento
        if not self.find("Novo_Detalhamento_Pagamento", matching=0.97, waiting_time=10000):
            self.not_found("Novo_Detalhamento_Pagamento")
        self.click()

        # Preenchendo dados financeiros
        self.preencher_detalhes_pagamento(row)

    def preencher_detalhes_pagamento(self, row):
        # Tratando a data do fato gerador
        data_original = row['Data do fato gerador']
        data_formatada = datetime.strptime(str(data_original), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
        print(data_formatada)

        # Preenchendo a data do fato gerador
        if not self.find("Data_Fato_Gerador", matching=0.97, waiting_time=10000):
            self.not_found("Data_Fato_Gerador")
        self.click_relative(9, 31)
        self.paste(data_formatada)

        # Tratando o valor da coluna "Valor Bruto"
        Valor_bruto = str(row['Valor bruto'])
        Valor_Retenção_IR = str(row['Valor da base de retenção do IR'])
        Valor_Imposto_Renda_IRRF = str(row['Valor do Imposto de Renda IRRF'])

        # Preenchendo os valores
        if not self.find("Valor_Bruto", matching=0.97, waiting_time=10000):
            self.not_found("Valor_Bruto")
        self.click_relative(21, 32)
        self.paste(Valor_bruto)

        if not self.find("Retencao_IR", matching=0.97, waiting_time=10000):
            self.not_found("Retencao_IR")
        self.click_relative(27, 29)
        self.paste(Valor_Retenção_IR)
        self.tab()
        self.paste(Valor_Imposto_Renda_IRRF)

        # Salvar detalhamento
        if not self.find("Salvar_Detalhamento", matching=0.97, waiting_time=10000):
            self.not_found("Salvar_Detalhamento")
        self.click()
        self.page_down()

        # Salvar rascunho
        if not self.find("Salvar_Rascunho", matching=0.97, waiting_time=10000):
            self.not_found("Salvar_Rascunho")
        self.click()

def voltar_rendimentos_pagos_creditados(self):
    # Tenta voltar à página "Rendimentos Pagos e Creditados"
    if not self.find("Rendimentos_Pagos_Creditados", matching=0.97, waiting_time=10000):
        self.not_found("Rendimentos_Pagos_Creditados")
        return False
    
    self.click()  # Clica para voltar à página

    # Aguardar o carregamento da página
    self.wait(3)  # Tempo para garantir que a página foi recarregada

    # Verifique se a página "Rendimentos Pagos e Creditados" foi carregada novamente
    if not self.find("Incluir_Pagamento_Credito", matching=0.97, waiting_time=10000):
        self.not_found("Incluir_Pagamento_Credito")
        return False
    
    self.click_at(601, 440)  # Clica para incluir um novo pagamento (se necessário)
    self.wait(3)  # Aguardar para garantir que a página de "Incluir Pagamento" seja carregada

    # Clica novamente em "Beneficiário PJ" ou qualquer outro botão necessário
    if not self.find("Beneficiario_PJ", matching=0.97, waiting_time=10000):
        self.not_found("Beneficiario_PJ")
    self.click()
    self.wait(5)  # Aguarda o carregamento da próxima etapa
    return True

    @staticmethod
    def not_found(label):
        print(f"Elemento não encontrado: {label}")

if __name__ == '__main__':
    Bot.main()
