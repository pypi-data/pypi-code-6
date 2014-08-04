from celery.task import task

@task(name="dkeen-add-event")
def add_event_delayed(client, event_collection, event_body, timestamp):
    client.add_event(event_collection, event_body, timestamp)

@task(name="dkeen-add-events")
def add_events_delayed(client, events):
    client.add_events(events)