# -*- coding: utf-8 -*-

from django.db import models
from jsonfield import JSONField


class FormaPagamento(models.Model):
    """Forma de pagamento."""

    CODIGOS_GATEWAYS = ['pagseguro', 'pagamento_digital', 'mercado_pago', 'paypal']

    PRINCIPAIS_FORMAS_PAGAMENTO = {
        'pagamento_digital': {
            'cartoes': ['visa', 'mastercard', 'hipercard', 'amex'],
            'bancos': ['itau', 'bradesco', 'banco-do-brasil'],
            'outros': ['boleto']
        },
        'pagseguro': {
            'cartoes': ['visa', 'mastercard', 'hipercard', 'amex'],
            'bancos': ['itau', 'bradesco', 'banco-do-brasil'],
            'outros': ['boleto']
        },
        'paypal': {
            'cartoes': ['visa', 'mastercard', 'amex']
        },
        'mercado_pago': {
            'cartoes': ['visa', 'mastercard', 'amex', 'elo'],
            'outros': ['boleto']
        }
    }

    id = models.AutoField(db_column="pagamento_id", primary_key=True)
    nome = models.CharField(db_column="pagamento_nome", max_length=128)
    codigo = models.CharField(db_column="pagamento_codigo", max_length=128, unique=True)
    ativo = models.BooleanField(db_column="pagamento_ativado", default=False)
    valor_minimo_parcela = models.DecimalField(db_column='pagamento_parcela_valor_minimo_parcela', max_digits=16, decimal_places=2, null=True)
    valor_minimo_parcelamento = models.DecimalField(db_column='pagamento_parcela_valor_minimo', max_digits=16, decimal_places=2, null=True)
    plano_indice = models.IntegerField(db_column='pagamento_plano_indice', default=1)
    posicao = models.IntegerField(db_column='pagamento_posicao', default=1000, null=False)

    conta = models.ForeignKey("plataforma.Conta", related_name="formas_pagamentos", null=True, default=None)
    contrato = models.ForeignKey("plataforma.Contrato", related_name="formas_pagamentos", null=True, default=None)

    class Meta:
        db_table = u"configuracao\".\"tb_pagamento"
        verbose_name = u"Forma de pagamento"
        verbose_name_plural = u"Formas de pagamentos"
        ordering = ["posicao", "nome"]

    def __unicode__(self):
        return self.nome


class FormaPagamentoConfiguracao(models.Model):
    """Configuração da forma de pagamento."""
    TIPO_VALOR_FIXO = 'fixo'
    TIPO_PORCENTAGEM = 'porcentagem'

    id = models.AutoField(db_column="pagamento_configuracao_id", primary_key=True)
    usuario = models.CharField(db_column="pagamento_configuracao_usuario", max_length=128, null=True)
    senha = models.CharField(db_column="pagamento_configuracao_senha", max_length=128, null=True)
    token = models.CharField(db_column="pagamento_configuracao_token", max_length=128, null=True)
    assinatura = models.CharField(db_column="pagamento_configuracao_assinatura", max_length=128, null=True)
    codigo_autorizacao = models.CharField(db_column="pagamento_configuracao_codigo_autorizacao", max_length=128, null=True)
    aplicacao = models.CharField(db_column="pagamento_configuracao_aplicacao_id", max_length=128, null=True, default=None)
    ativo = models.BooleanField(db_column="pagamento_configuracao_ativo", default=False)
    mostrar_parcelamento = models.BooleanField(db_column='pagamento_coonfiguracao_mostrar_parcelamento', default=False, null=False)
    maximo_parcelas = models.IntegerField(db_column="pagamento_configuracao_quantidade_parcela_maxima", default=None, null=True)
    parcelas_sem_juros = models.IntegerField(db_column="pagamento_configuracao_quantidade_parcela_sem_juros", default=None, null=True)
    desconto = models.BooleanField(db_column="pagamento_configuracao_desconto", default=False, null=False)
    desconto_tipo = models.CharField(db_column="pagamento_configuracao_desconto_tipo", max_length=32, default=TIPO_PORCENTAGEM)
    desconto_valor = models.DecimalField(db_column='pagamento_configuracao_desconto_valor', max_digits=16, decimal_places=2, null=True)
    email_comprovante = models.EmailField(db_column='pagamento_configuracao_email_comprovante', null=True)
    informacao_complementar = models.TextField(db_column='pagamento_configuracao_informacao_complementar', null=True)
    aplicar_no_total = models.BooleanField(db_column='pagamento_configuracao_desconto_aplicar_no_total', null=False, default=False)
    valor_minimo_parcela = models.DecimalField(
        db_column='pagamento_configuracao_valor_minimo_parcela', max_digits=16,
        decimal_places=2, null=True)

    json = JSONField(db_column='pagamento_configuracao_json', null=True, default=None)

    forma_pagamento = models.ForeignKey('configuracao.FormaPagamento', db_column="pagamento_id", related_name="configuracoes")
    conta = models.ForeignKey("plataforma.Conta", related_name="formas_pagamentos_configuracoes")
    contrato = models.ForeignKey("plataforma.Contrato", related_name="formas_pagamentos_configuracoes")

    data_criacao = models.DateTimeField(db_column='pagamento_configuracao_data_criacao', auto_now_add=True)
    data_modificacao = models.DateTimeField(db_column='pagamento_configuracao_data_modificacao', null=True, auto_now=True)

    class Meta:
        db_table = u"configuracao\".\"tb_pagamento_configuracao"
        verbose_name = u"Configuração da forma de pagamento"
        verbose_name_plural = u"Configurações das formas de pagamentos"
        ordering = ["id"]
        unique_together = (("conta", "forma_pagamento"),)

    def __unicode__(self):
        return unicode(self.id)
