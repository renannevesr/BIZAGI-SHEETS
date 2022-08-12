from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from flask import Flask, jsonify, request, abort
app = Flask(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1DeJNqwsZFpjLDwDPWPEAlgP5aLgyU9P29plHnL0b4ZQ'
SAMPLE_RANGE_NAME = 'Macohin!A1:B200'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    return service
@app.route('/', methods=['POST'])
def home():
    content = request.json
    service = main()
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    tamanho = len(values)+1

    # adicionar/editar valores no Google Sheets

    nome = content['name']
    email = content ['email']
    rua = content['street']
    cep = content['cep']
    bairro = content['district']
    cidade = content ['city']
    estado = content ['state']
    nacionality = content ['nacionality']
    maritalStatus = content['maritalStatus']
    nascimento = content ['birthDate']
    profession = content ['profession']
    cpf = content ['cpf']
    rg = content['rg']
    telefone = content['cellphone']
    gov = content ['email']
    valores_adicionar =[[f"{nome}",f"{telefone}",f"{nascimento}",f"{cpf}",f"{rg}",f"{gov}",f"{rua}",f"{bairro}",f"{cidade}",f"{cep}",f"{maritalStatus}"]]
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=f'Macohin!A{tamanho}', valueInputOption="RAW",
                                   body={"values": valores_adicionar}).execute()
    return content 

if __name__ == '__main__':
    app.run( port=7001)
