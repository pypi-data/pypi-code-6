#Test cases definition

def main(self):
    driver = self.driver
    driver.get(self.base_url + "/")
    assert 1+1==2
    print 'Test Demo'
    # Test all data