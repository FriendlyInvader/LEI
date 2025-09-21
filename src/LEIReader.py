import requests
from src.issuer import issuer
from src.dict_cache import dict_cache
import threading

class LEIReader:
    DEFAULT_ROOT = "https://api.gleif.org/api/v1/lei-issuers"
    
    def __init__(self, window:float=7.0, root:str=DEFAULT_ROOT) -> None:
        self._country_code_cache = dict_cache(self.fetch_country_code, window)
        self._fetch_cache = dict_cache(self.fetch, window)
        if root is None:
            self._root = self.DEFAULT_ROOT
        self._root = root

    def build_url(self, page:int = 1, size:int = 10)->str:
        return f"{self._root}?page%5Bnumber%5D={page}&page%5Bsize%5D={size}"

    def fetch_cache(self, page:int = 1, size:int = 10):
        return self._fetch_cache.get(self.build_url(page, size))

    def fetch_page(self, page:int = 1, size:int = 10):
        return self.fetch(self.build_url(page, size))

    def fetch(self, url:str):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def extract_issuers(self, page:int = 1, size:int = 10)->list[issuer]:
        get_issuer = lambda item: issuer(
            item["attributes"].get("lei", ""), 
            item["attributes"].get("name", ""),
            self._country_code_cache.get(item["relationships"]["fundJurisdictions"]["links"]["related"]))
        return [get_issuer(x) for x in self.fetch_cache(page, size).get("data", [])]
    
    def extract_issuers_to_list(self, container:list, page:int = 1, size:int = 10)->None:
        container.extend(self.extract_issuers(page, size))
    
    def fetch_country_code(self, jurisdiction_url: str)->str:
        response = requests.get(jurisdiction_url)
        response.raise_for_status()
        data = response.json().get("data", [])
        if not data:
            return ""
        return data[0]["attributes"]["countryCode"]

    def extract_issuers_concurrent(self, page_size_list:list[tuple[int, int]]):
        threads = []
        results = []
        for page, size in page_size_list:
            t = threading.Thread(
                    target=self.extract_issuers_to_list,
                    args=(results, page, size))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return results
