############### The class that compares the key-values ################


class Comparer:
    def __init__(self, programs, percentage):
        self.programs = programs
        self.total_comparisons = 0
        self.percentage = percentage
        self.result = {}
        self.do_the_work()

    def do_the_work(self):
        self.point_dict = {}
        self.avg_points_dict = {}
        sum_points = 0
        for i in range(0, len(self.programs), 1):
            for j in range(i + 1, len(self.programs), 1):
                sum_points, details = self.compare(self.programs[i], self.programs[j])
                self.total_comparisons += 1
                if not sum_points in self.result:
                    self.result[sum_points] = []
                self.result[sum_points].append((self.programs[i], self.programs[j], details))
        if sum_points:
            self.sum_points = sum_points / len(self.programs)
        #print "Total number of comparisons was " + str(self.total_comparisons) + "\n"

    def compare(self, a, b):
        # using points
        self.points = 0
        summary = []  # a list of lines which make up the summary for a given compare
        if a.detektor_signature.bigstring == b.detektor_signature.bigstring:
            self.points += 10
            # The string containing keywords and operators match.
            summary.append('Programs very similar. Look for use of query-replace.')
        if a.detektor_signature.keywordstring == b.detektor_signature.keywordstring:
            self.points += 3
            # Same number of each keywords used.
            if not a.detektor_signature.bigstring == b.detektor_signature.bigstring:
                summary.append('Equal number of each keyword used.')
        if a.detektor_signature.operatorstring == b.detektor_signature.operatorstring:
            self.points += 3
            if not a.detektor_signature.bigstring == b.detektor_signature.bigstring:
                summary.append('Same number of each operator used.')
        if a.detektor_signature.number_of_keywords == b.detektor_signature.number_of_keywords:
            self.points += 1
            if not a.detektor_signature.bigstring == b.detektor_signature.bigstring:
                summary.append('Equal total number of keywords.')
        if a.detektor_signature.number_of_operators == b.detektor_signature.number_of_operators:
            self.points += 1
            if not a.detektor_signature.bigstring == b.detektor_signature.bigstring:
                summary.append('Equal number of operators.')
        num_equal_funcs = 0
        for fhash1 in a.detektor_signature.list_of_functions:
            for fhash2 in b.detektor_signature.list_of_functions:
                if fhash1 == fhash2:
                    self.points += 3
                    num_equal_funcs += 1
        if num_equal_funcs:
            if not a.detektor_signature.bigstring == b.detektor_signature.bigstring:
                self.points = num_equal_funcs
                summary.append('Query-replace may have been used to make function(s) look different.')
        return self.points, summary

    #def get_result(self):
    #    return self.result

    def get_result(self):
        res = []
        keys = sorted(self.result.keys(), reverse=True)
        for key in keys:
            for r, s, t in self.result.get(key):
                res.append({
                    'points': key,
                    'object1': r,
                    'object2': s,
                    'details': t,
                    })
        return res

    def build_result(self):
        res = []
        keys = self.point_dict.keys()
        #limit = avg + avg * self.percentage / 100
        # limit = 1
        keys.sort()
        # print the highest scores first
        for i in range(len(keys) - 1, -1, -1):
            for p in self.point_dict[keys[i]]:
                avg = self.avg_points_dict[p[0]]
                if not avg:
                    break
                limit = avg + avg * self.percentage / 100
                if keys[i] >= limit:
                    #print keys[i],'points:',p[:-1],''
                    t = (p[0], p[1], p[2], p[3], keys[i], avg, p[4])
                    res.append(t)
                if keys[i] < limit:
                    break  # break out of this inner loop
        return res
