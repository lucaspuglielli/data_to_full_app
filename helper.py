from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
from ipeadatapy import *
import requests as req
import pandas as pd
import getpass
import bcrypt
import os


### TERRITORIO E POPULACAO RURAL

dict_territorio = {
    "territorio":{
        "populacao_rural":'POPRU'
    }
}

### AGROPECUARIA

serie_agro = {
    "agro_valores_totais":{
        "lavoura_total(ha)":'AREAPLATOT',
        "lavoura_temporaria(ha)":'AREAPLATEMP',
        "lavoura_permanente(ha)":'AREAPLAPERM',
        "colheita_total(ha)":'AREACOLTOT',
        "colheita_temporaria(ha)":'AREACOLTEMP',
        "colheita_permanente(ha)":'AREACOLPERM',
        "producao_total":'VALPRODTOT',
        "producao_temporaria":'VALPRODTEMP',
        "producao_permanente":'VALPRODPERM',
    },
    "algodao_herbaceo_caroco":{"area(ha)":'AREACOLALGHER',"quantidade":'QUANTPRODALGHER',"valor":'VALPRODALGHER',},
    "amendoim":{"area(ha)":'AREACOLAMENDOIM',"quantidade":'QUANTPRODAMENDOIM',"valor":'VALPRODAMENDOIM',},
    "arroz":{"area(ha)":'AREACOLARROZ',"quantidade":'QUANTPRODARROZ',"valor":'VALPRODARROZ',},
    "banana":{"area(ha)":'AREACOLBANANA',"quantidade":'QUANTPRODBANANA',"valor":'VALPRODBANANA',},
    "batata_inglesa":{"area(ha)":'AREACOLBATATA',"quantidade":'QUANTPRODBATATA',"valor":'VALPRODBATATA',},
    "cacau":{"area(ha)":'AREACOLCACAU',"quantidade":'QUANTPRODCACAU',"valor":'VALPRODCACAU',},
    "cafe":{"area(ha)":'AREACOLCAFE',"quantidade":'QUANTPRODCAFE',"valor":'VALPRODCAFE',},
    "cana_de_acucar":{"area(ha)":'AREACOLCANA',"quantidade":'QUANTPRODCANA',"valor":'VALPRODCANA',},
    "cebola":{"area(ha)":'AREACOLCEBOLA',"quantidade":'QUANTPRODCEBOLA',"valor":'VALPRODCEBOLA',},
    "feijao":{"area(ha)":'AREACOLFEIJAO',"quantidade":'QUANTPRODFEIJAO',"valor":'VALPRODFEIJAO',},
    "fumo":{"area(ha)":'AREACOLFUMO',"quantidade":'QUANTPRODFUMO',"valor":'VALPRODFUMO',},
    "laranja":{"area(ha)":'AREACOLLARANJA',"quantidade":'QUANTPRODLARANJA',"valor":'VALPRODLARANJA',},
    "mandioca":{"area(ha)":'AREACOLMANDIOCA',"quantidade":'QUANTPRODMANDIOCA',"valor":'VALPRODMANDIOCA',},
    "milho":{"area(ha)":'AREACOLMILHO',"quantidade":'QUANTPRODMILHO',"valor":'VALPRODMILHO',},
    "pimenta_do_reino":{"area(ha)":'AREACOLPIMENTA',"quantidade":'QUANTPRODPIMENTA',"valor":'VALPRODPIMENTA',},
    "soja":{"area(ha)":'AREACOLSOJA',"quantidade":'QUANTPRODSOJA',"valor":'VALPRODSOJA',},
    "tomate":{"area(ha)":'AREACOLTOMATE',"quantidade":'QUANTPRODTOMATE',"valor":'VALPRODTOMATE',},
    "trigo":{"area(ha)":'AREACOLTRIGO',"quantidade":'QUANTPRODTRIGO',"valor":'VALPRODTRIGO',},
    "uva":{"area(ha)":'AREACOLUVA',"quantidade":'QUANTPRODUVA',"valor":'VALPRODUVA',},
}

