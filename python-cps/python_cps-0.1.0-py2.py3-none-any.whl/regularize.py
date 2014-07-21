"""
Transform the data to be consistent.
"""

#-----------------------------------------------------------------------------
# Operations on values

def special_by_dd(keys):
    """All of these are inplace"""
    def expand_year(df, dd_name):
        """ For jan1989 - sep1995 they wrote the year as a SINGLE DIGIT"""
        if 'HRYEAR' in df.columns:
            k = 'HRYEAR'
        else:
            k = k = 'HdYEAR'
        last_digit = df[k].dropna().unique()[0]
        if last_digit >= 10:
            last_digit = last_digit % 10
        base_year = int(dd_name[-4:-1]) * 10
        df["HRYEAR4"] = base_year + last_digit
        df = df.drop(k, axis=1)
        return df

    def combine_age(df, dd_name):
        """For jan89 and jan92 they split the age over two fields."""
        df["PRTAGE"] = df["AdAGEDG1"] * 10 + df["AdAGEDG2"]
        df = df.drop(["AdAGEDG1", "AdAGEDG2"], axis=1)
        return df

    def align_lfsr(df, dd_name):
        """Jan1989 and Jan1999. LFSR (labor focrce status recode)
        had
           1 = WORKING
           2 = WITH JOB,NOT AT WORK
           3 = UNEMPLOYED, LOOKING FOR WORK
           4 = UNEMPLOYED, ON LAYOFF
           5 = NILF - WORKING W/O PAY < 15 HRS;
                      TEMP ABSENT FROM W/O PAY JOB
           6 = NILF - UNAVAILABLE
           7 = OTHER NILF
        newer ones have
           1   EMPLOYED-AT WORK
           2   EMPLOYED-ABSENT
           3   UNEMPLOYED-ON LAYOFF
           4   UNEMPLOYED-LOOKING
           5   NOT IN LABOR FORCE-RETIRED
           6   NOT IN LABOR FORCE-DISABLED
           7   NOT IN LABOR FORCE-OTHER
        this func does several things:
            1. Change 3 -> 4 and 4 -> 3 in the old ones.
            2. Change 5 and 6 to 7.
            2. Read retired from AhNLFREA == 4 and set to 5.
            3. Read ill/disabled from AhNLFREA == 2 and set to 6.
        Group 7 kind of loses meaning now.
        """
        # 1. realign 3 & 3
        status = df["AhLFSR"]
        # status = status.replace({3: 4, 4: 3})  # chcek on ordering

        status_ = status.copy()
        status_[status == 3] = 4
        status_[status == 4] = 3
        status = status_

        # 2. Add 5 and 6 to 7
        status = status.replace({5: 7, 6: 7})

        # 3. ill/disabled -> 6
        status[df['AhNLFREA'] == 2] = 6

        df['PEMLR'] = status
        df = df.drop(["AhLFSR", "AhNLFREA"], axis=1)
        return df

    def expand_hours(df, dd_name):
        """
        89 and 92 have a question for hours and bins. I goto midpoint of bin.

        Roughly corresponds to PEERNHRO

        A-EMPHRS    CHARACTER*002 .     (0357:0358)           LFSR=1 OR 2
           REASONS NOT AT WORK OR HOURS AT WORK
           -1 = NOT IN UNIVERSE
           WITH A JOB, BUT NOT AT WORK
           01 = ILLNESS
           02 = VACATION
           03 = BAD WEATHER
           04 = LABOR DISPUTE
           05 = ALL OTHER
           AT WORK
           06 = 1-4 HOURS
           07 = 5-14 HOURS
           08 = 15-21 HOURS
           09 = 22-29 HOURS
           10 = 30-34 HOURS
           11 = 35-39 HOURS
           12 = 40 HOURS
           13 = 41-47 HOURS
           14 = 48 HOURS
           15 = 49-59 HOURS
           16 = 60 HOURS OR MORE
        """
        hours = df['AhEMPHRS']
        hours_dic = {1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan, 5: np.nan,
                     6: 2, 7: 9.5, 8: 18, 9: 25.5, 10: 32, 11: 37, 13: 44,
                     15: 54}
        hours = hours.replace(hours_dic)
        df['PEERNHRO'] = hours
        df.drop("AhEMPHRS", axis=1)
        return df

    def combine_hours(df, dd_name):
        """
        For 89 and 92; "AdHRS1", "AdHRS2" combine to form "PEHRACTT"
        """
        fst = df['AdHRS1']
        snd = df['AdHRS2']
        df['PEHRACTT'] = fst * 10 + snd
        df = df.drop(["AdHRS1", "AdHRS2"], axis=1)
        return df

    func_dict = {"expand_year": expand_year, "combine_age": combine_age,
                 "expand_hours": expand_hours, "align_lfsr": align_lfsr,
                 "combine_hours": combine_hours}
    to_apply = filter(lambda x: x in keys, func_dict)
    filtered = {k: func_dict[k] for k in to_apply}
    return filtered

