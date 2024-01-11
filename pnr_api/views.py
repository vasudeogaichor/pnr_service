from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PNRStatusApiView(APIView):
    def get(self, request, pnr_number, *args, **kwargs):
        try:
            page_content = get_pnr_status_page(pnr_number)
            pnr_status = scrape_pnr_status_info(page_content)
            if len(pnr_status):
                return Response(pnr_status, status=status.HTTP_200_OK)
        except Exception as e:
            print('Operation exception occurred - ', e)
            return Response({"res": "Unavailable, please check the PNR number"}, status=status.HTTP_400_BAD_REQUEST)

def get_pnr_status_page(pnr_number):
    url = f"https://www.confirmtkt.com/pnr-status/{pnr_number}"

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.ID, 'passenger-info-container')))

    page_source = driver.page_source

    driver.quit()

    return page_source

def scrape_pnr_status_info(page_content):
    soup = bs(page_content, 'html5lib')
    div_html = soup.find('div', {'id': 'passenger-info-container'})
    tbody_html = div_html.find('tbody')
    tr_html = tbody_html.find_all('tr')
    
    passengers_details = []
    for row in tr_html:
        all_td = row.find_all('td')
        passenger = {
            "sr_no": int(all_td[0].find('span').text),
            "current_status": all_td[1].find('span').text,
            "booking_status": all_td[2].find('span').text,
        }
        passengers_details.append(passenger)
    return passengers_details
