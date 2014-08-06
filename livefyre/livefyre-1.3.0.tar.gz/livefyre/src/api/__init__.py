def get_lf_token_header(core, user_token = None):
    return {
            'Authorization': 'lftoken ' + (core.build_livefyre_token() if user_token is None else user_token),
            'Accepts': 'application/json'
    }