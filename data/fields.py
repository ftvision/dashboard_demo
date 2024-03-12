from dataclasses import dataclass, fields

@dataclass
class Params:
  name: str = ""
  param1: int = 0
  param2: float = 0.
  param3: str = ""
  param4: str = ""

def all_param_fields():
  return [(f.name, f.type) for f in fields(Params())]


