from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup as bs
import requests

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
    url = f"https://www.confirmtkt.com/pnr-status?pnr={pnr_number}"
    response = requests.get(url)
    return response.content

def scrape_pnr_status_info(page_content):
    soup = bs(page_content, features="lxml")
    div_html = soup.find('div', {'id': 'passenger-info-container'})
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
