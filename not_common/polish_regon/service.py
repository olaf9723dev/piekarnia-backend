from gusregon import GUS


class RegonService:

    def __init__(self, sandbox: bool = False, api_key: str = None):
        self.gus_client = GUS(sandbox=sandbox, api_key=api_key)

    def search(self, **kwargs):
        return self.gus_client.search(**kwargs)