serie_pecuaria = {
    "pecuaria_criacao":{
        "bovinos":'QUANTBOVINOS',
        "vacas_ordenhadas":'QUANTVACASORD',
        "bubalinos":'QUANTBUBALINOS',
        "caprinos":'QUANTCAPRINOS',
        "equinos":'QUANTEQUINOS',
        "galinaceos":'QUANTGALINACEOS',
        "ovinos":'QUANTOVINOS',
        "ovinos_tosquiados":'QUANTOVINOSTOSQ',
        "suinos":'QUANTSUINOS',
    },
    "casulo_de_bicho_da_seda":{"quantidade":'QUANTCASULOBS',"valor":'VALORCASULOBS',},
    "la":{"quantidade":'QUANTLA',"valor":'VALORLA',},
    "leite":{"quantidade":'QUANTLEITE',"valor":'VALORLEITE',},
    "mel_de_abelha":{"quantidade":'QUANTMEL',"valor":'VALORMEL',},
    "ovos_de_codorna":{"quantidade":'QUANTOVOCODORNA',"valor":'VALOROVOCODORNA',},
    "ovos_de_galinha":{"quantidade":'QUANTOVOGALINHA',"valor":'VALOROVOGALINHA',},
}

### CREDITO RURAL

serie_credito = {
    "credito_rural_geral":{
        "estoque_de_credito_rural":'CREAT',
        "fluxo_de_credito_rural":'CREATE',
        "total_de_contratos_de_credito_rural":'NCREAT',
    },
    "credito_rural_comercializacao":{
        "estoque_de_credito_rural":'COMERC',
        "estoque_de_credito_rural_agricola":'COMAGR',
        "estoque_de_credito_rural_pecuaria":'COMPEC',
        "fluxo_de_credito_rural":'COMERCE',
        "fluxo_de_credito_rural_agricola":'COMAGRE',
        "fluxo_de_credito_rural_pecuaria":'COMPECE',
        "total_de_contratos_de_credito_rural":'NCOMER',
        "total_de_contratos_de_credito_rural_agricola":'NCOMAG',
        "total_de_contratos_de_credito_rural_pecuaria":'NCOMPC',
    },
    "credito_rural_custeio":{
        "estoque_de_credito_rural":'CUSGIO',
        "estoque_de_credito_rural_agricola":'CUSAGR',
        "estoque_de_credito_rural_pecuaria":'CUSPEC',
        "fluxo_de_credito_rural":'CUSGIOE',
        "fluxo_de_credito_rural_agricola":'CUSAGRE',
        "fluxo_de_credito_rural_pecuaria":'CUSPECE',
        "total_de_contratos_de_credito_rural":'NCUSGI',
        "total_de_contratos_de_credito_rural_agricola":'NCUSAG',
        "total_de_contratos_de_credito_rural_pecuaria":'NCUSPC',
    },
    "credito_rural_investimento":{
        "estoque_de_credito_rural":'INVEST',
        "estoque_de_credito_rural_agricola":'INVAGR',
        "estoque_de_credito_rural_pecuaria":'INVPEC',
        "fluxo_de_credito_rural":'INVESTE',
        "fluxo_de_credito_rural_agricola":'INVAGRE',
        "fluxo_de_credito_rural_pecuaria":'INVPECE',
        "total_de_contratos_de_credito_rural":'NINVES',
        "total_de_contratos_de_credito_rural_agricola":'NINVAG',
        "total_de_contratos_de_credito_rural_pecuaria":'NINVPC'
    },
}

