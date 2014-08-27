import zerorpc

c = zerorpc.Client()
c.connect('tcp://127.0.0.1:4242')

def addSimJob(job):
    return c.addSimJob(job)

def echo(data):
    return c.echo(data)
