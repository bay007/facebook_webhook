import os

class Config(object):
    FBAPI_APP_SECRET = os.getenv("token_pagina_facebook") if os.getenv("token_pagina_facebook") else "BEAAGhFLVhafoBAKcnKZAQdxF8coVW8p2VCpldZBInmBPUEZBMBZAQFa4FrTVLjhNK3rVdFbZCKcQh6gzpOWcAGN6RzI5ByVeKDQ2pHdJZBewmRcmfKO76UImmih7m7FXh41rIc4fpj3zYbEg8Paz3p8nCeFvmOGz03JRAZA8cQlD0DuQ3cno13zt"
    