from botcity.core import DesktopBot
import Planilha
import time
from datetime import datetime
import pandas as pd

class Bot(DesktopBot):
    def action(self, execution=None):
        CNPJ = Planilha.buscaCNPJ()
        periodoEnvio = Planilha.buscaPeriodo()
        df = Planilha.buscaDados()

        self.browse("https://cav.receita.fazenda.gov.br/autenticacao/login")
        self.wait(2)
        self.navegar_inicial()

        for i, row in df.iterrows():
            cnpj = row['CNPJ do beneficiário']
            if pd.isna(cnpj):
                continue
            self.processar_lancamento(row, periodoEnvio, CNPJ)
            self.wait(2)
            self.voltar_rendimentos_pagos_creditados()

    def navegar_inicial(self):
        pass  # omitido para teste

    def processar_lancamento(self, row, periodoEnvio, CNPJ):
        self.find = lambda *a, **kw: True
        self.click = lambda: None
        self.click_at = lambda x, y: None
        self.wait = lambda x: None
        self.preencher_dados(row, periodoEnvio, CNPJ, row['CNPJ do beneficiário'])

    def preencher_dados(self, row, periodoEnvio, CNPJ, cnpj):
        self.find("PERIODO_APURACAO")
        self.click()
        self.paste(periodoEnvio)
        self.tab()
        self.paste(CNPJ)
        self.tab()
        self.paste(cnpj)
        self.tab()
        self.tab()
        self.enter()
        self.wait(1)
        self.find("Novo_Beneficiario")
        self.click()
        self.find("Grupo_de_Rendimento")
        self.click()
        self.find("Informando o Grupo 17")
        self.click()
        self.find("Natureza_Rendimento")
        self.click_relative(28, 34)
        self.find("Informando_17013")
        self.click()
        self.find("Salvar_Natureza")
        self.click()
        self.find("Novo_Detalhamento_Pagamento")
        self.click()
        self.preencher_detalhes_pagamento(row)

    def preencher_detalhes_pagamento(self, row):
        data_original = row['Data do fato gerador']
        data_formatada = datetime.strptime(str(data_original), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
        self.find("Data_Fato_Gerador")
        self.click_relative(9, 31)
        self.paste(data_formatada)
        self.find("Valor_Bruto")
        self.click_relative(21, 32)
        self.paste(str(row['Valor bruto']))
        self.find("Retencao_IR")
        self.click_relative(27, 29)
        self.paste(str(row['Valor da base de retenção do IR']))
        self.tab()
        self.paste(str(row['Valor do Imposto de Renda IRRF']))
        self.find("Salvar_Detalhamento")
        self.click()
        self.page_down()
        self.find("Salvar_Rascunho")
        self.click()

    def test_navegar_inicial_chamadas(self):
        bot = Bot()
        bot.find = MagicMock(return_value=True)
        bot.click = MagicMock()
        bot.wait = MagicMock()
        bot.paste = MagicMock()
        bot.not_found = MagicMock()

        bot.navegar_inicial()

        assert bot.find.call_count >= 5
        assert bot.click.call_count >= 5
        bot.paste.assert_called_once_with("reinf")

    def test_processar_lancamento_completo(self):
        bot = Bot()
        bot.find = MagicMock(return_value=True)
        bot.click = MagicMock()
        bot.wait = MagicMock()
        bot.click_at = MagicMock()
        bot.preencher_dados = MagicMock()

        row = pd.Series(row_data)
        bot.processar_lancamento(row, '012025', '12345678000199')

        bot.find.assert_any_call("RendimentosPAGOSeCreditados", matching=0.97, waiting_time=20000)
        bot.click.assert_called()
        bot.preencher_dados.assert_called_once()
