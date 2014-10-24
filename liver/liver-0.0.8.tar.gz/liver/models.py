from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy, ugettext as _

import datetime, time, pytz, calendar
import simplejson as json
import uuid

class SourcesGroup(models.Model):
    name = models.CharField(max_length=5000,verbose_name="Common Name")
    external_id = models.CharField(max_length=5000,verbose_name="External Id.")

    insertion_date = models.DateTimeField(editable=False)
    modification_date = models.DateTimeField(auto_now=True,
            auto_now_add=True, blank=True, null=True)
    default_offset_start = models.IntegerField(null=True, blank=True,
            verbose_name="Default offset start (in seconds)")
    default_offset_end = models.IntegerField(null=True, blank=True,
            verbose_name="Default offset end (in seconds)")
    default_availability_window = models.IntegerField(null=True, blank=True,
            verbose_name="Default availability window (in hours)")

    def clone(self):
        sg = SourcesGroup()
        if self.name and self.name.find(" (Clone") >= 0:
            sg.name = self.name[:self.name.find(" (Clone")] \
                    + " (Clone %s)" % int(time.time())
        else:
            sg.name = self.name + " (Clone %s)" % int(time.time())
        sg.external_id = self.external_id
        sg.default_offset_start = self.default_offset_start
        sg.default_offset_end = self.default_offset_end
        sg.default_availability_window = self.default_availability_window

        sg.save()

        for s in self.source_set.all():
            s_clone = s.clone()
            s_clone.sources_group = sg
            s_clone.save()

        return sg

    def save(self, *args, **kwargs):
        if not self.insertion_date:
            d = datetime.datetime.fromtimestamp(time.time(), pytz.UTC)
            self.insertion_date = d
        super(SourcesGroup, self).save(*args, **kwargs)

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"%s [%s]" % (slugify(self.name),
                self.external_id)



class Source(models.Model):
    name = models.CharField(max_length=5000,verbose_name="Common Name")
    external_id = models.CharField(max_length=5000,verbose_name="External Id.")
    uri = models.CharField(max_length=5000,verbose_name="URI")

    insertion_date = models.DateTimeField(editable=False)
    modification_date = models.DateTimeField(auto_now=True,
            auto_now_add=True, blank=True, null=True)

    sources_group = models.ForeignKey(SourcesGroup, null=True, blank=True)

    def clone(self):
        s = Source()
        if self.name and self.name.find(" (Clone") >= 0:
            s.name = self.name[:self.name.find(" (Clone")] \
                    + " (Clone %s)" % int(time.time())
        else:
            s.name = self.name + " (Clone %s)" % int(time.time())
        s.external_id = self.external_id
        s.uri = self.uri
        s.save()
        return s

    def save(self, *args, **kwargs):
        if not self.insertion_date:
            d = datetime.datetime.fromtimestamp(time.time(), pytz.UTC)
            self.insertion_date = d
        super(Source, self).save(*args, **kwargs)

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"%s [%s] [%s]" % (slugify(self.name), self.external_id,self.uri)


class Recorder(models.Model):
    name = models.CharField(max_length=5000)
    token = models.CharField(max_length=5000,default=str(uuid.uuid1()))

    def clone(self):
        r = Recorder()
        if self.name and self.name.find(" (Clone") >= 0:
            r.name = self.name[:self.name.find(" (Clone")] \
                    + " (Clone %s)" % int(time.time())
        else:
            r.name = self.name + " (Clone %s)" % int(time.time())
        r.token = self.token
        r.save()
        return r

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "%s [%s]" % (self.name, self.token)

