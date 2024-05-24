import json
import re
import os
import argparse
import datetime
import pathlib
import shutil

from ocr import main_no_args
from data_handling.sort_beneficiaries import passenger_been_sent
import requests

TOKEN_RE = re.compile(r'access_token=([\.\-\w]+)')
ISO_RE = re.compile(r'(\d{2})/(\d{2})/(\d{4})')
INPUT_URL = "https://api.acces-maroc.ma:443/api/api/demandeEvisa/dossierDemandeEVisa"
PATH = "C:\\Users\\Tal Meshali\\Desktop\\Discovery Winter"

FIELDS = {
    "birth_date": "",
    "last_name": "",
    "first_name": "",
    "birth_place": "",
    "passport_number": "",
    "issue_date": "",
    "expiry_date": "",
    "arrival_date": "",
    "departure_date": "",
    "profession": ""
}


def get_header(token):
    return {"Authorization": token}


def login(code):
    login_url = "https://api.acces-maroc.ma:443/access/api/login"
    login_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36",
    }

    login_details = {"dossier": code, "email": "moredite1@gmail.com"}
    res = requests.post(login_url, headers=login_agent, json=login_details)
    print("LOGIN:", res.status_code)
    return "Bearer " + re.findall(TOKEN_RE, res.text)[0]


def create_beneficiary(isr_code, trip, token):
    post_beneficiary_url = "https://api.acces-maroc.ma:443/api/api/conditionEvise/recherche/en"
    with open("../../../templates/beneficiary_initial_request.json", "r") as f:
        beneficiary = json.load(f)
    beneficiary["dateNaissance"] = convert_date_to_iso(FIELDS["birth_date"])
    res = requests.post(post_beneficiary_url, headers=get_header(token), json=beneficiary)
    print("POST: ", res.status_code)
    current_evisa = get_demande_evisa(token)
    if not current_evisa["refsDemandeVisa"]:
        put_res = put_info_request(current_evisa, token)
        isr_code = put_res["numDossier"]
        token = login(isr_code)
    else:
        put_res = put_info_request(current_evisa, token)
    post_documents(put_res, token, trip)
    return isr_code, token


def get_demande_evisa(token):
    header = get_header(token)
    get_dossier_url = "https://api.acces-maroc.ma:443/api/api/demandeEvisa/dossierEVisa"
    res = requests.get(get_dossier_url, headers=header)
    print("GET:", res.status_code)
    return res.json()


def convert_date_to_iso(date):
    # date comes at a format of DD/MM/YYYY
    return str(datetime.datetime.strptime(date, "%d/%m/%Y").isoformat()) + ".000Z"


def put_info_request(full_req, token):
    header = get_header(token)
    with open("../../../templates/beneficiary_update_details.json") as f:
        f = json.load(f)
        req = f["PUT"]["CONSTANT"]
        variable_params = f["PUT"]["VARIABLES"]
        for var_param, translated_field in variable_params.items():
            if "ISO" in translated_field:
                var_for_req = convert_date_to_iso(FIELDS[translated_field.split("/")[0]])
            else:
                var_for_req = FIELDS[translated_field]
            if "/" in var_param:
                field_loc = var_param.split("/")
                req[field_loc[0]][field_loc[1]] = var_for_req
            else:
                req[var_param] = var_for_req
    full_req["refsDemandeVisa"].append(req)

    res = requests.put(INPUT_URL, headers=header, json=full_req)
    print("PUT:", res.status_code)
    return res.json()


def get_path_to_document(passenger, trip, get_json=False):
    result = {}
    path = f'C:\\Users\\Tal Meshali\\Desktop\\Discovery Winter\\{trip}\\READY FOR VISA\\{passenger}'
    for item in os.listdir(path):
        if get_json:
            if "json" in item:
                return os.path.join(path, item)
        if "PHOTO" in item:
            result["Photo"] = os.path.join(path, item)
        if "PASSPORT" in item and "json" not in item:
            result["Passport"] = os.path.join(path, item)
    return result


