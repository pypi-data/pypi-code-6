# import random
# import pydecode.hyper as ph
# import pydecode.chart as chart
# import pydecode.nlp.dependency_parsing as dep
# import pydecode.test.utils as utils
# import nose.tools as nt


# def test_parse():
#     for n in range(2, 6):
#         first = [[random.random() for j in range(n+1)] for i in range(n+1)]
#         second = [[[random.random() for k in range(n+1)] for j in range(n+1)] for i in range(n+1)]

#         scorer1 = dep.ArcScorer(n, first, None)
#         scorer2 = dep.ArcScorer(n, first, second)

#         yield check_parse, n, scorer1
#         yield check_second_parse, n, scorer2

# def check_parse(n, scorer):
#     c = chart.ChartBuilder(lambda a:a, chart.HypergraphSemiRing, 
#                            build_hypergraph = True)
#     dep.parse_first_order(n, c)
#     hypergraph = c.finish()
#     paths = utils.all_paths(hypergraph)
#     parses = map(dep.path_to_parse, paths)
#     parses.sort()
#     parses2 = list(dep.DependencyParse.enumerate_projective(n))
#     parses2.sort()
#     assert(parses == parses2)

#     def score(label):
#         if label is None: return 0.0
#         return scorer.arc_score(label.head, label.mod)
#     scores = ph.LogViterbiPotentials(hypergraph).from_vector(
#         [score(edge.label) for edge in hypergraph.edges ])
#     for path in paths:
#         nt.assert_almost_equal(scores.dot(path), 
#                                scorer.score(dep.path_to_parse(path)))



# def check_second_parse(n, scorer):
#     c = chart.ChartBuilder(lambda a:a, chart.HypergraphSemiRing, 
#                            build_hypergraph = True)
#     dep.parse_second_order(n, c)
#     hypergraph = c.finish()
#     paths = utils.all_paths(hypergraph)
#     parses = map(dep.path_to_parse, paths)
#     parses.sort()
#     parses2 = list(dep.DependencyParse.enumerate_projective(n))
#     parses2.sort()
#     assert(parses == parses2)

#     def score(label):
#         if label is None: return 0.0
#         return scorer.arc_score(label.head, label.mod, label.sibling)
#     scores = ph.LogViterbiPotentials(hypergraph).from_vector(
#         [score(edge.label) for edge in hypergraph.edges ])

#     scores = ph.LogViterbiPotentials(hypergraph).from_vector(
#         [score(edge.label) for edge in hypergraph.edges ])
#     for path in paths:
#         nt.assert_almost_equal(scores.dot(path), 
#                                scorer.score(dep.path_to_parse(path)))
