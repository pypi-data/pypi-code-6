def get_coach_data(filename):
    try:
        with open(filename) as f:
            data=f.readline()
            data_hash={}
            arr=data.strip().split(",")
            data_hash['Name']= arr.pop(0)
            data_hash['DOB'] = arr.pop(0)
            name=data_hash['Name']
            dob=data_hash['DOB']           
            return(name,dob,arr)
    except IOError as ioerr:
        print('File error'+str(ioerr))
        return(None)
        
