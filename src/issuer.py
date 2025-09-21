class issuer:
    _code = ""
    _name = ""
    _country_code = ""

    def __init__(self, code:str="", name:str="", country_code:str=""):
        self._code = code
        self._name = name
        self._country_code = country_code

    @property
    def code(self)->str:
        return self._code

    @property
    def name(self)->str:
        return self._name
    
    @property
    def country_code(self)->str:
        return self._country_code

    def __str__(self)->str:
        return f"{self._code} - {self._name} - {self._country_code}"