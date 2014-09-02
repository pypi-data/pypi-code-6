# -*- coding: utf-8 -*-
# TODO: Faltou adicionar o controle de produtos

from django.db import models


class DadosCobranca(models.Model):

    id = models.AutoField(db_column="dados_cobranca_id", primary_key=True)
    forma_pagamento = models.CharField(db_column="dados_cobranca_forma_pagamento")
    tipo_pessoa = models.CharField(db_column="dados_cobranca_tipo_pessoa")
    email_nfe = models.CharField(db_column="dados_cobranca_email_nfe")
    nome_responsavel = models.CharField(db_column="dados_cobranca_nome_responsavel")
    cpf = models.CharField(db_column="dados_cobranca_cpf")
    razao_social = models.CharField(db_column="dados_cobranca_razao_social")
    cnpj = models.CharField(db_column="dados_cobranca_cnpj")
    telefone_principal = models.CharField(db_column="dados_cobranca_telefone_principal")
    telefone_alternativo = models.CharField(db_column="dados_cobranca_telefone_alternativo")
    endereco_logradouro = models.CharField(db_column="dados_cobranca_endereco_logradouro")
    endereco_numero = models.CharField(db_column="dados_cobranca_endereco_numero")
    endereco_complemento = models.CharField(db_column="dados_cobranca_endereco_complemento")
    endereco_bairro = models.CharField(db_column="dados_cobranca_endereco_bairro")
    endereco_cidade_ibge = models.CharField(db_column="dados_cobranca_endereco_cidade_ibge")
    endereco_estado = models.CharField(db_column="dados_cobranca_endereco_estado")
    endereco_cep = models.CharField(db_column="dados_cobranca_endereco_cep")

    conta = models.ForeignKey("plataforma.Conta", db_column="conta_id")
    contrato = models.ForeignKey("plataforma.Contrato", db_column="contrato_id")

    class Meta:
        db_table = u"faturamento\".\"tb_dados_cobranca"


class DadosCobrancaCartao(models.Model):
    """Guarda os dados do cartão de crédito da conta.

    Os dados são guardados criptografados e só o executor da tarefas de
    pagamento tem permissão para decriptografar os dados.
    """

    id = models.AutoField(db_column="dados_cobranca_cartao_id", primary_key=True)
    nome_portador = models.CharField(db_column="dados_cobranca_cartao_nome_portador",)
    numero = models.CharField(db_column="dados_cobranca_cartao_numero", max_length=64, null=False)
    cvv = models.CharField(db_column="dados_cobranca_cartao_cvv", max_length=64, null=False)
    expiracao_mes = models.CharField(db_column="dados_cobranca_cartao_expiracao_mes", max_length=255, null=False)
    expiracao_ano = models.CharField(db_column="dados_cobranca_cartao_expiracao_ano", max_length=255, null=False)
    ultimos_numeros = models.CharField(db_column="dados_cobranca_cartao_ultimos_numeros", max_length=255, null=False)
    data_criacao = models.DateTimeField(db_column="dados_cobranca_cartao_data_criacao", auto_now_add=True)
    data_modificacao = models.DateTimeField(db_column="dados_cobranca_cartao_data_modificacao", auto_now=True)

    conta = models.ForeignKey("plataforma.Conta", db_column="conta_id")
    contrato = models.ForeignKey("plataforma.Contrato", db_column="contrato_id")
    dados_cobranca = models.ForeignKey("DadosCobranca", db_column="dados_cobranca_id")

    class Meta:
        db_table = u"faturamento\".\"tb_dados_cobranca_cartao"