def upload_document(path, token, change_field):
    with open('../../../templates/blob.json', 'r') as f:
        blob = json.load(f)
    for field in change_field.keys():
        if "/" in field:
            fields = field.split("/")
            blob[fields[0]][fields[1]] = change_field[field]
        else:
            blob[field] = change_field[field]

    upload_url = "https://api.acces-maroc.ma:443/api/api/v1"
    photo_name = path.split("\\")[-1]
    doc_type = path.split(".")[-1]
    photo = pathlib.Path(path).read_bytes()
    res = requests.post(upload_url, headers=get_header(token), files={
        'attachment': ('blob', json.dumps(blob).encode(), 'application/json'),
        'file': (photo_name, photo, 'application/pdf' if doc_type == 'pdf' else 'image/jpeg')
    })
    print(f"DOC_POST:", res.status_code)
    print(res.content)


def get_profession():
    d1 = datetime.datetime.today()
    d2 = datetime.datetime.strptime(FIELDS["birth_date"], '%d/%m/%Y')
    underage = True if (d1 - d2).days / 365 < 18 else False
    return {
        "id": 123 if underage else 55,
        "code": "PR31" if underage else "PR14",
        "libelle": "WITHOUT" if underage else "EMPLOYEE",
        "lang": "en",
        "statut": "Active",
        "active": True,
    }


def post_documents(full_req, token, trip, name=''):
    beneficiary_name, beneficiary_id = '', ''
    if name:
        for req in full_req["refsDemandeVisa"]:
            beneficiary_name = req["refInfoBeneficiairesVisa"]["nom"] + " " + req["refInfoBeneficiairesVisa"]["prenom"]
            if name == beneficiary_name:
                beneficiary_id = req["id"]
                break
        if not beneficiary_id:
            print(f"Beneficiary {name} wasn't found in request.")
            return
    else:
        req = full_req["refsDemandeVisa"][-1]
        beneficiary_id = req["id"]
        beneficiary_name = req["refInfoBeneficiairesVisa"]["nom"] + " " + req["refInfoBeneficiairesVisa"]["prenom"]
    documents = get_path_to_document(beneficiary_name, trip)

    for category, path in sorted(documents.items(), reverse=True):
        change_field = {
            "category/codeCategory": "295" if category == "Photo" else "296",
            "category/code": "PHT" if category == "Photo" else "PSP",
            "description": path.split('\\')[-1],
            "attachableId": beneficiary_id
        }
        upload_document(path, token, change_field)
    data = {"attachableId": beneficiary_id}
    save = requests.put(url="https://api.acces-maroc.ma/api/api/v1/checkRequiredAttEvisa/en", headers=get_header(token),
                        json=data)
    print("SAVE:", save.status_code)


def fix_beneficiary(isr_code, trip, name):
    token = login(isr_code)
    res = get_demande_evisa(token)
    post_documents(res, token, trip, name)


def download_visas(code):
    token = login(code)
    dossier_info = get_demande_evisa(token)["refsDemandeVisa"]

    visa_id_list = [item["id"] for item in dossier_info]
    visa_name_list = [
        item["refInfoBeneficiairesVisa"]["nom"] + " " + item["refInfoBeneficiairesVisa"]["prenom"] for
        item in dossier_info]
    payload = {}
    headers = get_header(token)

    visas_already_downloaded = set()
    for trip in os.listdir(PATH):
        current = os.path.join(PATH, trip)
        if not os.path.isdir(current) or trip == "Visas Only":
            continue
        if "VISAS" not in os.listdir(current):
            continue
        for code in os.listdir(current):
            if not os.path.isdir(os.path.join(current, code)):
                continue
            for passenger in os.listdir(os.path.join(current, code)):
                if passenger in os.listdir(os.path.join(current, "VISAS")):
                    visas_already_downloaded.add(passenger)

    for i in range(len(visa_id_list)):
        if visa_name_list[i] in visas_already_downloaded:
            continue
        try:
            visa_url = f"https://api.acces-maroc.ma:443/api/api/demandeEvisa/genererDemandeEvisaImp/{visa_id_list[i]}"
            res = requests.get(visa_url, headers=headers, data=payload)
            if res.status_code == 409:
                print(f"{visa_name_list[i]}: Failed, needs addressing")
                continue
            if res.status_code != 200:
                print("Unexpected error:", res.status_code, res.content)
                return
            print(f"{visa_name_list[i]}: Successful")
            with open(f"C:\\Users\\Tal Meshali\\Downloads\\{visa_name_list[i]} VISA.pdf", "wb") as f:
                f.write(res.content)
        except Exception:
            print(f"Finished for batch {code}")
            return


