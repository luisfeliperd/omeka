#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from collections import defaultdict
import pandas as pd
import time


# In[2]:


endpoint_items = 'http://bdce.unb.br/api/items'
endpoint_collections = 'http://bdce.unb.br/api/collections'
response = requests.get(endpoint_items, params = {'page':'1'})
metadata_dict = defaultdict(list)
metadatum_dict = {'Coordenadora do Curso de Comunicação Organizacional':[],'Diretor de Marketing':[],'Diagramador(es)':[],'Repórteres':[],'Editor ou diretor de arte':[],'Coordenadora de Laboratórios':[],'Chefe de Departamento de Comunicação Organizacional':[],'Suporte de informática':[],'Publisher':[],'Projeto de Marketing':[],'Equipe':[],'Secretário de redação':[],'Monitor(es)':[],'Projeto gráfico':[],'Revisão':[],'Chefe de Departamento de Audiovisuais e Publicidade':[],'Editor(es)':[],'Colaborador(es)':[],'Executivo de Marketing':[],'Coordenador(a) de Graduação':[],'Editor(a) de Arte':[],'Localização no CEDOC':[],'Creator':[],'Editor(a) executivo':[],'Colaboradores':[],'Revisor de arte':[],'Coordenadora de Projetos Finais':[],'Dimensões físicas':[],'Secretária de Redação':[],'Professor(es)':[],'Coordenador de Pós-Graduação':[],'Fotógrafo':[],'Secretária de Marketing':[],'Capa':[],'Localização no arquivo':[],'Impressão':[],'Coordenador(a) de Extensão':[],'Subject':[],'Editor(a) chefe':[],'Secretário(a)':[],'Revisor(es)':[],'Chefe de Departamento de Jornalismo':[],'Ilustrador(es)':[],'Title':[],'Notas':[],'Jornalista(s)':[],'Gráfica':[],'Date':[],'Editor de Fotográfia':[]}
metadata_dict.update(metadatum_dict)
items = response.json()


# In[3]:


#Extração dos Metadados
page = 0

while requests.get(endpoint_items, params = {'page':page}).json():
    
    items = requests.get(endpoint_items, params = {'page':page}).json()
    
    page+=1
    
    print(page, end=", ")  
    
    for item in items:
        
                                #### Coleção ####
        metadata_dict['id'].append(item['id'])
        
        try:
            metadata_dict['colecao'].append(item['collection']['id'])
        except:
            metadata_dict['colecao'].append('')
            
                                ####  METADADOS  ####
        metadatum_dict = {'Coordenadora do Curso de Comunicação Organizacional':[],'Diretor de Marketing':[],
                          'Diagramador(es)':[],'Repórteres':[],'Editor ou diretor de arte':[],
                          'Coordenadora de Laboratórios':[],'Chefe de Departamento de Comunicação Organizacional':[],
                          'Suporte de informática':[],'Publisher':[],'Projeto de Marketing':[],'Equipe':[],
                          'Secretário de redação':[],'Monitor(es)':[],'Projeto gráfico':[],'Revisão':[],
                          'Chefe de Departamento de Audiovisuais e Publicidade':[],'Editor(es)':[],'Colaborador(es)':[],
                          'Executivo de Marketing':[],'Coordenador(a) de Graduação':[],'Editor(a) de Arte':[],
                          'Localização no CEDOC':[],'Creator':[],'Editor(a) executivo':[],'Colaboradores':[],
                          'Revisor de arte':[],'Coordenadora de Projetos Finais':[],'Dimensões físicas':[],
                          'Secretária de Redação':[],'Professor(es)':[],'Coordenador de Pós-Graduação':[],'Fotógrafo':[],
                          'Secretária de Marketing':[],'Capa':[],'Localização no arquivo':[],'Impressão':[],
                          'Coordenador(a) de Extensão':[],'Subject':[],'Editor(a) chefe':[],'Secretário(a)':[],
                          'Revisor(es)':[],'Chefe de Departamento de Jornalismo':[],'Ilustrador(es)':[],'Title':[],
                          'Notas':[],'Jornalista(s)':[],'Gráfica':[],'Date':[],'Editor de Fotográfia':[]}
        
        for metadata in item['element_texts']:
            
            for key in metadatum_dict.keys():
                
                if key == metadata['element']['name']:
                    metadatum_dict[key].append(metadata['text'])
                    
                else:
                    metadatum_dict[key].append('')
                    
        for key in metadatum_dict.keys():
            
            metadatum_dict[key] = list(filter(None, metadatum_dict[key]))
            
            if metadatum_dict[key]:
                metadata_dict[key].append("||".join(metadatum_dict[key]))
                
            else:
                 metadata_dict[key].append("".join(metadatum_dict[key]))
            
                                ##### ANEXOS #####
                
        #O json do item direcina par outro json com os links dos arquivos anexados ao item
        lista_att = []

        #acessando o endpoint do json dos anexos do item
        files = requests.get(item['files']['url'])

        #adiciona a url de cada anexo em uma lista
        for file in files.json():
            lista_att.append(file['file_urls']['original'])

        #para documento principal no Tainacan
        if not lista_att:
            document = ''
            attch = ''
            
        else:
            document = lista_att[0]

            #para anexos no Tainacan
            if len(lista_att) >1:
                attch = "||".join(lista_att[1:])
            else:
                attch = ''
        metadata_dict['document'].append(document)
        metadata_dict['attachment'].append(attch)                

                                        #### EXIBIÇÕES ####
        exhibit_dict = defaultdict(list)
        
        exhibit_endpoint = item['extended_resources']['exhibit_pages']['url']
        exhibits = requests.get(exhibit_endpoint).json()

        
        if len(exhibits) == 0:
            exhibit_dict['id'].append('')
            exhibit_dict['title'].append('')
        
        elif len(exhibits) == 9:
            exhibit_dict['id'].append(str(exhibits['id']))
            exhibit_dict['title'].append(exhibits['title'])
        
        else:
            for exhibit in exhibits:
                exhibit_dict['id'].append(str(exhibit['id']))
                exhibit_dict['title'].append(exhibit['title'])

        metadata_dict['exhibit_id'].append("||".join(exhibit_dict['id']))
        metadata_dict['exhibit_name'].append("||".join(exhibit_dict['title']))
        
                                    #### GEOLOCALIZAÇÕES ####
        if 'geolocations' in item['extended_resources'].keys():
            
            geolocation_endpoint = item['extended_resources']['geolocations']['url']
            geolocation = requests.get(geolocation_endpoint).json()
            
            #Latitude, Longitude, Endereço
            metadata_dict['geo_latitude'].append(geolocation['latitude'])
            metadata_dict['geo_longitude'].append(geolocation['longitude'])
            metadata_dict['geo_adress'].append(geolocation['address'])
        else:
            metadata_dict['geo_latitude'].append('')
            metadata_dict['geo_longitude'].append('')
            metadata_dict['geo_adress'].append('')
    
                                                #### TAGS ####
        lista_tags = []
        
        for tag in item['tags']:
            lista_tags.append(tag['name'])
            
        lista_tags = list(filter(None, lista_tags))
        
        if len(lista_tags)>1:
            metadata_dict['tags'].append("||".join(lista_tags))
        else:
            metadata_dict['tags'].append("".join(lista_tags))
            
    time.sleep(20)
    