class Fatura(models.Model):

    id = models.AutoField(db_column="fatura_id", primary_key=True)
    situacao = models.CharField(db_column="fatura_situacao")
    data_vencimento = models.DateField(db_column="fatura_data_vencimento")
    data_tolerancia = models.DateField(db_column="fatura_data_tolerancia")
    data_pagamento = models.DateField(db_column="fatura_data_pagamento", default=None)
    valor_pcc_imposto = models.DecimalField(db_column="fatura_valor_pcc_imposto", decimal_places=2, max_digits=12)
    valor_total = models.DecimalField(db_column="fatura_valor_total", decimal_places=2, max_digits=12)
    valor_desconto = models.DecimalField(db_column="fatura_valor_desconto", decimal_places=2, max_digits=12)
    valor_subtotal = models.DecimalField(db_column="fatura_valor_subtotal", decimal_places=2, max_digits=12)
    dados_forma_pagamento = models.CharField(db_column="fatura_dados_forma_pagamento")
    dados_tipo_pessoa = models.CharField(db_column="fatura_dados_tipo_pessoa")
    dados_email_nfe = models.CharField(db_column="fatura_dados_email_nfe")
    dados_nome_responsavel = models.CharField(db_column="fatura_dados_nome_responsavel")
    dados_cpf = models.CharField(db_column="fatura_dados_cpf", default=None)
    dados_razao_social = models.CharField(db_column="fatura_dados_razao_social", default=None)
    dados_cnpj = models.CharField(db_column="fatura_dados_cnpj", default=None)
    dados_telefone_principal = models.CharField(db_column="fatura_dados_telefone_principal", default=None)
    dados_telefone_alternativo = models.CharField(db_column="fatura_dados_telefone_alternativo", default=None)
    dados_endereco_logradouro = models.CharField(db_column="fatura_dados_endereco_logradouro")
    dados_endereco_numero = models.CharField(db_column="fatura_dados_endereco_numero")
    dados_endereco_complemento = models.CharField(db_column="fatura_dados_endereco_complemento", default=None)
    dados_endereco_bairro = models.CharField(db_column="fatura_dados_endereco_bairro")
    dados_endereco_cidade_ibge = models.CharField(db_column="fatura_dados_endereco_cidade_ibge")
    dados_endereco_estado = models.CharField(db_column="fatura_dados_endereco_estado")
    dados_endereco_cep = models.CharField(db_column="fatura_dados_endereco_cep")
    boleto_codigo_de_barras = models.CharField(db_column="fatura_boleto_codigo_de_barras", default=None)
    boleto_url = models.CharField(db_column="fatura_boleto_url", default=None)
    cartao_de_credito_cv = models.CharField(db_column="fatura_cartao_de_credito_cv")
    cartao_de_credito_numero = models.CharField(db_column="fatura_cartao_de_credito_numero")
    controle_lancamento_numero = models.IntegerField(db_column="fatura_controle_lancamento_numero", default=None)
    controle_quitada = models.IntegerField(db_column="fatura_controle_quitada", default=None)
    controle_nota_fiscal = models.IntegerField(db_column="fatura_controle_nota_fiscal", default=None)
    data_criacao = models.DateTimeField(db_column="fatura_data_criacao", auto_now_add=True)
    data_modificacao = models.DateTimeField(db_column="fatura_data_modificacao", auto_now=True)

    conta = models.ForeignKey("plataforma.Conta", db_column="conta_id")
    contrato = models.ForeignKey("plataforma.Contrato", db_column="contrato_id")

    class Meta:
        db_table = u"faturamento\".\"tb_fatura"


class FaturaItem(models.Model):

    id = models.AutoField(db_column="fatura_item_id", primary_key=True)
    valor = models.DecimalField(db_column="fatura_item_valor", decimal_places=2, max_digits=12)
    referencia_tabela = models.CharField(db_column="fatura_item_referencia_tabela")
    referencia_campo = models.CharField(db_column="fatura_item_referencia_campo")
    referencia_id = models.IntegerField(db_column="fatura_item_referencia_id")

    conta = models.ForeignKey("plataforma.Conta", db_column="conta_id")
    contrato = models.ForeignKey("plataforma.Contrato", db_column="contrato_id")
    fatura = models.ForeignKey("Fatura", db_column="fatura_id")

    class Meta:
        db_table = u"faturamento\".\"tb_fatura_item"


class Colecao(models.Model):

    id = models.AutoField(db_column="colecao_id", primary_key=True)
    nome = models.TextField(db_column="colecao_nome")
    data_criacao = models.DateTimeField(db_column="colecao_data_criacao", auto_now_add=True)
    data_modificacao = models.DateTimeField(db_column="colecao_data_modificacao", auto_now=True)

    class Meta:
        db_table = u"faturamento\".\"tb_colecao"


class Plano(models.Model):

    id = models.AutoField(db_column="plano_id", primary_key=True)
    nome = models.TextField(db_column="plano_nome")
    valor = models.DecimalField(db_column="plano_valor")
    indice = models.IntegerField(db_column="plano_indice", default=0)
    intervalo = models.IntegerField(db_column="plano_intervalo", default=0)
    controle_trafego = models.IntegerField(db_column="plano_controle_trafego", default=0)
    controle_visitas = models.IntegerField(db_column="plano_controle_visitas", default=0)
    controle_produtos = models.IntegerField(db_column="plano_controle_produtos", default=0)
    data_criacao = models.DateTimeField(db_column="plano_data_criacao", auto_now_add=True)
    data_modificacao = models.DateTimeField(db_column="plano_data_modificacao", auto_now=True)

    colecao = models.ForeignKey("Colecao", db_column="colecao_id")

    class Meta:
        app_label = 'faturamento'
        db_table = u"faturamento\".\"tb_plano"


class PlanoAssinatura(models.Model):

    id = models.AutoField(db_column="plano_assinatura_id", primary_key=True)
    acao = models.TextField(db_column="plano_assinatura_acao", default='MANTEVE')
    ciclo_inicio = models.DateField(db_column="plano_assinatura_ciclo_inicio")
    ciclo_fim = models.DateField(db_column="plano_assinatura_ciclo_fim")
    controle_trafego = models.IntegerField(db_column="plano_assinatura_controle_trafego", default=0)
    controle_visitas = models.IntegerField(db_column="plano_assinatura_controle_visitas", default=0)
    controle_produtos = models.IntegerField(db_column="plano_assinatura_controle_produtos", default=0)
    data_criacao = models.DateTimeField(db_column="plano_assinatura_data_criacao", auto_now_add=True)
    data_modificacao = models.DateTimeField(db_column="plano_assinatura_data_modificacao", auto_now=True)

    conta = models.ForeignKey("plataforma.Conta", db_column="conta_id")
    contrato = models.ForeignKey("plataforma.Contrato", db_column="contrato_id")
    plano = models.ForeignKey("Plano", db_column="plano_id")
    fatura = models.ForeignKey("Fatura", db_column="fatura_id")

    class Meta:
        db_table = u"faturamento\".\"tb_plano_assinatura"
