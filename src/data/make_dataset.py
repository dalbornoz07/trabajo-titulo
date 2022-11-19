"""
Author: Diego Albornoz
Versión: 1.5
Updated: 08-11-2022
Created: 01-11-2022
"""

import pandas as pd
import numpy as np
import os
import sys
from typing import List
from multiprocessing import Process, Lock

#from selenium import webdriver
#from selenium.webdriver.common.by import by

#driver = webdriver.Firefox()


#Global variables
HOME = '/'.join(os.getcwd().split('/')[:-2])
RAW= os.path.join(HOME,'data/raw')
PROCESSED = os.path.join(HOME,'data/processed')
INTERIM = os.path.join(HOME,'data/interim')

CAMPUS = {0:"CC",1:"CSSJ",2:"Vitacura"}

def get_files_list(condition:str='')->List[str]:
    """
    Descripción: Obtiene el listado de archivos dentro de la carpeta data/raw
    Parametros: condition (str) formato que deben tener los archivos a BUSCAR
    Retorno: Listado con los nombres de cada archivo que se encuentra en el directorio data/raw
    """
    return [ os.path.join(root,name) for root,_,filename in os.walk(os.path.join(RAW,condition),topdown=True)  for name in filename ]


def aux_gen_list_cols(text:str='',start:int=1,end:int=12)->List[str]:
    return [text.format(i) for i in range(start,end)]


def create_campus_csv(archivo:str,anno:int,semestre:int)->None:
    """
    Descripción:  Genera archivos csv con los datos de los estudiantes para que luego sean transformados y procesados
    Parámetros: - archivo(str) nombre del archivo en excel que se va trabajar
                - anno (int) año trabajado
                - semestre (int) semestre trabajado (1 o 2)
    Retorno: - 
    """
    df_template= pd.DataFrame({"RUT":[],"DV.1":[],"Nombre":[],"VTR":[],"C1":[],"C2":[],"CR":[],
                            'S1':[],'S2':[],'S3':[],'S4':[],'S5':[],'S6':[],'S7':[],'S8':[],'S9':[],'S10':[],
                            'F1':[],'F2':[],'F3':[],'F4':[],'F5':[],'F6':[],'F7':[],'F8':[],'F9':[],'F10':[],
                            'T1':[],'T2':[],'T3':[],'T4':[],'T5':[],'T6':[],'T7':[],'T8':[],'T9':[],'T10':[],
                            'SM1':[],'SM2':[],'SM3':[],'SM4':[],'SM5':[],'SM6':[],'SM7':[],'SM8':[],"NF":[],
                            "Carrera_origen":[],"Carrera":[],'Campus':[],"Sexo":[],'Sem':[],'Anno':[]})
    df_template['Carrera'] = pd.Series(df_template['Carrera'], dtype='string')

    id_campus = [key for key,val in CAMPUS.items() if val in archivo][0]
    
    assert archivo.endswith('.xlsx'), "Error en extensión de archivo, solo se acepta xlsx"
    df_base = pd.read_excel(pd.ExcelFile(archivo),None,na_filter=False,skiprows=3,header=0)
    for sheet in list(df_base.keys()):
        if sheet in ['Estadísticas','SUMATORIAS','Cuestionario']:
            continue
      
        sheet_data = df_base[sheet]
        sheet_data.replace(['','-','#¡DIV/0!'],np.nan,inplace=True)
        sheet_data.dropna(subset=['RUT'],inplace=True,axis=0)

        _columns = ['RUT','DV.1','Nombre','VTR','C1','C2','CR','NF','Carrera']

        controles = aux_gen_list_cols('S{}',1,11)
        tareas = aux_gen_list_cols('T{}',1,11)
        formativos = aux_gen_list_cols('F{}',1,11)
        actividades = aux_gen_list_cols('SM{}',1,9)
    
        sheet_data.fillna(0,inplace=True)
        
        sheet_data[controles] = sheet_data[controles].apply(lambda x: x.astype(str).str.replace(',','.')).astype(float)
        sheet_data[tareas] = sheet_data[gen_list_cols('S{}.1',1,11)].apply(lambda x: x.astype(str).str.replace(',','.')).astype(float)
        sheet_data[formativos] = sheet_data[gen_list_cols('S{}.2',1,11)].apply(lambda x: x.astype(str).str.replace(',','.')).astype(float)
        sheet_data[actividades] = sheet_data[gen_list_cols('S{}.3',2,10)].apply(lambda x: x.astype(str).str.replace(',','.')).astype(float)
        sheet_data['Carrera_origen']= sheet_data.Rol.str[4:7]

        df_template = pd.concat(
            [df_template,
            sheet_data[_columns+controles+tareas+formativos+actividades+['Carrera_origen']]
            ])
    

    df_template.Sem=semestre
    df_template.Anno=anno
    df_template.Campus = id_campus
    df_template.fillna(0,inplace=True)

    df_template.to_csv(
        f'{INTERIM}/{anno}-{semestre}/{anno}-{semestre}_{CAMPUS[id_campus]}.csv',
        decimal='.',
        index=False)



