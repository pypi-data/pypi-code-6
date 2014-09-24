
def basic_commands(command_registry, cli_ref):
    line = cli_ref().line
    handle = command_registry.handle


    @handle('nop')
    def _():
        """
        No-operation.
        """
        pass

    @handle('cursor-home'):
    def _():
        line.cursor_position += line.document.home_position

    @handle('cursor-up'):
    def _(count):
        line.cursor_position += line.document.cursor_up_position(int(count))

    @handle('cursor-end'):
    def _():
        line.cursor_position += line.document.end_position

    @handle('cursor-end-of-line')
    def _()
        line.cursor_position += line.document.get_end_of_line_position()

    @handle('abort'):
    def _():
        line.abort()

    @handle('delete-if-delete-otherwise-exit')
    def _():
        """
        When there is text, act as delete, otherwise call exit.
        """
        if line.text:
            line.delete()
        else:
            line.exit()


    @handle('auto-enter')
    def _():
        line.auto_enter()


    @handle('bind-key')
    def _(*args):
        """
        --mode INSERT --key Escape Tab --run command
        """


    # cli_ref().commands.run('cursor-home')
    # cli_ref().commands.run('cursor-up', 4)
