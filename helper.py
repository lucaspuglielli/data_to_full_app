from cryptography.fernet import Fernet
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime
from ipeadatapy import *
import requests as req
import pandas as pd
import getpass
import redis
import os


### TERRITORY AND RURAL POPULATION

dict_territorio = {
    "territorio":{
        "populacao_rural":'POPRU'
    }
}


### AGRICULTURE AND LIVESTOCK

serie_agricultura = {
    "agricultura_valores_totais":{
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


### RURAL FINANCING

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
    postgres_user = os.getenv('POSTGRES_USER')
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    postgres_host = os.getenv('POSTGRES_HOST')
    postgres_port = os.getenv('POSTGRES_PORT')
    postgres_db = os.getenv('POSTGRES_DB')
    database_url = f'postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}'
    return create_engine(database_url)


# Create the redis connection
def get_redis():
    load_dotenv()
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')
    redis_db = os.getenv('REDIS_DB')
    return redis.Redis(host=redis_host, port=redis_port, db=redis_db)


# Runs user authentication
def user_auth():
    r = get_redis()
    try:
        datamaster_user_username = r.get('datamaster_user_username').decode('utf-8')
        datamaster_user_password = r.get('datamaster_user_password').decode('utf-8')
    except:
        datamaster_user_username = ""
        datamaster_user_password = ""
    load_dotenv()
    fernet_key = os.getenv('FERNET_KEY')
    cipher_suite = Fernet(fernet_key)
    invitation_hash = os.getenv('SIGN_UP_PASSWORD')
    postgres_user = os.getenv('POSTGRES_USER')
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    postgres_host = os.getenv('POSTGRES_HOST')
    postgres_port = os.getenv('POSTGRES_PORT')
    postgres_auth_db = os.getenv('POSTGRES_AUTH_DB')
    auth_database_url = f'postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_auth_db}'
    auth_engine = create_engine(auth_database_url)

    def user_registry():
        sign_up_input = input("Do you want to sign up (y/n): ")
        sign_up = sign_up_input.lower().strip() == "y"
        if sign_up and (input("Please enter your invitation: ") == invitation_hash):
            datamaster_user_username = input("Please enter your username: ")
            datamaster_user_password = input("Please enter your password: ")
            # datamaster_user_password = getpass.getpass("Please enter your password: ")
            hashed_datamaster_user_password = cipher_suite.encrypt(datamaster_user_password.encode()).decode()
            df = pd.DataFrame({'USERNAME': [datamaster_user_username], 'PASSWORD': [hashed_datamaster_user_password]})
            try:
                query = 'SELECT * FROM users WHERE "USERNAME"=%s'
                existing_users = pd.read_sql(query, auth_engine, params=(datamaster_user_username,))
                if not existing_users.empty:
                    print("Username already taken")
                    datamaster_user_username = ""
                    datamaster_user_password = ""
                    r.set('datamaster_user_username', datamaster_user_username)
                    r.set('datamaster_user_password', datamaster_user_password)
                    return False
                else:
                    df.to_sql('users', auth_engine, if_exists='append', index=False)
                    r.set('datamaster_user_username', datamaster_user_username)
                    r.set('datamaster_user_password', datamaster_user_password)
                    return True
            except:
                df.to_sql('users', auth_engine, if_exists='append', index=False)
                r.set('datamaster_user_username', datamaster_user_username)
                r.set('datamaster_user_password', datamaster_user_password)
                return True

    query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
    tables_df = pd.read_sql(query, auth_engine)
    table_list = tables_df['table_name'].tolist()
    try:
        if ("users" in table_list):
            if datamaster_user_username != '':
                query = 'SELECT * FROM users WHERE "USERNAME"=%s'
                df = pd.read_sql(query, auth_engine, params=(datamaster_user_username,))
                dehashed_datamaster_user_password = cipher_suite.decrypt((df['PASSWORD'][0]).encode()).decode()
                if datamaster_user_password != '' and df.shape[0] != 0 and (datamaster_user_password == dehashed_datamaster_user_password):
                    return True
                else:
                    return user_registry()
            else:
                datamaster_user_username = input("Please enter your username: ")
                datamaster_user_password = input("Please enter your password: ")
                # datamaster_user_password = getpass.getpass("Please enter your password: ")
                query = 'SELECT * FROM users WHERE "USERNAME"=%s'
                df = pd.read_sql(query, auth_engine, params=(datamaster_user_username,))
                if df.shape[0] != 0 and (datamaster_user_password == cipher_suite.decrypt((df['PASSWORD'][0]).encode()).decode()):
                    r.set('datamaster_user_username', datamaster_user_username)
                    r.set('datamaster_user_password', datamaster_user_password)
                    return True
                else:
                    return user_registry()
        else:
            return user_registry()
    except:
        datamaster_user_username = ""
        datamaster_user_password = ""
        r.set('datamaster_user_username', datamaster_user_username)
        r.set('datamaster_user_password', datamaster_user_password)
        return user_registry()





# Search for the table components in the dictionaries.
def find_value_in_dicts(key): 
    dicts = [dict_territorio, serie_agricultura, serie_pecuaria, serie_credito] 
    for dictionary in dicts: 
        for sub_key, sub_value in dictionary.items(): 
            if isinstance(sub_value, dict): 
                if key in sub_value: 
                    return sub_value[key] 
                else: 
                    if key == sub_key: 
                        return sub_value 
    return "Key not found in any dictionary"


# Verify if key is valid.
def verify_key_in_dicts(key): 
    dicts = [dict_territorio, serie_agricultura, serie_pecuaria, serie_credito] 
    for dictionary in dicts: 
        for sub_key, sub_value in dictionary.items(): 
            if isinstance(sub_value, dict): 
                if key in sub_value: 
                    return True 
                else: 
                    if key == sub_key: 
                        return True 
    return False


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
                    merged_df.rename(columns={'AREA': 'AREA(KM2)'}, inplace=True)
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
        except:
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
        'AREA(KM2)': float,
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
            # area_list = ['AREA(KM2)', 
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
    if user_auth():
        check_table = verify_key_in_dicts(table)
        check_year = (year==None or isinstance(year, int))
        if check_table and check_year:
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
                    df = df[df['YEAR']==year]
                return df
        else:
            if not check_table:
                print("Invalid table name")
            if not check_year:
                print("Invalid year (must be a number)")
    else:
        print("User not logged-in")


# Try to get the table from the database.
def save_table(df, name):
    if user_auth():
        try:
            if not verify_key_in_dicts(name):
                engine = get_engine()
                print(f"Saving table: {name}")
                df.to_sql(f'{name}', engine, if_exists='replace', index=False)
            else:
                print("Table name reserved for API tables")
        except Exception as e:
            raise e
    else:
        print("User not logged-in")


# Try to save the dataframe into the database.
def load_table(name):
    if user_auth():
        try:
            engine = get_engine()
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            tables_db = pd.read_sql(query, engine)
            available_tables = tables_db["table_name"].tolist()
            if name in available_tables:
                print(f"Loading table: {name}")
                query = f"SELECT * FROM {name}" 
                return pd.read_sql(query, engine)
            else:
                print("Table not available in the database")
        except Exception as e:
            raise e
    else:
        print("User not logged-in")


# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# Try to delete a table from the database.
def delete_table(name):
    if user_auth():
        try:
            engine = get_engine()
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            tables_db = pd.read_sql(query, engine)
            available_tables = tables_db["table_name"].tolist()
            if name in available_tables:
                print(f"Deleting table: {name}")
                with engine.connect() as connection:
                    with connection.begin():
                        connection.execute(text(f'DROP TABLE IF EXISTS "{name}"'))
                        print("Table deleted")
            else:
                print("Table not available in the database")
        except Exception as e:
            raise e
    else:
        print("User not logged-in")