def get_arrival_departure_dates(date_org):
    day, month = date_org.split('-')[0].split(".")
    date_arrival = datetime.date.today().replace(day=int(day), month=int(month))
    date_departure = date_arrival + datetime.timedelta(days=14)
    FIELDS[
        "arrival_date"] = f"{str(date_arrival.day).zfill(2)}/{str(date_arrival.month).zfill(2)}/{date_arrival.year}"
    FIELDS[
        "departure_date"] = f"{str(date_departure.day).zfill(2)}/{str(date_departure.month).zfill(2)}/{date_departure.year}"


def parse_args():
    """
    Parse command line arguments
    WARNING: This function will exit the program if arguments are invalid
    :return: dictionary of arguments
    """
    parser = argparse.ArgumentParser(description='Sort to Beneficiaries')
    parser.add_argument(
        '-t', '--trip',
        type=str,
        required=False,
        help='date of the specified trip')
    parser.add_argument(
        '-v', '--visa',
        action='store_true',
        required=False,
        help='download prepared visas from given codes')
    parser.add_argument(
        '-o', '--ocr',
        action='store_true',
        required=False,
        help='run the ocr scan for each passenger in given trip')
    parser.add_argument(
        '-c', '--code',
        type=str,
        required=False,
        help='temporary code of a new request, format of XXXXXX')
    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    if args['visa']:
        for code in args['code'].split(" "):
            download_visas(code)
    elif args['ocr']:
        if args['trip'] == 'all':
            trips = filter(lambda x: re.match(r'\d{1,2}\.\d{1,2}', x), os.listdir(PATH))
        else:
            trips = args['trip'].split(' ')
        for TRIP in trips:
            if "READY FOR VISA" not in os.listdir(os.path.join(PATH, TRIP)):
                continue
            path = os.path.join(PATH, TRIP, "READY FOR VISA")
            for passenger in os.listdir(path):
                if not passenger + " PASSPORT.json" in os.listdir(os.path.join(path, passenger)):
                    try:
                        main_no_args(TRIP, passenger)
                    except ValueError as e:
                        print(f"Failed to parse {passenger} due to a value error {e}")
                        shutil.copytree(os.path.join(path, passenger), os.path.join(PATH, TRIP, passenger),
                                        dirs_exist_ok=True)
                        shutil.rmtree(os.path.join(path, passenger))
    else:
        if args['trip'] == 'all':
            trips = filter(lambda x: re.match(r'\d{1,2}\.\d{1,2}', x), os.listdir(PATH))
        else:
            trips = args['trip'].split(' ')
        for TRIP in trips:
            TRIP = TRIP.replace('\'', '')
            ISR = args['code']
            if "READY FOR VISA" not in os.listdir(os.path.join(PATH, TRIP)):
                continue
            path = os.path.join(PATH, TRIP, "READY FOR VISA")
            token = login(ISR)
            get_arrival_departure_dates(TRIP)
            for passenger in os.listdir(path):
                path_to_json = get_path_to_document(passenger, TRIP, get_json=True)
                with open(path_to_json, 'r') as f:
                    f = json.load(f)
                    for key, value in f.items():
                        FIELDS[key] = value
                FIELDS["profession"] = get_profession()
                ISR, token = create_beneficiary(ISR, TRIP, token)
                passenger_been_sent(TRIP, ISR, passenger)
                print("\n")
            if len(os.listdir(path)) == 0:
                os.rmdir(path)
