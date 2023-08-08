'''
======================================================================================================
Copyright (c) 2023, TSRE Library
======================================================================================================
'''
from pynginxconfig import NginxConfig


class TNginxConfig(NginxConfig):
    """method to demonstrate inheritance"""

    def list_proxy_rule(self):
        """list all location proxy rule"""
        res: dict = {}
        data_list: list = self.data
        for key, item in data_list[0].items():
            if key == "value" and isinstance(item, list):
                for ind in item:
                    if isinstance(ind, dict) and ind.get("param"):
                        val = ind.get("param")
                        res[val] = ind.get("value")
        return res

    # def append_value(self, name: str, rule: List[tuple]) -> None:
    def append_value(self, name: str, rule: tuple) -> None:
        """append location proxy rule"""
        new_rule = {'name': 'location'}
        new_data_list = self.data
        for key, item in new_data_list[0].items():
            print(f"key: {key}, item: {item}")
            if key == "value" and isinstance(item, list):
                for ind in item:
                    if isinstance(ind, dict) and ind.get("param"):
                        if ind.get("param") == name:
                            # name in location
                            ind["value"].extend([rule])
                            return
                # name not in location
                new_rule['param'] = name
                new_rule['value'] = [rule]
                item.append(new_rule)
                return

    def remove_value(self, name: str, rule: tuple) -> None:
        """remove location proxy rule"""

    def modify_value(self, name: str, rule: tuple) -> None:
        """modify location proxy rule"""
