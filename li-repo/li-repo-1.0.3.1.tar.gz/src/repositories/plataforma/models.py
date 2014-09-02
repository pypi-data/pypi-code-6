# -*- coding: utf-8 -*-

from django.db import models
from jsonfield import JSONField


class Contrato(models.Model):

    id = models.AutoField(db_column="contrato_id", primary_key=True)
    nome = models.CharField(db_column="contrato_nome", max_length=255)
    codigo = models.CharField(db_column="contrato_codigo", max_length=255, unique=True)
    dominio = models.CharField(db_column="contrato_dominio", max_length=255)
    url_institucional = models.CharField(db_column="contrato_url_institucional", max_length=255)
    parametros = JSONField(u'Parametros do contrato', db_column="contrato_parametros", null=True, help_text=u'Os parametros informados vão sobreescrever os do contrato principal.')
    tipo = models.CharField(db_column="contrato_tipo", max_length=32)

    class Meta:
        db_table = u"plataforma\".\"tb_contrato"


class Conta(models.Model):

    id = models.AutoField(db_column="conta_id", primary_key=True)
    apelido = models.CharField(db_column="conta_apelido", max_length=32)
    dominio = models.CharField(db_column="conta_loja_dominio", max_length=128, null=True, default=None)
    situacao = models.CharField(db_column="conta_situacao")

    contrato = models.ForeignKey('Contrato', db_column="contrato_id")
    plano = models.ForeignKey('faturamento.Plano', db_column="plano_id")

    class Meta:
        db_table = u"plataforma\".\"tb_conta"


class Dominio(models.Model):
    """Lista de domínios habilitados para uma conta."""
    id = models.AutoField(db_column="dominio_id", primary_key=True)
    fqdn = models.CharField(db_column="dominio_fqdn", max_length=128, null=False, unique=True)
    principal = models.BooleanField(db_column="dominio_principal", default=False, db_index=True)

    conta = models.ForeignKey("Conta", db_column="conta_id", related_name="dominios")

    class Meta:
        db_table = u"configuracao\".\"tb_dominio"


class Usuario(models.Model):

    id = models.AutoField(db_column="usuario_id", primary_key=True)
    nome = models.CharField(db_column="usuario_nome", max_length=128)
    email = models.EmailField(db_column="usuario_email")
    confirmado = models.BooleanField(db_column="usuario_confirmado", default=False)

    conta_id = models.ManyToManyField('Conta', through="ContaUsuario")

    class Meta:
        db_table = u"plataforma\".\"tb_usuario"

    @property
    def primeiro_nome(self):
        if self.nome:
            return self.nome.split()[0]


class ContaUsuario(models.Model):
    """Relação entre conta e usuário."""
    id = models.AutoField(db_column="conta_usuario_id", primary_key=True)

    usuario = models.ForeignKey('Usuario', db_column="usuario_id")
    conta = models.ForeignKey('Conta', db_column="conta_id")

    class Meta:
        db_table = u"plataforma\".\"tb_conta_usuario"
        unique_together = ('conta', 'usuario')


class Certificado(models.Model):
    """Tipo de certificados a venda."""

    id = models.AutoField(db_column="certificado_id", primary_key=True)
    ativo = models.BooleanField(db_column="certificado_ativo", default=True)
    nome = models.CharField(db_column="certificado_nome", max_length=64)
    codigo = models.CharField(db_column="certificado_codigo", max_length=64, unique=True)
    fornecedor = models.CharField(db_column="certificado_fornecedor", max_length=128)
    fornecedor_site = models.CharField(db_column="certificado_fornecedor_site", max_length=256, null=True)
    descricao = models.TextField(db_column="certificado_descricao", null=True, default=None)
    valor = models.DecimalField(db_column="certificado_valor", max_digits=16, decimal_places=2)
    validade_anos = models.IntegerField(db_column="certificado_validade_anos")

    crt_intermediario = models.TextField(db_column="certificado_crt_intermediario", null=True)
    crt_raiz = models.TextField(db_column="certificado_crt_raiz", null=True)

    class Meta:
        db_table = u"plataforma\".\"tb_certificado"

    def __unicode__(self):
        return self.nome


class ContaCertificado(models.Model):
    """Gerencia os Certificados SSL instalados na Loja integrada."""

    id = models.AutoField(db_column="conta_certificado_id", primary_key=True, null=False)
    dominio = models.CharField(db_column="conta_certificado_dominio", max_length=128)
    key = models.TextField(db_column="conta_certificado_key", null=True)
    csr = models.TextField(db_column="conta_certificado_csr", null=True)
    crt = models.TextField(db_column="conta_certificado_crt", null=True)
    data_inicio = models.DateTimeField(db_column="conta_certificado_data_inicio", auto_now_add=True)
    data_expiracao = models.DateTimeField(db_column="conta_certificado_data_expiracao", null=True)
    situacao = models.CharField(db_column="conta_certificado_situacao", max_length=32)

    nc_compra_id = models.IntegerField(db_column="conta_certificado_namecheap_compra_id", null=True)
    nc_certificado_id = models.IntegerField(db_column="conta_certificado_namecheap_certificado_id", null=True)
    nc_transacao_id = models.IntegerField(db_column="conta_certificado_namecheap_transacao_id", null=True)

    certificado = models.ForeignKey('Certificado', related_name='contas', on_delete=models.CASCADE)
    contrato = models.ForeignKey('Contrato', db_column="contrato_id")
    conta = models.ForeignKey('Conta', db_column="conta_id")

    class Meta:
        db_table = u"plataforma\".\"tb_conta_certificado"


class Imagem(models.Model):
    """Imagens."""

    id = models.AutoField(db_column="imagem_id", primary_key=True)
    tabela = models.CharField(db_column="imagem_tabela", max_length=64, null=True)
    campo = models.CharField(db_column="imagem_campo", max_length=64, null=True)
    linha_id = models.IntegerField(db_column="imagem_linha_id", null=True)
    data_criacao = models.DateTimeField(db_column="imagem_data_criacao", auto_now_add=True)
    data_modificacao = models.DateTimeField(db_column="imagem_data_modificacao", auto_now=True)

    caminho = models.CharField(db_column="imagem_caminho", null=True)

    tipo = models.CharField(db_column="imagem_tipo", max_length=32)
    processada = models.BooleanField(db_column="imagem_processada")

    contrato = models.ForeignKey('Contrato', db_column="contrato_id")
    conta = models.ForeignKey('Conta', db_column="conta_id")

    class Meta:
        db_table = u"plataforma\".\"tb_imagem"