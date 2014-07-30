from ops import API
from ops import Compound
from ops import Target

def info_test():
  api = API('0e939a76', '1004d9ef5f4ee1ab0bbfc02b623cb955')

  compound = Compound(api,'http://www.conceptwiki.org/concept/38932552-111f-4a4e-a46a-4ed1d7bdf9d5')
  print dir(compound)
  print(compound.label)

  target = Target(api, 'http://www.conceptwiki.org/concept/00059958-a045-4581-9dc5-e5a08bb0c291')

  print dir(target)
  print(target.function_annotation)
  print(target.label)


def iteration_test():
  api = API('0e939a76', '1004d9ef5f4ee1ab0bbfc02b623cb955')
  compound = Compound(api,'http://www.conceptwiki.org/concept/38932552-111f-4a4e-a46a-4ed1d7bdf9d5')

  for t in compound.get_pharmacological_protein_targets():
      print(t.label + " " + t.type)

if __name__ == "__main__":
    info_test()
