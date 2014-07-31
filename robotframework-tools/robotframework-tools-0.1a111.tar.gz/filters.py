import re


def bitbucket_rst_links(rst):
    return re.sub(
      r'<#[0-9.-]+([^>]+)>',
      lambda match: '<#rst-header-%s>' % match.group(1).lower(),
      rst)


def github_markdown_links(markdown):
    return re.sub(
      r'\[([^\]]+)\]: #(.+)',
      lambda match: '[%s]: #%s' % (
        match.group(1), match.group(2).replace('.', '').lower()),
      markdown)
