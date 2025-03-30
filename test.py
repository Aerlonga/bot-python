import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import pandas as pd

# ------------------------------
# Dados de teste
# ------------------------------
row_data = {
    'CNPJ do beneficiário': '98765432000188',
    'Data do fato gerador': '2025-01-15 00:00:00',
    'Valor bruto': 1000.00,
    'Valor da base de retenção do IR': 800.00,
    'Valor do Imposto de Renda IRRF': 120.00
}

# ------------------------------
# Classe Bot original (sem DesktopBot)
# ------------------------------
class Bot:
    def browse(self, url): pass
    def wait(self, seconds): pass
    def navegar_inicial(self): pass
    def find(self, *args, **kwargs): return True
    def click(self): pass
    def click_at(self, x, y): pass
    def click_relative(self, x, y): pass
    def paste(self, value): pass
    def tab(self): pass
    def enter(self): pass
    def page_down(self): pass
    def voltar_rendimentos_pagos_creditados(self): return True

    def action(self, execution=None):
        import Planilha
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

    def processar_lancamento(self, row, periodoEnvio, CNPJ):
        self.preencher_dados(row, periodoEnvio, CNPJ, row['CNPJ do beneficiário'])

    def preencher_dados(self, row, periodoEnvio, CNPJ, cnpj):
        self.paste(periodoEnvio)
        self.tab()
        self.paste(CNPJ)
        self.tab()
        self.paste(cnpj)
        self.tab()
        self.tab()
        self.enter()
        self.wait(1)
        self.preencher_detalhes_pagamento(row)

    def preencher_detalhes_pagamento(self, row):
        data_original = row['Data do fato gerador']
        data_formatada = datetime.strptime(str(data_original), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
        self.paste(data_formatada)
        self.paste(str(row['Valor bruto']))
        self.paste(str(row['Valor da base de retenção do IR']))
        self.paste(str(row['Valor do Imposto de Renda IRRF']))

# ------------------------------
# Subclasse para testar o loop
# ------------------------------
class BotTestLoop(Bot):
    def __init__(self):
        super().__init__()
        self.contador = 0
        self.rows_processados = []

    def processar_lancamento(self, row, periodoEnvio, CNPJ):
        self.contador += 1
        self.rows_processados.append(row['CNPJ do beneficiário'])

    def voltar_rendimentos_pagos_creditados(self):
        return True

    def browse(self, url): pass
    def wait(self, seconds): pass
    def navegar_inicial(self): pass

# ------------------------------
# Testes
# ------------------------------
class TestBot(unittest.TestCase):

    def test_loop_action_com_3_linhas(self):
        mock_df = pd.DataFrame([
            {**row_data, 'CNPJ do beneficiário': '11111111000191'},
            {**row_data, 'CNPJ do beneficiário': None},
            {**row_data, 'CNPJ do beneficiário': '22222222000191'},
        ])

        with patch('Planilha.buscaDados', return_value=mock_df), \
             patch('Planilha.buscaPeriodo', return_value='012025'), \
             patch('Planilha.buscaCNPJ', return_value='12345678000199'):

            bot = BotTestLoop()
            bot.action()

            self.assertEqual(bot.contador, 2)
            self.assertEqual(
                bot.rows_processados,
                ['11111111000191', '22222222000191']
            )

    @patch('Planilha.buscaDados')
    @patch('Planilha.buscaPeriodo')
    @patch('Planilha.buscaCNPJ')
    def test_action_com_mock(self, mock_buscaCNPJ, mock_buscaPeriodo, mock_buscaDados):
        mock_buscaCNPJ.return_value = '12345678000199'
        mock_buscaPeriodo.return_value = '012025'
        mock_buscaDados.return_value = pd.DataFrame([row_data])

        bot = Bot()
        bot.browse = MagicMock()
        bot.wait = MagicMock()
        bot.navegar_inicial = MagicMock()
        bot.processar_lancamento = MagicMock()
        bot.voltar_rendimentos_pagos_creditados = MagicMock(return_value=True)

        bot.action()

        bot.browse.assert_called_once_with("https://cav.receita.fazenda.gov.br/autenticacao/login")
        bot.navegar_inicial.assert_called_once()
        bot.processar_lancamento.assert_called_once()
        bot.voltar_rendimentos_pagos_creditados.assert_called_once()

    def test_processar_lancamento(self):
        bot = Bot()
        bot.preencher_dados = MagicMock()
        bot.processar_lancamento(pd.Series(row_data), '012025', '12345678000199')
        bot.preencher_dados.assert_called_once()

    def test_preencher_dados(self):
        bot = Bot()
        for attr in ['paste', 'tab', 'enter', 'wait']:
            setattr(bot, attr, MagicMock())
        bot.preencher_detalhes_pagamento = MagicMock()
        bot.preencher_dados(pd.Series(row_data), '012025', '12345678000199', row_data['CNPJ do beneficiário'])
        bot.preencher_detalhes_pagamento.assert_called_once()

    def test_preencher_detalhes_pagamento(self):
        bot = Bot()
        bot.paste = MagicMock()
        bot.preencher_detalhes_pagamento(pd.Series(row_data))
        self.assertEqual(bot.paste.call_count, 4)

    def test_action_com_valor_nan(self):
        linha_com_nan = row_data.copy()
        linha_com_nan['CNPJ do beneficiário'] = None
        mock_df = pd.DataFrame([linha_com_nan])

        with patch('Planilha.buscaDados', return_value=mock_df), \
             patch('Planilha.buscaPeriodo', return_value='012025'), \
             patch('Planilha.buscaCNPJ', return_value='12345678000199'):

            bot = Bot()
            bot.browse = MagicMock()
            bot.wait = MagicMock()
            bot.navegar_inicial = MagicMock()
            bot.processar_lancamento = MagicMock()
            bot.voltar_rendimentos_pagos_creditados = MagicMock()

            bot.action()

            bot.processar_lancamento.assert_not_called()
            bot.voltar_rendimentos_pagos_creditados.assert_not_called()

    def test_action_com_varias_linhas(self):
        mock_df = pd.DataFrame([
            row_data,
            {**row_data, 'CNPJ do beneficiário': '00000000000191'},
        ])

        with patch('Planilha.buscaDados', return_value=mock_df), \
             patch('Planilha.buscaPeriodo', return_value='012025'), \
             patch('Planilha.buscaCNPJ', return_value='12345678000199'):

            bot = Bot()
            bot.browse = MagicMock()
            bot.wait = MagicMock()
            bot.navegar_inicial = MagicMock()
            bot.processar_lancamento = MagicMock()
            bot.voltar_rendimentos_pagos_creditados = MagicMock()

            bot.action()

            self.assertEqual(bot.processar_lancamento.call_count, 2)
            self.assertEqual(bot.voltar_rendimentos_pagos_creditados.call_count, 2)

if __name__ == '__main__':
    unittest.main()
