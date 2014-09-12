# -*- coding: utf-8 -*-


def get_celery_worker_status():
    from celery import current_app

    return current_app.control.inspect().stats()