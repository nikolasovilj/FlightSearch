import requests as r
import json

def get_token():

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    base_url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": "2u7NuAPuBWALCjzdecMgM8TpNbc1A9jF",
        "client_secret": "BM1uAOpcGGpWCfG1"
    }


    res = r.post(base_url, data=data, headers=headers)
    #print(res.text)

    res = json.loads(res.text)

    return res['access_token']



def make_request(src_iata, dest_iata, departure_date, return_date, numOfAdults, currency):
    token = get_token()

    header = dict()
    header['Authorization'] = "Bearer " + token

    base_url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={src_iata}&destinationLocationCode={dest_iata}&departureDate={departure_date}&returnDate={return_date}&adults={numOfAdults}&nonStop=false&max=20&currencyCode={currency}"
    
    #print(header)
    print(base_url)

    res = r.get(base_url, headers = header)
    status_code = res.status_code
    
    res = res.json()
    
    data = list()
    

    for item in res['data']:
        row = dict()
        row['numOfavSeats'] = item['numberOfBookableSeats']
        row['duration'] = item['itineraries'][0]['duration']
        row['departureNumOfTransfers'] = len(item['itineraries'][0]['segments'])
        row['src_iata'] = item['itineraries'][0]['segments'][0]['departure']['iataCode']
        row['departureDate'] = " ".join(item['itineraries'][0]['segments'][0]['departure']['at'].split("T"))
        row['dest_iata'] = item['itineraries'][0]['segments'][-1]['arrival']['iataCode']
        row['returnDate'] = " ".join(item['itineraries'][1]['segments'][0]['departure']['at'].split("T"))
        row['returnNumOfTransfers'] = len(item['itineraries'][1]['segments'])
        row['currency'] = item['price']['currency']
        row['total'] = item['price']['total']
        row['lastTicketingDate'] = item['lastTicketingDate']
        row['numOfAdults'] = numOfAdults
        data.append(row)
        
    tmp = [json.dumps(x) for x in data]
    tmp2 = list(set(tmp))
    tmp2 = [json.loads(x) for x in tmp2]
    return status_code, {'amadeus_data': tmp2}
