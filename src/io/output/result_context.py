

class ResultContext:
    def __init__(self, **kwargs):
        self._properties = kwargs
    
    def get(self, key:str):
        if key in self._properties:
            return self._properties[key]
        else:
            return None