#-----------------------------------------------------------------------------
# Operations on IDS

def standardize_cols(df, dd_name, settings):
    """
    Rename cols in df according to the spec in settings for that year.

    standaradize_cols :: df -> str -> dict -> df
    """
    renamer = settings["col_rename_by_dd"][dd_name]
    df = df.rename(columns=renamer)

    common = {"PRTAGE", "HRMIS", "HRYEAR4", "PESEX", "HRMONTH", "PTDTRACE",
              "PEMLR", "PRERNWA", "PTWK", "PEMARITL", "PRDISC",
              "HEFAMINC", "PTDTRACE", "HWHHWGT", "PEERNHRY", "HRMIS"}
    cols = set(df.columns.tolist())
    extra = cols - common
    missing = common - cols

    if missing:
        name = str(df.HRYEAR4.iloc[0]) + str(df.HRMONTH.iloc[0])
        key = ' '.join([str(arrow.utcnow()), name, 'missing'])
        d = {key: list(missing)}
        with open('make_hdf_store_log.json', 'a') as f:
            json.dump(d, f, indent=2)

    if extra:
        name = str(df.HRYEAR4.iloc[0]) + str(df.HRMONTH.iloc[0])
        key = ' '.join([str(arrow.utcnow()), name, 'extra'])
        d = {key: list(extra)}
        with open('make_hdf_store_log.json', 'a') as f:
            json.dump(d, f, indent=2)

    return df

def standardize_ids(df):
    """
    pre may2004 need to fill out the ids by creating HRHHID2 manually:
    (ignore the position values, this is from jan2013)

    HRHHID2        5         HOUSEHOLD IDENTIFIER (part 2) 71 - 75

         EDITED UNIVERSE:    ALL HHLD's IN SAMPLE

         Part 1 of this number is found in columns 1-15 of the record.
         Concatenate this item with Part 1 for matching forward in time.

         The component parts of this number are as follows:
         71-72     Numeric component of the sample number (HRSAMPLE)
         73-74     Serial suffix-converted to numerics (HRSERSUF)
         75        Household Number (HUHHNUM)

    NOTE: not documented by sersuf of -1 seems to map to '00'
    """
    import string

    hrsample = df['HRSAMPLE'].str.extract(r'(\d+)')
    hrsersuf = df['HRSERSUF'].astype(str)
    huhhnum = df['HUHHNUM'].astype(str)

    sersuf_d = {a: str(ord(a.lower()) - 96).zfill(2) for a in hrsersuf.unique()
                if a in list(string.ascii_letters)}
    sersuf_d['-1.0'] = '00'
    sersuf_d['-1'] = '00'
    hrsersuf = hrsersuf.map(sersuf_d)  # 10x faster than replace
    hrhhid2 = (hrsample + hrsersuf + huhhnum).dropna()
    return hrhhid2.astype(np.int64)