for key in metadata_dict.keys():
    print(key, len(metadata_dict[key]))


# In[4]:


expt_df = pd.DataFrame(metadata_dict)
expt_df.to_csv('itens_omeka_bdce.csv')


# # SUBTIPOS DE METADADOS
# 
#          """                     #### INFOS BÁSICAS ####
#         
#         for value in item.keys():
#             if type(item[value]) != dict and type(item[value]) != list:
#                 metadata_dict[value].append(str(item[value]))
#         """

# In[ ]:


#INFOS BÁSICAS DO ITEM (OK)
infos_dict = {}

for item in items[0]:
    if type(items[0][item]) != dict and type(items[0][item]) != list:
        infos_dict[item] = str(items[0][item])

print(infos_dict)


# In[ ]:


#TAGS DO ITEM
for tag in items[0]['tags']:
    print(tag['name'])


# In[ ]:


#ANEXOS (OK)
#O json do item direcina par outro json com os links dos arquivos anexados ao item
lista_att = []

#acessando o endpoint do json dos anexos do item
files = requests.get(items[0]['files']['url'])

#adiciona a url de cada anexo em uma lista
for file in files.json():
    lista_att.append(file['file_urls']['original'])

#para documento principal no Tainacan
document = lista_att[0]

#para anexos no Tainacan
if len(lista_att) >1:
    attch = "||".join(lista_att[1:])
else:
    attch = ''
print(document, attch)


# In[ ]:


#RELAÇÃO COM EXIBIÇÃO (OK)
exhibit_endpoint = items[0]['extended_resources']['exhibit_pages']['url']
exhibit = requests.get(exhibit_endpoint).json()

#Id e nome da exibição
exhibit_id = exhibit['id']
exhibit_name = exhibit['title']

print(exhibit_id, exhibit_name)


# In[ ]:


#GEOLOCALIZAÇÃO #Pode não ocorrer (OK)
geolocation_endpoint = items[0]['extended_resources']['geolocations']['url']
geolocation = requests.get(geolocation_endpoint).json()

#Latitude, Longitude, Endereço
geo_latitude = geolocation['latitude']
geo_longitude = geolocation['longitude']
geo_adress = geolocation['address']

print(geo_latitude, geo_longitude, geo_adress)


# In[ ]:


#METADADOS DO ITEM (OK)
for metadata in items[0]['element_texts']:
    print(metadata['element']['name'], metadata['text'])


# In[ ]:


#ITERAR PELAS PÁGINAS DE ITENS
page = 0

while requests.get(endpoint_items, params = {'page':page, 'per_page':'5'}).json():
    page+=1
    print(page)
    
    for item in requests.get(endpoint_items, params = {'page':page, 'per_page':'5'}).json():


# In[ ]:


#teste
page = 0

lista_metadata = []

while requests.get(endpoint_items, params = {'page':page}).json():
    page+=1
    print(page)
    
    for item in requests.get(endpoint_items, params = {'page':page}).json():        
        
        for metadata in item['element_texts']:
            for key in metadatum_dict.keys():
                if key == metadata['element']['name']:
                    metadatum_dict[key].append(metadata['text'])
                else:
                    metadatum_dict[key].append('')


# In[ ]:




