from dateutil.parser import parse


class DateRangeMixin(object):

    def get_default_start(self):
        return None

    def get_default_end(self):
        return None

    def get_range(self):
        default_start = self.get_default_start()
        default_end = self.get_default_end()
        start = self.request.GET.get("start", default_start)
        end = self.request.GET.get("end", default_end)
        if end:
            end = parse(end).date()
        else:
            end = default_end

        if start:
            start = parse(start).date()
        else:
            start = default_start

        return start, end

    # def get_context_data(self, **kwargs):
    #     start, end = self.get_range()
    #     return super(DateRangeMixin, self).get_context_data(
    #         start=start,
    #         end=end,
    #         **kwargs
    #     )