def create_campus_csv_AULA(archivo:str,anno:int,semestre:int)->None:
    """
    Descripción:  Genera archivos csv con los datos de los estudiantes  que provienen de la plataforma AULA, para que luego sean transformados y procesados
    Parámetros: - archivo(str) nombre del archivo en excel que se va trabajar
                - anno (int) año trabajado
                - semestre (int) semestre trabajado (1 o 2)
    Retorno: - 
    """
    id_campus = [key for key,val in CAMPUS.items() if val in archivo][0]
    df_base = pd.read_excel(pd.ExcelFile(archivo),None,na_filter=False,skiprows=0,header=0)
    
    for sheet in list(df_base.keys()):
        sheet_data = df_base[sheet]
      
        df=pd.DataFrame()

        df[['RUT','DV.1']] = tuple(sheet_data['Número de ID'].str.split('-'))
        df['Nombre']= sheet_data['Nombre']
        df[['C1','C2','CR']] = sheet_data.filter(regex='Total Certamen').iloc[:,0:]
        df[[f'S{i}' for i in range(1,11)]] = sheet_data.filter(regex='Cuestionario:Control').iloc[:,0:10]
        df[[f'F{i}' for i in range(1,11)]] = sheet_data.filter(regex='Total UVA').iloc[:,0:10]
        df[[f'T{i}' for i in range(1,11)]] = sheet_data.filter(regex='Tarea:Tarea').iloc[:,0:10]
        df[[f'SM{i}' for i in range(1,9)]] = np.nan
        df['Carrera'] = sheet_data['Departamento']
        df['Campus'] = id_campus
        df['Sem']= semestre
        df['Anno']= anno

        df.replace(['-'],0.0,inplace=True)
        df.to_csv(
        f'{INTERIM}/{anno}-{semestre}/{anno}-{semestre}_{CAMPUS[id_campus]}_AULA.csv',
        decimal='.',
        index=False)



def generate(annos_list:list[str])->None:
    threads=[]
    temp='{}-{}'
    for i in annos_list:
        year,sem = i.split('-')
        year = int(year)
        sem = int(sem)
        file_list=get_files_list(temp.format(year,sem))
        
        if not os.path.isdir(f'{INTERIM}/{year}-{sem}'):
            os.mkdir(f'{INTERIM}/{year}-{sem}')

        for f in file_list:
            func = create_campus_csv
            if 'AULA.xlsx' in f.split('_'):
                func= create_campus_csv_AULA

            t = Process(target=func,args=[f,year,sem],daemon=True)
            threads.append(t)
            t.start()
            
    for t in threads:
        t.join()
        
if __name__=='__main__':
    annos=['2020-2','2021-1','2021-2']
    generate(annos)
