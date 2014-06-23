import unittest
import logging

from ..client import InteractClient
from ..types import InteractObject, ListMergeRule, RecordData


logging.disable(logging.CRITICAL)

class ResponsysIntegrationTest(unittest.TestCase):
    "Responsys Integration InteractClient"

    def setUp(self):
        self.MASTER_FOLDER = 'UDEMY_TEST_FOLDER'
        self.MCL_OBJECT = 'CONTACTS_LIST_TEST'
        self.username = 'api@udemy'
        self.password = 'Murfyzf8TG8cuNY'
        self.pod = '5'
        self.client = InteractClient(self.username, self.password, self.pod)

    def test_connects_and_does_stuff(self):
        with self.client as client:
            list_ = InteractObject(self.MASTER_FOLDER, self.MCL_OBJECT)
            members = client.retrieve_list_members(
                list_,
                'CUSTOMER_ID',
                ['First_Name', 'Last_Name', 'Email_Address_'],
                list(range(1, 200))
            )
            self.assertTrue(len(members))
            record_data = [{
                 'Customer_Id_': 90000,
                 'First_Name': 'Foo',
                 'Last_Name': 'Bar',
                 'Email_Address_': 'email@email.com',
                 'Email_Permission_Status_': 'I',
                 'Registration_Date': '01/01/01',
                 'OPTOUT_LINK': '',
                 'COUNTRY_': '',
                 'Lang_Locale': '',
                 'Date_Of_Birth': '',
                 'Gender': '',
                 'Active_Status': '',
                 'Course_Category_1': '',
                 'Course_Category_2': '',
                 'Course_Category_3': '',
                 'Course_Category_4': '',
                 'Course_Category_5': '',
                 'Course_Category_6': '',
                 'Course_Category_7': '',
                 'Course_Category_8': '',
                 'Course_Category_9': '',
                 'Course_Category_10': '',
                 'Course_Category_11': '',
                 'Course_Category_12': '',
                 'Course_Category_13': '',
                 'Course_Category_14': '',
                 'Course_Category_15': '',
                 'Last_Login': '',
                 'Number_Of_Logins': '',
                 'Number_Of_Published_Courses': '',
                 'Number_Of_Published_HQ_Courses': '',
                 'Number_Of_Free_Courses': '',
                 'Number_Of_Paid_Courses': '',
                 'Number_Of_Courses_Created': '',
                 'FB_User_Id': '',
                 'Signup_Source': '',
                 'Is_Premium_Instructor': '',
                 'Is_Affiliate': '',
                 'POSTAL_STREET_1_': '',
                 'CITY_': '',
                 'STATE_': '',
                 'Postal_Code_': '',
                 'User_Locale': 'en_US',
                 'Platform': '',
                 'SOURCE_ORGANIZATION_ID': '',
                 'LAST_PURCHASE_DATE': '',
                 'LAST_PAID_PURCHASE_DATE': '',
                 'TIMEZONE': '',
                 'UTC_DIFF': '',
            }]
            record_data = RecordData(record_data)
            merge_response = client.merge_list_members(list_, record_data, ListMergeRule())
            client.delete_list_members(list_, 'CUSTOMER_ID', [90000])