class RecordSource(models.Model):
    external_id = models.CharField(max_length=5000,verbose_name="External Id.",
            default = "")
    sources_group = models.ForeignKey(SourcesGroup, null=True, blank=True)

    insertion_date = models.DateTimeField(editable=False)
    modification_date = models.DateTimeField(auto_now=True,
            auto_now_add=True, blank=True, null=True)
    enabled = models.BooleanField(default=True)
    enabled_since = models.DateTimeField(null=True, blank=True)
    enabled_until = models.DateTimeField(null=True, blank=True,
            default = None, verbose_name="Enabled to")

    def clone(self):
        rs = RecordSource()
        rs.external_id = self.external_id
        rs.sources_group = self.sources_group
        rs.enabled = False
        rs.enabled_since = self.enabled_since
        rs.enabled_until = self.enabled_until
        rs.save()
        rm_list = RecordMetadata.objects.filter(record_source=self)
        for rm in rm_list:
            rm_clone = rm.clone()
            rm_clone.record_source=rs
            rm_clone.save()
        rr_list = RecordRule.objects.filter(record_source=self)
        for rr in rr_list:
            rr_clone = rr.clone()
            rr_clone.record_source=rs
            rr_clone.save()
        return rs

    def save(self, *args, **kwargs):
        if not self.insertion_date:
            d = datetime.datetime.fromtimestamp(time.time(), pytz.UTC)
            self.insertion_date = d
        super(RecordSource, self).save(*args, **kwargs)

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "Record %s" % (unicode(self.sources_group))


class RecordMetadata(models.Model):
    record_source = models.ForeignKey(RecordSource)

    key = models.CharField(max_length=5000,blank=True)
    value = models.CharField(max_length=5000,blank=True)

    def clone(self):
        rm = RecordMetadata()
        rm.record_source = self.record_source
        rm.key = self.key
        rm.value = self.value
        rm.save()
        return rm

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "%s - %s" % (self.key, self.value)


class RecordRule(models.Model):
    record_source = models.ForeignKey(RecordSource)

    metadata_key_filter = models.CharField(max_length=5000,blank=True)
    metadata_value_filter = models.CharField(max_length=5000,blank=True)

    offset_start = models.IntegerField(null=True, blank=True,
            verbose_name="Offset start (in seconds)")
    offset_end = models.IntegerField(null=True, blank=True,
            verbose_name="Offset end(in seconds)")
    availability_window = models.IntegerField(null=True, blank=True,
            verbose_name="Availability window (in hours)")

    def clone(self):
        rr = RecordRule()
        rr.record_source = self.record_source
        rr.metadata_key_filter = self.metadata_key_filter
        rr.metadata_value_filter = self.metadata_value_filter
        rr.offset_start = self.offset_start
        rr.offset_end = self.offset_end
        rr.availability_window = self.availability_window
        rr.save()
        return rr

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "[%s:%s] [start:%s,end:%s] (%s)" \
    % (self.metadata_key_filter,
       self.metadata_value_filter,
       self.offset_start,
       self.offset_end,
       self.availability_window)


