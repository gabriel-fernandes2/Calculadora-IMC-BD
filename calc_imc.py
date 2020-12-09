#Exercício – Ciclo 4 - Gabriel S. Fernandes
#Calculadora IMC Python Com Banco de Dados

import gi
import sqlite3

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
builder = Gtk.Builder()
builder.add_from_file('interface_cal_imc.glade')

class Handler(object):
    def __init__(self):
        self.peso = builder.get_object('tx_peso')
        self.altura = builder.get_object('tx_altura')
        self.nome = builder.get_object('tx_nome')
        self.endereco = builder.get_object('tx_Endereco')
        self.text_buffer = builder.get_object('textbuffer_resultado')

    def on_bt_calc_clicked(self, button, msg_tx=str):
        imc = float(self.peso.get_text()) / (float(self.altura.get_text()) **2)
        nomepessoa = str(self.nome.get_text())
        enderecopessoa = str(self.endereco.get_text())
        pesopessoa = float(self.peso.get_text())
        alturapessoa = float(self.altura.get_text())

        if imc > 0:
            if imc < 17:
                msg_tx = 'Muito abaixo do peso'
            if 17 <= imc < 18.50:
                msg_tx = 'Abaixo do Normal.'
            if 18.50 <= imc < 25:
                msg_tx = 'Peso Normal.'
            if 25 <= imc < 30:
                msg_tx = 'Acima do Peso.'
            if 30 <= imc < 35:
                msg_tx = 'Obesidade I'
            if 35 <= imc < 40:
                msg_tx = 'Obesidade II (Severa)'
            if imc > 40:
                msg_tx = 'Obesidade III (Mórbida)'


        self.text_buffer.set_text('Seu IMC é: {:.2f} \n sua situação é: {} '.format(imc, msg_tx))

        conexao = sqlite3.connect("banco_IMC.db")
        cursor = conexao.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS banco_IMC(nome text, end text,peso real,alt real, r_imc real, situacao text)")
        cursor.execute("INSERT INTO banco_IMC(nome, end, peso, alt, r_imc, situacao) VALUES(?,?,?,?,?,?)",(nomepessoa, enderecopessoa, pesopessoa, alturapessoa, imc, msg_tx))
        conexao.commit()
        cursor.close()
        conexao.close()

    def on_main_destroy(self, window):
        Gtk.main_quit()

    def on_id_sair_clicked(self, button):
        Gtk.main_quit()

    def on_bt_reiniciar_clicked(self, button):
        self.peso.set_text("")
        self.altura.set_text("")
        self.nome.set_text("")
        self.endereco.set_text("")
        self.text_buffer.set_text("Digite seus dados ao lado, depois pressione Calcular")

builder.connect_signals(Handler())
window = builder.get_object('main')
window.show_all()
Gtk.main()
