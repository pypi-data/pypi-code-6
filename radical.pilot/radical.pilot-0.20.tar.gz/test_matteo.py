
import radical.pilot as rp

#-------------------------------------------------------------------------
#
def test__issue_169_part_2():
    """ https://github.com/radical-cybertools/radical.pilot/issues/169
    """

    session = rp.Session()
    print " >>> test__issue_169_part_2"

    pmgr = rp.PilotManager(session=session)
    
    cpd1 = rp.ComputePilotDescription()
    cpd1.resource = "localhost"
    cpd1.cores    = 1
    cpd1.runtime  = 1
    cpd1.sandbox  = "/tmp/radical.pilot.sandbox.unittests"
    cpd1.cleanup  = True

    cpd2 = rp.ComputePilotDescription()
    cpd2.resource = "localhost"
    cpd2.cores    = 1
    cpd2.runtime  = 1
    cpd2.sandbox  = "/tmp/radical.pilot.sandbox.unittests"
    cpd2.cleanup  = True

    pilots = pmgr.submit_pilots([cpd1, cpd2])

    pmgr.wait_pilots(timeout=10*60)
    
    for pilot in pilots:
        try :
            assert pilot.state == rp.DONE, "state: %s" % pilot.state
            assert pilot.stop_time  is not None,      "time : %s" % pilot.stop_time
            assert pilot.start_time is not None,      "time : %s" % pilot.start_time
        except :
            print 'pilot: %s (%s)' % (pilot.uid, pilot.state)
            for entry in pilot.state_history :
                print '       %s : %s' % (entry.timestamp, entry.state)
            print '     : %s' % str(pilot.log)
            raise

    print " <<< test__issue_169_part_2"
    session.close()

#-------------------------------------------------------------------------
#
def test__issue_114_part_1():
    """ https://github.com/radical-cybertools/radical.pilot/issues/114
    """

    session = rp.Session()
    print " >>> test__issue_114_part_1"

    pm = rp.PilotManager(session=session)

    cpd = rp.ComputePilotDescription()
    cpd.resource = "localhost"
    cpd.cores    = 1
    cpd.runtime  = 5
    cpd.sandbox  = "/tmp/radical.pilot.sandbox.unittests"
    cpd.cleanup  = True

    pilot = pm.submit_pilots(pilot_descriptions=cpd)
    state = pm.wait_pilots(state=[rp.ACTIVE, 
                                  rp.DONE, 
                                  rp.FAILED], 
                                  timeout=10*60)

    assert (pilot.state == rp.ACTIVE), "pilot state: %s" % pilot.state

    um = rp.UnitManager(
        session=session,
        scheduler=rp.SCHED_DIRECT_SUBMISSION
    )
    um.add_pilots(pilot)

    all_tasks = []

    for i in range(0,2):
        cudesc = rp.ComputeUnitDescription()
        cudesc.cores      = 1
        cudesc.executable = "/bin/sleep"
        cudesc.arguments  = ['60']
        all_tasks.append(cudesc)

    units  = um.submit_units(all_tasks)
    states = um.wait_units (state=[rp.SCHEDULING, rp.EXECUTING], 
                            timeout=2*60)

    assert rp.SCHEDULING in states, "states: %s" % states

    states = um.wait_units (state=[rp.EXECUTING, rp.DONE], 
                            timeout=2*60)

    assert rp.EXECUTING  in states, "states: %s" % states

    print " <<< test__issue_114_part_1"

    session.close()

#-------------------------------------------------------------------------
#
def test__issue_114_part_2():
    """ https://github.com/radical-cybertools/radical.pilot/issues/114
    """

    session = rp.Session()
    print " >>> test__issue_114_part_2"

    pm  = rp.PilotManager(session=session)

    cpd = rp.ComputePilotDescription()
    cpd.resource = "localhost"
    cpd.cores   = 1
    cpd.runtime = 5
    cpd.sandbox = "/tmp/radical.pilot.sandbox.unittests"
    cpd.cleanup = True

    pilot = pm.submit_pilots(pilot_descriptions=cpd)

    um = rp.UnitManager(
        session=session,
        scheduler=rp.SCHED_DIRECT_SUBMISSION
    )
    um.add_pilots(pilot)

    state = pm.wait_pilots(state=[rp.ACTIVE, 
                                  rp.DONE, 
                                  rp.FAILED], 
                                  timeout=5*60)

    assert (pilot.state == rp.ACTIVE), "pilot state: %s" % pilot.state

    cudesc = rp.ComputeUnitDescription()
    cudesc.cores      = 1
    cudesc.executable = "/bin/sleep"
    cudesc.arguments  = ['60']

    cu    = um.submit_units(cudesc)
    state = um.wait_units(state=[rp.EXECUTING], timeout=60)

    assert state    == [rp.EXECUTING], 'state   : %s' % state
    assert cu.state ==  rp.EXECUTING , 'cu state: %s' % cu.state

    state = um.wait_units(timeout=2*60)

    assert state    == [rp.DONE], 'state   : %s' % state    
    assert cu.state ==  rp.DONE , 'cu state: %s' % cu.state 

    print " <<< test__issue_114_part_2"

    session.close ()

