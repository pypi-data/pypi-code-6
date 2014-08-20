# encoding: utf-8

from api import PublisherApi, random_string

if __name__ == "__main__":
    api = PublisherApi(
        connect_id='9010F8C4AD9955DBDC9F',
        secret_key='0fd3c88a205f45+Fba833622e3e859/B4453c74c',
    )
    applications = api.get('programapplications', status='confirmed', adspace=897026, items=50)
    page_numbers = api.get_page_numbers(applications)
  
    for page_number in page_numbers:
        applications = api.get('programapplications', status='confirmed', adspace=897026, items=50, page=page_number)
        pass
        try:
            application_items = applications['programApplicationItems']['programApplicationItem']
        except:
            print applications
        
        for application in application_items:
            application_is_active = application['program']['@active'] == 'true'
            program_id = application['program']['@id']
            if application_is_active:
                program = api.get('programs/program/{0}'.format(program_id))
                if program:
                    print application['program']['$']
                    website = program['programItem'][0]['url']
                    tracking_url = api.get_tracking_url(website, 897026)
                    if tracking_url:
                        program_reference = api.get_program_identifier(tracking_url)
                        print program_reference
                    print website
                    print tracking_url       
        
 
 
    
    
