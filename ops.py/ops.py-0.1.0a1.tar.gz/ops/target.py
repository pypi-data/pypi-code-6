class Target:
  def __init__(self, api, target_uri):
      self.api = api
      self.init_uri = target_uri
      res = api.getTargetInfo(target_uri)
      self._parse_and_populate(res)
      self.json = res

  def _parse_and_populate(self, compound_info_results):
    primaryTopic = compound_info_results['result']['primaryTopic']
    if "prefLabel" in primaryTopic:
      self.label = primaryTopic['prefLabel']
    elif "label" in primaryTopic:
      self.label = primaryTopic['label']

    if "type" in primaryTopic:
      self.type = primaryTopic['type']

    exactMatches = primaryTopic['exactMatch']

    for exactMatch in exactMatches:
      if "numberOfResidues" in exactMatch:
        self.number_of_residues = exactMatch["numberOfResidues"]

      if "Function_Annotation" in exactMatch:
        self.function_annotation = exactMatch["Function_Annotation"]

      if "organisim" in exactMatch:
        self.organism_url = exactMatch["organisim"]
