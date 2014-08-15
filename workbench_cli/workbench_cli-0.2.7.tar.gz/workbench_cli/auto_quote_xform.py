""" AutoQuoteTransformer: IPython Transformer so we can shortcut
    Workbench commands by using 'auto-quotes' """

import re
from IPython.core.prefilter import PrefilterTransformer

# Helper Classes
class AutoQuoteTransformer(PrefilterTransformer):
    """ AutoQuoteTransformer: IPython Transformer so we can shortcut
        Workbench commands by using 'auto-quotes' """

    def register_command_set(self, command_set):
        """Register all the Workbench commands"""
        self.command_set = command_set

    def transform(self, line, _continue_prompt):
        """Shortcut Workbench commands by using 'auto-quotes'"""

        # Capture the original line
        orig_line = line

        # Very conservative logic (but possibly flawed)
        # 1) Lines with any of these symbols ; , ' " ( ) aren't touched
        # 2) Need to have more than one token
        # 3) First token in line must be in the workbench command set
        # 4) If first token is 'help' than all other tokens are quoted
        # 5) Otherwise only tokens that are not in any of the namespace are quoted


        # 1) Lines with any of these symbols ; , ' " ( ) aren't touched
        skip_symbols = [';', ',', '\'', '"', '(', ')']
        if any([sym in line for sym in skip_symbols]):
            return line

        # Build up token set and info
        token_list = re.split(' |;|,|(|)|\'|"', line)
        num_tokens = len(token_list)
        first_token = token_list[0]
        token_set = set(token_list)
        if None in token_set: # In some cases None creeps in
            token_set.remove(None)

        # 2) Need to have more than one token
        # 3) First token in line must be in the workbench command set
        if num_tokens > 1 and first_token in self.command_set:

            # 4) If first token is 'help' than all other tokens are quoted
            if first_token == 'help':
                token_set.remove('help')
                for token in token_set:
                    line = line.replace(token, '"'+token+'"')

            # 5) Otherwise only tokens that are not in any of the namespace are quoted
            else: # Not help
                ns_token_set = set([token for nspace in self.shell.all_ns_refs for token in nspace])
                for token in token_set:
                    if token not in ns_token_set:
                        line = line.replace(token, '"'+token+'"')

        # Return the processed line
        return line
