from celery import task


@task(ignore_result=True)
def process_image(id, original, result, **options):
    engine.do_process_image(id, original.fullname, result.fullname, **options)