# Send a request to the API, select the response value, 
# and return it as a pandas DataFrame.
# def api_request(url):
#     time1 = datetime.today()
#     print("Sending the request to the API")
#     response = req.get(url)
#     if response.status_code == req.codes.ok:
#         json_response = response.json()
#         if 'value' in json_response:
#             time2 = datetime.today()
#             print(f"Response received in {time2 - time1}")
#             try:
#                 data_frame = pd.DataFrame(json_response['value'])
#                 return data_frame
#             except Exception:
#                 return None
#     time2 = datetime.today()
#     print(f"Request failed in {time2 - time1}")
#     return None


# Create the engine needed for database connection
def get_engine(): 
    load_dotenv()
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_name = os.getenv('POSTGRES_DB')
    database_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/{db_name}'
    return create_engine(database_url)


# Search for the table components in the dictionaries.
def find_value_in_dicts(key): 
    dicts = [dict_territorio, serie_agro, serie_pecuaria, serie_credito] 
    for dictionary in dicts: 
        for sub_key, sub_value in dictionary.items(): 
            if isinstance(sub_value, dict): 
                if key in sub_value: 
                    return sub_value[key] 
                else: 
                    if key == sub_key: 
                        return sub_value 
    return "Key not found in any dictionary"


# Iterate through the received dictionary to pull all the components needed from the API, 
# and merge them into a single table using the full list of territories as a base.
def mount_table(dict_of_files):
    dataframes = {}
    for key, value in dict_of_files.items():
        time1 = datetime.today()
        print(f"Pulling data from {value}")
        df_api = timeseries(value)
        df_api.rename(columns={df_api.columns[-1]: key.upper()}, inplace=True)
        dataframes[key] = df_api[['TERCODIGO', 'YEAR', df_api.columns[-1]]]
        time2 = datetime.today()
        print(f"Info received in {time2 - time1}")
    merged_df = None
    time1 = datetime.today()
    print("Merging tables")
    for key, df in dataframes.items():
        try:
            if merged_df is None:
                if key=='populacao_rural':
                    merged_df = territories()
                    merged_df.rename(columns={'AREA': 'AREA(M2)'}, inplace=True)
                    merged_df = merged_df[merged_df['NAME'] != '(não definido)']
                else:
                    merged_df = territories()[['NAME', 'ID', 'LEVEL']]
                    merged_df = merged_df[merged_df['NAME'] != '(não definido)']
                merged_df.rename(columns={'ID': 'TERCODIGO'}, inplace=True)
                merged_df = merged_df.merge(df, on=['TERCODIGO'], how='left')
                merged_df = merged_df.drop_duplicates()
            else:
                merged_df = merged_df.merge(df, on=['TERCODIGO', 'YEAR'], how='left')
                merged_df = merged_df.drop_duplicates()
        except Exception as e:
            print(e)
    merged_df = merged_df.fillna(0)
    merged_df = standardize_data(merged_df)
    time2 = datetime.today()
    print(f"Tables merged in {time2 - time1}")
    return merged_df


