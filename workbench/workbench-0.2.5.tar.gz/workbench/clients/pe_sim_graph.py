''' This client generates a similarity graph from features in PE Files '''
import zerorpc
import os
import workbench_client

def add_it(workbench, file_list, labels):
    ''' Add the given file_list to workbench as samples, also add them as nodes '''
    md5s = []
    for filename in file_list:
        if filename != '.DS_Store':
            with open(filename, 'rb') as pe_file:
                md5 = workbench.store_sample(filename,  pe_file.read(), 'pe')
                workbench.add_node(md5, md5[:6], labels)
                md5s.append(md5)
    return md5s


def jaccard_sims(feature_list):
    ''' Compute Jaccard similarities between all the observations in the feature list '''

    sim_info_list = []
    for feature_info in feature_list:
        md5_source = feature_info['md5']
        features_source = feature_info['features']
        for feature_info in feature_list:
            md5_target = feature_info['md5']
            features_target = feature_info['features']
            if md5_source == md5_target: 
                continue
            sim = jaccard_sim(features_source, features_target)
            if sim > .5:
                sim_info_list.append({'source': md5_source, 'target': md5_target, 'sim': sim})

    return sim_info_list


def jaccard_sim(features1, features2):
    ''' Compute similarity between two sets using Jaccard similarity '''
    set1 = set(features1)
    set2 = set(features2)
    try:
        return len(set1.intersection(set2))/float(max(len(set1), len(set2)))
    except ZeroDivisionError:
        return 0


def run():
    ''' This client generates a similarity graph from features in PE Files '''

    # Grab server args
    args = workbench_client.grab_server_args()

    # Start up workbench connection
    workbench = zerorpc.Client()
    workbench.connect('tcp://'+args['server']+':'+args['port'])

    # Test out PEFile -> pe_deep_sim -> pe_jaccard_sim -> graph
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/pe/bad')
    bad_files = [os.path.join(data_path, child) for child in os.listdir(data_path)][:10]
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data/pe/good')
    good_files = [os.path.join(data_path, child) for child in os.listdir(data_path)][:10]

    # Clear any graph in the Neo4j database
    workbench.clear_graph_db()

    # First throw them into workbench and add them as nodes into the graph
    all_md5s = add_it(workbench, bad_files, ['pe', 'bad']) + add_it(workbench, good_files, ['pe', 'good'])

    # Compute pe_features on all files of type pe, just pull back the sparse features
    imports = workbench.batch_work_request('pe_features',
        {'md5_list': all_md5s, 'subkeys':['md5', 'sparse_features.imported_symbols']})

    # Compute pe_features on all files of type pe, just pull back the sparse features
    warnings = workbench.batch_work_request('pe_features',
        {'md5_list': all_md5s, 'subkeys':['md5', 'sparse_features.pe_warning_strings']})

    # Compute strings on all files of type pe, just pull back the string_list
    strings = workbench.batch_work_request('strings', {'md5_list': all_md5s, 'subkeys':['md5', 'string_list']})

    # Compute pe_peid on all files of type pe, just pull back the match_list
    peids = workbench.batch_work_request('pe_peid', {'md5_list': all_md5s, 'subkeys':['md5', 'match_list']})

    # Organize the data a bit
    imports = [{'md5': r['md5'], 'features': r['imported_symbols']} for r in imports]
    warnings = [{'md5': r['md5'], 'features': r['pe_warning_strings']} for r in warnings]
    strings = [{'md5': r['md5'], 'features': r['string_list']} for r in strings]
    peids = [{'md5': r['md5'], 'features': r['match_list']} for r in peids]

    # Compute the Jaccard Index between imported systems and store as relationships
    sims = jaccard_sims(imports)
    for sim_info in sims:
        workbench.add_rel(sim_info['source'], sim_info['target'], 'imports')

    # Compute the Jaccard Index between warnings and store as relationships
    sims = jaccard_sims(warnings)
    for sim_info in sims:
        workbench.add_rel(sim_info['source'], sim_info['target'], 'warnings')

    # Compute the Jaccard Index between strings and store as relationships
    sims = jaccard_sims(strings)
    for sim_info in sims:
        workbench.add_rel(sim_info['source'], sim_info['target'], 'strings')

    # Compute the Jaccard Index between peids and store as relationships
    sims = jaccard_sims(peids)
    for sim_info in sims:
        workbench.add_rel(sim_info['source'], sim_info['target'], 'peids')

    # Compute pe_deep_sim on all files of type pe
    results = workbench.batch_work_request('pe_deep_sim', {'type_tag': 'pe'})

    # Store the ssdeep sims as relationships
    for result in list(results):
        for sim_info in result['sim_list']:
            workbench.add_rel(result['md5'], sim_info['md5'], 'ssdeep')

    # Let them know where they can get there graph
    print 'All done: go to http://localhost:7474/browser and execute this query: "%s"' % \
        ('match (n)-[r]-() return n,r')

import pytest
@pytest.mark.xfail
def test():
    ''' pe_sim_graph test '''
    run()

if __name__ == '__main__':
    run()
