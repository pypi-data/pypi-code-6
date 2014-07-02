# -*- coding:utf-8 -*-
from interlegis.intranetmodelo.policy.utils import _add_id

import os

PROJECTNAME = 'interlegis.portalmodelo.policy'
PROFILE_ID = '{0}:default'.format(PROJECTNAME)

# content created at Plone's installation
DEFAULT_CONTENT = ('front-page', 'news', 'events', 'Members')

LOREM_TITLE = u'Lorem ipsum'
LOREM_DESCRIPTION = u'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.'

IMAGE = open(
    os.path.join(
        os.path.dirname(__file__), 'tests', 'bandeira-brasil.jpg')).read()

# new site structure; this dictionary defines the objects that are going to be
# created on the root of the site; it also includes information about folder
# constrains and objects to be created inside them
SITE_STRUCTURE = [
    dict(
        type='collective.cover.content',
        title=u'Página inicial',
        template_layout='Portal Modelo',
    ),
    dict(
        type='Folder',
        title=u'Sobre a Câmara',
        excludeFromNav=True,
        _addable_types=['Folder', 'File', 'Link', 'Document', 'Window'],
        _children=[
            dict(type='Folder', title=u'Acesso'),
            dict(type='Folder', title=u'História'),
            dict(type='Folder', title=u'Função e definição'),
            dict(type='Folder', title=u'Estrutura'),
            dict(
                type='Folder',
                title=u'Notícias',
                _addable_types=['Collection', 'Folder', 'News Item'],
                _children=[
                    dict(
                        type='Collection',
                        title=u'Notícias',
                        query=[
                            dict(
                                i='portal_type',
                                o='plone.app.querystring.operation.selection.is',
                                v='News Item',
                            ),
                            dict(
                                i='path',
                                o='plone.app.querystring.operation.string.relativePath',
                                v='../',
                            ),
                        ],
                        sort_reversed=True,
                        sort_on=u'created',
                        limit=100,
                    ),
                    dict(
                        type='News Item',
                        title=LOREM_TITLE,
                        description=LOREM_DESCRIPTION,
                    ),
                    dict(
                        type='News Item',
                        id='lorem-ipsum-1',
                        title=LOREM_TITLE,
                        description=LOREM_DESCRIPTION,
                    ),
                    dict(
                        type='News Item',
                        id='lorem-ipsum-2',
                        title=LOREM_TITLE,
                        description=LOREM_DESCRIPTION,
                    ),
                    dict(
                        type='News Item',
                        id='lorem-ipsum-3',
                        title=LOREM_TITLE,
                        description=LOREM_DESCRIPTION,
                    ),
                ],
            ),
            dict(
                type='Folder',
                title=u'Eventos',
                _addable_types=['Collection', 'Event', 'Folder'],
            ),
            dict(
                type='Folder',
                title=u'Fotos',
                _addable_types=['Collection', 'Folder', 'Image', 'Link'],
            ),
        ],
    ),
    dict(
        type='Folder',
        title=u'Processo legislativo',
        excludeFromNav=True,
        _addable_types=['Folder', 'File', 'Link', 'Document', 'Window'],
    ),
    dict(
        type='Folder',
        title=u'Leis',
        excludeFromNav=True,
        _addable_types=['Folder', 'File', 'Link', 'Document', 'Window'],
        _children=[
            dict(type='Folder', title=u'Legislação Municipal'),
            dict(type='Folder', title=u'Lei Orgânica Municipal'),
            dict(type='Folder', title=u'LEXML'),
        ],
    ),
    dict(
        type='Folder',
        title=u'Transparência',
        _addable_types=['Folder', 'File', 'Link', 'Document', 'Window'],
        _children=[
            dict(
                type='Folder',
                title=u'Despesas',
                description=u'Gastos diretos da Câmara Municipal.',
                _addable_types=['CSVData', 'Folder', 'File', 'Link', 'Document', 'Window'],
            ),
            dict(
                type='Folder',
                title=u'Transferências',
                description=u'Repasses ou transferências de recursos financeiros para entidades.',
                _addable_types=['CSVData', 'Folder', 'File', 'Link', 'Document', 'Window'],
            ),
            dict(
                type='Folder',
                title=u'Receitas',
                description=u'Receitas da Câmara Municipal.',
                _addable_types=['CSVData', 'Folder', 'File', 'Link', 'Document', 'Window'],
            ),
            dict(
                type='Folder',
                title=u'Acompanhamento',
                description=u'Acompanhamento de programas, ações, projetos e obras de órgãos e entidades.',
                _addable_types=['CSVData', 'Folder', 'File', 'Link', 'Document', 'Window'],
            ),
            dict(
                type='Folder',
                title=u'Licitações',
                description=u'Informações sobre os processos de licitação da Câmara Municipal.',
                _addable_types=['CSVData', 'Folder', 'File', 'Link', 'Document', 'Window'],
            ),
            dict(
                type='Document',
                title=u'FAQ',
                description=u'Perguntas mais frequentes dos visitantes.',
            ),
        ],
    ),
    dict(
        type='Folder',
        title=u'Links úteis',
        excludeFromNav=True,
        _addable_types=['Folder', 'Link'],
        _children=[
            dict(
                type='Link',
                title=u'Prefeitura',
                remoteUrl='http://',
            ),
            dict(
                type='Link',
                title=u'Diario Oficial',
                remoteUrl='http://',
            ),
            dict(
                type='Link',
                title=u'Programa Interlegis',
                remoteUrl='http://www.interlegis.gov.br',
            ),
            dict(
                type='Link',
                title=u'Assembléia Estadual',
                remoteUrl='http://',
            ),
            dict(
                type='Link',
                title=u'Câmara dos Deputados',
                remoteUrl='http://www.camara.gov.br',
            ),
            dict(
                type='Link',
                title=u'Senado Federal',
                remoteUrl='http://www.senado.gov.br',
            ),
        ],
    ),
    dict(
        type='OmbudsOffice',
        title=u'Ouvidoria',
        description=u'Sistema de informações ao cidadão.',
        claim_types=[
            dict(claim_type='Denúncia'),
            dict(claim_type='Dúvida'),
            dict(claim_type='Elogio'),
            dict(claim_type='Pedido de Acesso à Informação'),
            dict(claim_type='Solicitação'),
            dict(claim_type='Sugestão'),
            dict(claim_type='Reclamação'),
        ],
        areas=[
            dict(responsible='Nome do Responsável', email='nome@dominio.leg.br', area='Administração'),
            dict(responsible='Nome do Responsável', email='nome@dominio.leg.br', area='Assessoria Legislativa e Jurídica'),
            dict(responsible='Nome do Responsável', email='nome@dominio.leg.br', area='Comissões'),
            dict(responsible='Nome do Responsável', email='nome@dominio.leg.br', area='Ouvidoria'),
            dict(responsible='Nome do Responsável', email='nome@dominio.leg.br', area='Secretaria Legislativa'),
            dict(responsible='Nome do Responsável', email='nome@dominio.leg.br', area='Plenário'),
        ],
    ),
    dict(
        type='Folder',
        title=u'Banco de imagens',
        excludeFromNav=True,
        _addable_types=['Folder', 'Image', 'Link'],
    ),
    dict(
        type='Blog',
        id='blog',
        title=u'Blog Legislativo',
        description=u'Weblog sobre assuntos técnicos dos setores da Casa Legislativa.',
        author=u'Funcionários da Casa Legislativa',
        excludeFromNav=True,
    ),
    dict(
        type='Folder',
        title=u'Boletins',
        excludeFromNav=True,
        _addable_types=['EasyNewsletter'],
        _children=[
            dict(
                type='EasyNewsletter',
                title=u'Acompanhe a Câmara',
                description=u'Receba por e-mail tudo o que acontece de novo na nossa Casa Legislativa.',
            ),
        ],
    ),
    dict(
        type='Folder',
        title=u'Enquetes',
        excludeFromNav=True,
        _addable_types=['collective.polls.poll'],
    ),
    dict(
        type='Ploneboard',
        title=u'Fóruns',
        excludeFromNav=True,
        _children=[
            dict(
                type='PloneboardForum',
                title=u'Educação',
                description='Debates sobre o ensino público em nosso município.',
            ),
            dict(
                type='PloneboardForum',
                title=u'Saúde',
                description='Debates sobre saúde pública em nosso município .',
            ),
            dict(
                type='PloneboardForum',
                title=u'Transporte',
                description='Debates sobre mobilidade urbana em nosso município.',
            ),
        ],
    ),
    dict(
        type='Document',
        title=u'Rodapé',
        text=u'<p>O conteúdo deste site está publicado sob a licença <a href="http://creativecommons.org/licenses/by-nc-sa/3.0/br/">Creative Commons - atribuição e não-comercial</a>.</p>',
        excludeFromNav=True,
    ),
    dict(
        type='Document',
        title=u'Perguntas frequentes',
    ),
]

SITE_STRUCTURE = _add_id(SITE_STRUCTURE)