#-------------------------------------------------------------------------
#
def test__issue_114_part_3():
    """ https://github.com/radical-cybertools/radical.pilot/issues/114
    """

    print " >>> test__issue_114_part_3"

    session = rp.Session()

    pm = rp.PilotManager(session=session)

    cpd = rp.ComputePilotDescription()
    cpd.resource = "localhost"
    cpd.cores   = 1
    cpd.runtime = 1
    cpd.sandbox = "/tmp/radical.pilot.sandbox.unittests"
    cpd.cleanup = True

    pilot = pm.submit_pilots(pilot_descriptions=cpd)

    um = rp.UnitManager(
        session   = session,
        scheduler = rp.SCHED_DIRECT_SUBMISSION
    )
    um.add_pilots(pilot)

    state = pm.wait_pilots(state=[rp.ACTIVE, 
                                  rp.DONE, 
                                  rp.FAILED], 
                                  timeout=20*60)

    assert state       == [rp.ACTIVE], 'state      : %s' % state    
    assert pilot.state ==  rp.ACTIVE , 'pilot state: %s' % pilot.state 

    state = pm.wait_pilots(timeout=3*60)

    print "pilot %s: %s / %s" % (pilot.uid, pilot.state, state)
    for entry in pilot.state_history :
        print "      %s : %s" % (entry.timestamp, entry.state)
    for log in pilot.log :
        print "      log : %s" % log

    assert state       == [rp.DONE], 'state      : %s' % state        
    assert pilot.state ==  rp.DONE , 'pilot state: %s' % pilot.state  

    print " <<< test__issue_114_part_3"

    session.close()


# ------------------------------------------------------------------------------
#
def test__remote_simple_submission():
    """ Test simple remote submission with one pilot.
    """

    import os

    test_resource = os.getenv('RADICAL_PILOT_TEST_REMOTE_RESOURCE',     "localhost")
    test_ssh_uid  = os.getenv('RADICAL_PILOT_TEST_REMOTE_SSH_USER_ID',  None)
    test_ssh_key  = os.getenv('RADICAL_PILOT_TEST_REMOTE_SSH_USER_KEY', None)
    test_workdir  = os.getenv('RADICAL_PILOT_TEST_REMOTE_WORKDIR',      "/tmp/radical.pilot.sandbox.unittests")
    test_cores    = os.getenv('RADICAL_PILOT_TEST_REMOTE_CORES',        "1")
    test_num_cus  = os.getenv('RADICAL_PILOT_TEST_REMOTE_NUM_CUS',      "2")
    test_timeout  = os.getenv('RADICAL_PILOT_TEST_TIMEOUT',             "5")

    session    = rp.Session()

    c = rp.Context('ssh')
    c.user_id  = test_ssh_uid
    c.user_key = test_ssh_key

    session.add_context(c)

    pm  = rp.PilotManager(session=session)

    cpd = rp.ComputePilotDescription()
    cpd.resource = test_resource
    cpd.cores    = test_cores
    cpd.runtime  = 15
    cpd.sandbox  = test_workdir

    pilot = pm.submit_pilots(pilot_descriptions=cpd)

    um = rp.UnitManager(session=session, scheduler='round_robin')
    um.add_pilots(pilot)

    cudescs = []
    for _ in range(0,int(test_num_cus)):
        cudesc = rp.ComputeUnitDescription()
        cudesc.cores      = 1
        cudesc.executable = "/bin/sleep"
        cudesc.arguments  = ['10']
        cudescs.append(cudesc)

    cus = um.submit_units(cudescs)

    for cu in cus:
        assert cu is not None
        assert cu.start_time is None
        assert cu.stop_time is None

    ret = um.wait_units(timeout=5*60)
    print "Return states from wait: %s" % ret

    for cu in cus:
        assert cu.state == rp.DONE, "state: %s" % cu.state
        assert cu.stop_time is not None

    pm.cancel_pilots()

    session.close()


# ------------------------------------------------------------------------------
#

# test__issue_114_part_1 ()
# test__issue_114_part_2 ()
# test__issue_114_part_3 ()
# test__issue_169_part_2 ()

test__remote_simple_submission ()

