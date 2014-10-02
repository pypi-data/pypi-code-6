import markdown


def make_markdowner(extensions):
    def render_markdown(raw_content):
        return markdown.markdown(
            raw_content,
            extensions=extensions,
        )
    return render_markdown


def register(ctx, config):
    markdown_extentions = ['md', 'mkd', 'markdown']
    markdowner = make_markdowner(config.get('extensions', []))
    ctx.content_renderer.add_renderer(markdown_extentions, markdowner)
