#This script is created to compare the same page on a production environment and on a staging environment to make sure there are no unexpected changes.
#Applitools is used to create a baseline from the production site.
#There is an option to test a whole page at once.
#There is a .xlsx file saved in private location. The domain is the only difference in the production URL and the staging URL. All credentials are removed.


from applitools.eyes import Eyes, BatchInfo
from selenium import webdriver
import openpyxl


def main():

    customer="winterfest"
    url_file_name="book_url_to_be_checked.xlsx"
    protocol ="https://"

    # Initialize the eyes SDK and set your private API key.
    eyes = Eyes()
    eyes.api_key = <<<<<API key here>>>>>>
    mybatch = BatchInfo(customer)

    # Testing whole web page
    eyes.force_full_page_screenshot = True
    eyes.hide_scrollbars = True
    eyes.use_css_transition = True

    eyes.batch = mybatch

    print('Opening workbook...')
    wb = openpyxl.load_workbook(url_file_name)
    sheet = wb[customer]

    domain_live = sheet['A' + str(2)].value.split('//', 1)[1].split('/', 1)[0]
    domain_staging = sheet['B' + str(2)].value.split('//', 1)[1].split('/', 1)[0]
    username_staging = sheet['C' + str(2)].value
    password_staging = sheet['D' + str(2)].value

    print("Base data for the client:", customer, "\nLiveURL: ", domain_live, "\nStagingURL: "+ domain_staging,
          "\nStaging_username: "+username_staging)

    print('\n **** Reading rows... ****')
    #
    url_list=[]

    for row in range(2, sheet.max_row + 1):
    #Creating a dictionary "info" with two elements add into the list "url_list":

        if (sheet['F' + str(row)].value==None) or (sheet['E' + str(row)].value==None):
            print("Skiped empty row: ", row)
        else:
            info = {}
            info['menu_title'] = sheet['E' + str(row)].value
            #removing the domain from url
            info['menu_path'] = ''.join(sheet['F' + str(row)].value.split('//', 1)[1].split('/', 1)[1:])
            url_list.append(info)

    driver = webdriver.Chrome()

    for item in url_list:
        #domain_live

        print("Test Live: ", item['menu_title'], protocol+domain_live+"/"+item['menu_path'])

        driver.get(protocol+domain_live+"/"+item['menu_path'])

        eyes.open(driver=driver, app_name=customer, test_name=item['menu_title'], viewport_size={'width': 800, 'height': 600})
        try:
            eyes.check_window(item['menu_title'])
        finally:
            eyes.close()

        print("Test Staging: ", item['menu_title'], protocol + domain_staging + "/"+item['menu_path'])
        driver.get(protocol + domain_staging + "/" + item['menu_path'])

        eyes.open(driver=driver, app_name=customer, test_name=item['menu_title'], viewport_size={'width': 800, 'height': 600})
        try:
            eyes.check_window(item['menu_title'])
        finally:
            eyes.close()


   # driver.close()

if __name__ == "__main__":
    main()