class RecordJob(models.Model):
    class Meta:
        verbose_name = _('Record job')

    status_choices = [
        ('waiting', _('Waiting')),
        ('running', _('Running')),
        ('failed', _('Failed')),
        ('successful', _('Successful')),
        ('cancelled', _('Cancelled')),
    ]

    record_source = models.ForeignKey(RecordSource, null=True, blank=True,
                        on_delete=models.SET_NULL)

    sources_group = models.ForeignKey(SourcesGroup)

    insertion_date = models.DateTimeField(editable=False)
    modification_date = models.DateTimeField(auto_now=True,
            auto_now_add=True, blank=True, null=True)
    execution_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)

    scheduled_start_date = models.DateTimeField(null=True, blank=True)
    scheduled_duration = models.IntegerField(
            verbose_name="Scheduled duration (in seconds)")

    enabled = models.BooleanField(default=True)

    recorder =  models.ForeignKey(Recorder, null=True, blank=True,
            on_delete=models.SET_NULL)

    result = models.CharField(max_length=5000, blank=True, null=True,
            verbose_name=_('Result'),default="None")
    status = models.CharField(max_length=5000,
            verbose_name=_('Status'),
            choices=status_choices)

    def get_scheduled_start_timestamp(self):
        return calendar.timegm(
            self.scheduled_start_date.astimezone(
                pytz.utc).utctimetuple())
    scheduled_start_timestamp = property(get_scheduled_start_timestamp)

    def clone(self):
        rj = RecordJob()
        rj.record_source = self.record_source
        rj.sources_group = self.sources_group
        rj.scheduled_start_date = self.scheduled_start_date
        rj.scheduled_duration = self.scheduled_duration
        rj.enabled = self.enabled
        rj.save()
        rjm_list = RecordJobMetadata.objects.filter(record_job=self)
        for rjm in rjm_list:
            rjm_clone = rjm.clone()
            rjm_clone.record_job=rj
            rjm_clone.save()
        return rj

    def save(self, *args, **kwargs):
        if not self.insertion_date:
            d = datetime.datetime.fromtimestamp(time.time(), pytz.UTC)
            self.insertion_date = d
        super(RecordJob, self).save(*args, **kwargs)

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "%s [start:%s, duration:%s]" \
    % (self.sources_group,
       self.scheduled_start_date,
       self.scheduled_duration)



class RecordJobMetadata(models.Model):
    record_job = models.ForeignKey(RecordJob)

    key = models.CharField(max_length=5000,blank=True)
    value = models.CharField(max_length=5000,blank=True)

    def clone(self):
        rjm = RecordJobMetadata()
        rjm.record_job = self.record_job
        rjm.key = self.key
        rjm.value = self.value
        rjm.save()
        return rjm

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "%s - %s" % (self.key, self.value)


class Record(models.Model):
    record_job = models.ForeignKey(RecordJob, on_delete=models.SET_NULL,
            null=True, blank=True,
            verbose_name="Associated record job")
    recorder = models.ForeignKey(Recorder, on_delete=models.SET_NULL,
            null=True, blank=True,
            verbose_name="Associated recorder")

    name = models.CharField(max_length=5000,blank=True,editable=False)

    insertion_date = models.DateTimeField(editable=False)
    modification_date = models.DateTimeField(auto_now=True,
            auto_now_add=True, blank=True, null=True)

    metadata_json = models.TextField(max_length=5000,blank=True,editable=False) # json
    def get_metadata(self):
        try:
          res = ""
          m_list = json.loads(self.metadata_json)
          for m in m_list:
              res +=\
"%s:%s\n" % (m.keys()[0], m.values()[0])
        except Exception:
          res = self.metadata_json
        return res
    metadata = property(get_metadata)

    profiles_json = models.TextField(max_length=5000,blank=True,editable=False) # json
    def get_profiles(self):
        try:
          res = ""
          p_list = json.loads(self.profiles_json)
          for p in p_list:
              res +=\
"uri:%(uri)s file:%(destination)s\n"  % p

        except Exception:
          res = self.profiles_json
        return res
    profiles = property(get_profiles)

    to_delete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.insertion_date:
            d = datetime.datetime.fromtimestamp(time.time(), pytz.UTC)
            self.insertion_date = d
        # TODO: Implementar la logica que decide si el flag to_delete se
        # activa o no
        super(Record, self).save(*args, **kwargs)

    def delete(self, using=None):
        if self.to_delete:
            return super(Record, self).delete()
        else:
            self.to_delete = True
            self.save()

    def clone(self):
        r = Record()
        if self.name and self.name.find(" (Clone") >= 0:
            r.name = self.name[:self.name.find(" (Clone")] \
                    + " (Clone %s)" % int(time.time())
        else:
            r.name = self.name + " (Clone %s)" % int(time.time())

        r.metadata_json = self.metadata_json
        r.profiles_json = self.profiles_json
        r.record_job = self.record_job
        r.save()
        return r

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "%s" % (self.name)




