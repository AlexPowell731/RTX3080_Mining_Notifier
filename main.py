import datetime
import json
import requests
from bs4 import BeautifulSoup

url = "https://whattomine.com/coins?aq_69xt=0&aq_68xt=0&aq_68=0&aq_67xt=1&aq_66xt=1&aq_vii=0&aq_5700xt=1&aq_5700=0" \
      "&aq_5600xt=0&aq_vega64=0&aq_vega56=0&aq_3090=1&aq_38Ti=0&aq_3080=1&aq_38L=0&aq_37Ti=0&aq_3070=1&aq_37L=1" \
      "&aq_3060Ti=0&aq_36TiL=0&aq_3060=0&aq_36L=0&aq_66=2&aq_55xt8=1&aq_580=1&aq_570=1&aq_480=3&aq_470=1&aq_fury=0" \
      "&aq_380=0&aq_a5=0&aq_a45=0&aq_a4=1&aq_a2=0&aq_2080Ti=0&aq_2080=0&aq_2070=0&aq_2060=0&aq_166s=1&aq_1660Ti=0" \
      "&aq_1660=2&aq_1080Ti=0&aq_1080=0&aq_1070Ti=0&aq_1070=0&aq_10606=0&aq_1050Ti=1&eth=true&factor%5Beth_hr%5D=98.0" \
      "&factor%5Beth_p%5D=315.0&factor%5Be4g_hr%5D=0.0&factor%5Be4g_p%5D=0.0&factor%5Bzh_hr%5D=0.0&factor%5Bzh_p%5D=0" \
      ".0&factor%5Bcnh_hr%5D=0.0&factor%5Bcnh_p%5D=0.0&factor%5Bcng_hr%5D=0.0&factor%5Bcng_p%5D=0.0&factor%5Bcnf_hr" \
      "%5D=0.0&factor%5Bcnf_p%5D=0.0&factor%5Bcx_hr%5D=0.0&factor%5Bcx_p%5D=0.0&factor%5Beqa_hr%5D=0.0&factor%5Beqa_p" \
      "%5D=0.0&factor%5Bcc_hr%5D=0.0&factor%5Bcc_p%5D=0.0&factor%5Bcr29_hr%5D=0.0&factor%5Bcr29_p%5D=0.0&factor" \
      "%5Bct31_hr%5D=0.0&factor%5Bct31_p%5D=0.0&factor%5Bct32_hr%5D=0.0&factor%5Bct32_p%5D=0.0&factor%5Beqb_hr%5D=0.0" \
      "&factor%5Beqb_p%5D=0.0&factor%5Brmx_hr%5D=0.0&factor%5Brmx_p%5D=0.0&factor%5Bns_hr%5D=0.0&factor%5Bns_p%5D=0.0" \
      "&factor%5Bal_hr%5D=0.0&factor%5Bal_p%5D=0.0&factor%5Bops_hr%5D=0.0&factor%5Bops_p%5D=0.0&factor%5Beqz_hr%5D=0" \
      ".0&factor%5Beqz_p%5D=0.0&factor%5Bzlh_hr%5D=0.0&factor%5Bzlh_p%5D=0.0&factor%5Bkpw_hr%5D=0.0&factor%5Bkpw_p%5D" \
      "=0.0&factor%5Bppw_hr%5D=0.0&factor%5Bppw_p%5D=0.0&factor%5Bx25x_hr%5D=0.0&factor%5Bx25x_p%5D=0.0&factor" \
      "%5Bfpw_hr%5D=0.0&factor%5Bfpw_p%5D=0.0&factor%5Bvh_hr%5D=0.0&factor%5Bvh_p%5D=0.0&factor%5Bcost%5D=0.26&factor" \
      "%5Bcost_currency%5D=USD&sort=Profit24&volume=0&revenue=24h&factor%5Bexchanges%5D%5B%5D=&factor%5Bexchanges%5D" \
      "%5B%5D=binance&factor%5Bexchanges%5D%5B%5D=bitfinex&factor%5Bexchanges%5D%5B%5D=bitforex&factor%5Bexchanges%5D" \
      "%5B%5D=bittrex&factor%5Bexchanges%5D%5B%5D=coinex&factor%5Bexchanges%5D%5B%5D=dove&factor%5Bexchanges%5D%5B%5D" \
      "=exmo&factor%5Bexchanges%5D%5B%5D=gate&factor%5Bexchanges%5D%5B%5D=graviex&factor%5Bexchanges%5D%5B%5D=hitbtc" \
      "&factor%5Bexchanges%5D%5B%5D=hotbit&factor%5Bexchanges%5D%5B%5D=ogre&factor%5Bexchanges%5D%5B%5D=poloniex" \
      "&factor%5Bexchanges%5D%5B%5D=stex&dataset=Main&commit=Calculate "

power_cost = '$0.26'
power_usage = '315w'
# date = date.today()
time_now = datetime.datetime.now().strftime("%H:%M:%S")


# Get all the html from the page
def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def parse(soup):
    # Finds all matching content on site (ETH table of results on whattomine)
    results = soup.find_all('tr', {'class': 'table-success'})
    values = []
    for item in results:
        # Finds all <strong> tags (figures we want off of whattomine) and replaces unwanted text
        details = str(item.find_all('strong')).replace('<strong>', '').replace('</strong', '').replace('\n', '') \
            .replace('>', '').replace(',', '').replace('[', '').replace(']', '').split()
        values.append(details)
    return values


soup = get_data(url)
data = parse(soup)

# Assign results to dictionary for future use
results = {
    'profit_per_day': data[0][3],
    'difficulty': data[0][0],
    # 'date': date,
    'time': time_now
}

json_object = json.dumps(results, default=str)


def check_results(results):
    if results['profit_per_day'][0] == '$':
        payload = {
            "content": "ETH Mining Stats - RTX 3080\n" +
                       "------------------------------------------------------------------" +
                       f"\nAt power cost of: {power_cost}/KWH and power usage of: {power_usage}. ETH Mining is "
                       f"PROFITABLE! \n" + json_object.replace("{", '').replace("}", '').replace('"', '').replace
                       (" ", "").replace(",", '\n').replace("difficulty", 'Difficulty').replace
                       ("profit_per_day", 'Profit Per Day').replace("date:", 'Date: ').replace("time:", 'Time: ')
        }

        header = {
            "authorization": "OTk2ODQzNDc3OTkwMTMzNzkw.GiyUFH.4HCoUjya5BOsqoQ6IdFjKKWeN1FsV9oGI7ulJk"
        }

        req = requests.post("https://discord.com/api/v9/channels/999736607613648897/messages", data=payload,
                            headers=header)
    else:
        payload = {
            "content": "ETH Mining Stats - RTX 3080\n" +
                       "------------------------------------------------------------------" +
                       f"\nAt power cost of: {power_cost}/KWH and power usage of: {power_usage}. ETH Mining is NOT "
                       f"profitable! \n" + json_object.replace("{", '').replace("}", '').replace('"', '').replace
                       (" ", "").replace(",", '\n').replace("difficulty", 'Difficulty').replace
                       ("profit_per_day", 'Profit Per Day').replace("date:", 'Date: ').replace("Time: :", 'Time: ')
        }

        header = {
            "authorization": "OTk2ODQzNDc3OTkwMTMzNzkw.GiyUFH.4HCoUjya5BOsqoQ6IdFjKKWeN1FsV9oGI7ulJk"
        }

        req = requests.post("https://discord.com/api/v9/channels/999736607613648897/messages", data=payload,
                            headers=header)


check_results(results)