# Convert columns to their correct data types
def standardize_data(df):
    type_mappings = {
        'NAME': str,
        'TERCODIGO': str,
        'LEVEL': str,
        'YEAR': int,
        'AREA(M2)': float,
        'POPULACAO_RURAL': int,
        'AREA(HA)': float,
        'LAVOURA_TOTAL(HA)': float,
        'LAVOURA_TEMPORARIA(HA)': float,
        'LAVOURA_PERMANENTE(HA)': float,
        'COLHEITA_TOTAL(HA)': float,
        'COLHEITA_TEMPORARIA(HA)': float,
        'COLHEITA_PERMANENTE(HA)': float,
        'QUANTIDADE': float,
        'VALOR': float,
        'BOVINOS': int,
        'VACAS_ORDENHADAS': int,
        'BUBALINOS': int,
        'CAPRINOS': int,
        'EQUINOS': int,
        'GALINACEOS': int,
        'OVINOS': int,
        'OVINOS_TOSQUIADOS': int,
        'SUINOS': int,
        'PRODUCAO_TOTAL': float,
        'PRODUCAO_TEMPORARIA': float,
        'PRODUCAO_PERMANENTE': float,
        'ESTOQUE_DE_CREDITO_RURAL': float,
        'ESTOQUE_DE_CREDITO_RURAL_AGRICOLA': float,
        'ESTOQUE_DE_CREDITO_RURAL_PECUARIA': float,
        'FLUXO_DE_CREDITO_RURAL': float,
        'FLUXO_DE_CREDITO_RURAL_AGRICOLA': float,
        'FLUXO_DE_CREDITO_RURAL_PECUARIA': float,
        'TOTAL_DE_CONTRATOS_DE_CREDITO_RURAL': int,
        'TOTAL_DE_CONTRATOS_DE_CREDITO_RURAL_AGRICOLA': int,
        'TOTAL_DE_CONTRATOS_DE_CREDITO_RURAL_PECUARIA': int,
    }
    for column, dtype in type_mappings.items():
        if column in df.columns:
            df[column] = df[column].astype(dtype)
            # area_list = ['AREA(M2)', 
            #              'AREA(HA)', 
            #              'LAVOURA_TOTAL(HA)', 
            #              'LAVOURA_TEMPORARIA(HA)',
            #              'LAVOURA_PERMANENTE(HA)', 
            #              'COLHEITA_TOTAL(HA)', 
            #              'COLHEITA_TEMPORARIA(HA)', 
            #              'COLHEITA_PERMANENTE(HA)']
            area_list = []
            if dtype == float and column not in area_list:
                df[column] = df[column].round(2)
    return df



# Try to get the table from the database. If it doesn't exist,
# pull all the related data from the source, clean it,
# create a table for it, then return the DataFrame.
def get_data(table, year=None):
    engine = get_engine()
    start_time = datetime.today()
    try:
        time1 = datetime.today()
        print(f"Loading table: {table}")
        if year!=None:
            query = f'SELECT * FROM {table} WHERE "YEAR"={year}'
        else:
            query = f"SELECT * FROM {table}" 
        df =  pd.read_sql(query, engine)
        time2 = datetime.today()
        print(f"Loaded in {time2 - time1}")
        print(f"Finished in {time2 - start_time}")
        return df
    except:
        print(f"Table {table} could not be loaded")
        df = mount_table(find_value_in_dicts(table))
        time1 = datetime.today()
        print(f"Saving table: {table}")
        df.to_sql(f'{table}', engine, if_exists='replace', index=False)
        print(f"{table} saved!")
        time2 = datetime.today()
        print(f"Table saved {df.shape[0]} rows in {time2 - time1}")
        print(f"Finished in {time2 - start_time}")
        if year!=None:
            df[df['YEAR']==year]
        return df


# Encrypts data
def anonymize_data(data):
    salt = bcrypt.gensalt()
    hashed_data = bcrypt.hashpw(data.encode('utf-8'), salt)
    return hashed_data


# Verify encrypted data
def verify_encryption(input_data, hashed_data):
    return bcrypt.checkpw(input_data.encode('utf-8'), hashed_data)





#
# def user_auth():
#     try:
#         engine = get_engine()
#         try:
#             user_password = user_password
#         except:
#             query = f'SELECT * FROM users WHERE "USERNAME"="{user_username}"'
#             df = pd.read_sql(query, engine)
#             user_password = df['PASSWORD']
#         if verify_data(user_password, user_password):
#     except:
#         print("User not logged in")
#         sign_up = input("Do you want to sign up (y/n): ").lower().strip() == 'y'
#         if sign_up:
#             user_username = input("Please enter your username: ")
#             user_password = anonymize_data(getpass.getpass("Please enter your password: "))
#         else:
#             pass


    
    #colocar verificacao no inicio de cada funcao para ver se usuario esta logado, na funcao de input, perguntar ao usuario se deseja fazer login ou cadastrar, adicionar um hash encriptado para servir de "convite" antes de liberar cadastro, salvar uma tabela com usuario e senha hasheada entre o input e o armazenamento em variavel




    
