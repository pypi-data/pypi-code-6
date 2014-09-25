import requests
import lxml.etree as et

class NSLDS():

    # Class Variables
    host = 'https://www.nslds.ed.gov'
    entry_link = '/nslds_SA/SaPrivacyConfirmation.do'
    accept_link = '/nslds_SA/SaFinPrivacyAccept.do'
    login_link = '/nslds_SA/SaFinLoginPage.do'
    login_action = '/nslds_SA/SaFinLogin.do'
    loan_download = '/nslds_SA/SaFinShowMyDataConfirm.do'
    download_confirm = '/nslds_SA/MyData/MyStudentData.do'

    def __init__(self,**kwargs):
        self.borrower_ssn = kwargs.get('borrower_ssn')
        self.borrower_name = kwargs.get('borrower_name')
        self.borrower_dob = kwargs.get('borrower_dob')
        self.pin = kwargs.get('pin')
        self.session_id = None

    def get_loan_data(self):
        #Create Session
        s = requests.Session()

        # Navigate to Login Page
        login_response = s.get(NSLDS.host + NSLDS.login_link)

        # Parse HTML for login page
        login_tree = et.HTML(login_response.content)

        # Get and set sessionId from login page
        input_html_elements = login_tree.findall('.//input')
        for input_element in input_html_elements:
            try:
                if input_element.attrib['name']=='sessionId':
                    self.session_id=input_element.attrib['value']
            except KeyError:
                pass

        # Get PIN selection grid
        grid={}
        select_html_elements = login_tree.findall('.//select')
        for select_element in select_html_elements:
            select_name = select_element.attrib['name']+'h'
            grid[select_name]={}
            # Each Select element has 10 options (0-9)
            options = select_element.findall('option')
            for option in options:
                val = option.attrib['value']
                pin_num = option.text
                grid[select_name][pin_num]=int(val)

        # Generate parameter list for login POST
        payload = {}
        payload['borrowerSsn'] = self.borrower_ssn
        payload['borrowerName'] = self.borrower_name
        payload['borrowerDob'] = self.borrower_dob
        payload['sessionId'] = self.session_id

        payload['yin1h']=grid['yin1h'][self.pin[0]]
        payload['yin2h']=grid['yin2h'][self.pin[1]]
        payload['yin3h']=grid['yin3h'][self.pin[2]]
        payload['yin4h']=grid['yin4h'][self.pin[3]]

        # POST login credentials
        post_response = s.post(NSLDS.host + NSLDS.login_action, data=payload)

        # Check for login errors
        error_tree = et.HTML(post_response.content)
        errors = error_tree.findall('.//li')
        if errors:
            print 'Encountered following errors while attempting login:'
            print errors

        # Download the Loan Data
        click_download_response = s.get(NSLDS.host + NSLDS.loan_download)
        confirm_download_response = s.get(NSLDS.host + NSLDS.download_confirm, data={'language':'en'})

        loan_data = confirm_download_response.content

        s.close()
        return loan_data
