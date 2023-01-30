from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs


class PNRStatusApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, pnr_number, *args, **kwargs):
        '''
        Get status for given requested pnr
        '''
        try:
        #     return Response([
        #         {
        #     "sr_no": 1,
        #     "current_status": "CNF D3 25",
        #     "booking_status": "CNF D3 25",
        # },
        #         {
        #     "sr_no": 1,
        #     "current_status": "CNF D3 25",
        #     "booking_status": "CNF D3 25",
        # }], status=status.HTTP_200_OK)
            page = get_pnr_status_page(pnr_number)
            pnr_status = scrape_pnr_status_info(page)
            if len(pnr_status):
                return Response(pnr_status, status=status.HTTP_200_OK)
        except:
                return Response({"res": "Unavailable, please check the PNR number"}, status=status.HTTP_400_BAD_REQUEST) 

def get_pnr_status_page(pnr_number):
    dr = webdriver.Chrome(service=Service(ChromeDriverManager().install())) #chrome_options=chrome_options)
    dr.get("https://www.confirmtkt.com/pnr-status")
    pnr = dr.find_element('id',"pnr-text")
    pnr.clear()
    pnr.send_keys(pnr_number)
    dr.find_element('css selector','button.col-xs-4.btn.btn-success.btn-proceed').click()
    return dr

def scrape_pnr_status_info(page):
    html = page.page_source
    soup = bs(html, features="lxml")
    div_html = soup.find('div',{'id': 'passenger-info-container'})
    tbody_html = div_html.find('tbody')
    tr_html = tbody_html.find_all('tr')
    passengers_details = []
    for row in tr_html:
        all_td = row.find_all('td')
        passenger = {
            "sr_no": int(all_td[0].text),
            "current_status": all_td[1].find('span').text,
            "booking_status": all_td[2].find('span').text,
        }
        passengers_details.append(passenger)
    return passengers_details