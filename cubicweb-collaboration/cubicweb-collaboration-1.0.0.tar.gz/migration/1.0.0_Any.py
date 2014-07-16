from cubes.container import CONTAINERS


wf_rtype_roles = (('custom_workflow', 'subject'),
                  ('in_state', 'subject'),
                  ('wf_info_for', 'object'))

for etype, cfg in CONTAINERS.iteritems():
    if hasattr(cfg, 'collaboration_config'):
        eschema = schema[etype]
        if not any(eschema.has_relation(rtype, role)
                   for rtype, role in wf_rtype_roles):
            make_workflowable(etype)
        default = True
        if (eschema.has_relation('default_workflow', role='subject') and
                eschema.default_workflow):
            print ('%s already has a a default worklow, collaboration '
                   'workflow will not be the default one.' % etype)
            default = False
        collabcfg = cfg.collaboration_config
        wf = collabcfg.build_collaboration_workflow(session, default=default)
        for entity in find_entities(etype):
            adapted = entity.cw_adapt_to('IWorkflowable')
            state = u'wfs_immutable' if entity.frozen else u'wfs_mutable'
            adapted.set_initial_state(state)
        drop_attribute(etype, 'frozen')
