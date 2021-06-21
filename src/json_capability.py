class JSONCapability:
    def to_json(self):
        return {k: v if not isinstance(v, JSONCapability) else v.to_json()
                for k, v in self.__dict__.items() if v is not None}
