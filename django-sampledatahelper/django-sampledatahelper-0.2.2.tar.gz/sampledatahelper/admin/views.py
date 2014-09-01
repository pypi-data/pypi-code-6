from django.db.models.loading import get_model
from sampledatahelper.model_helper import ModelDataHelper

def add_sample(request, app_label, model):
    mdh = ModelDataHelper(seed=12345678901)
    if filter(lambda x: x['model'] == "{}.{}".format(app_label, model), settings.SAMPLEDATAHELPER_MODELS):
        model = get_model(app_label, model)
        instance = model()
        mdh.fill_model_instance(instance)
        instance.save()
