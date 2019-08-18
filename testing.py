
import json, sys
from datetime import datetime, timedelta

class Main:
    def __init__(self):  
        datas = open('entrada/entrada.json', 'r')

        # transforma as linhas em uma unica strig
        str_dados = ''
        lista = []
        for data in datas:
            
            if not data == ' ' or not data == '\t' or not data == '\n':
                str_dados += data
            

        # para separar os varios jsons, od json.loads pega apenas um por vez
        i = 0
        new_str = ''
        lista = []
        while i < len(str_dados):
            new_str += str_dados[i]
            if str_dados[i] == '}' and str_dados[i+1] == ',':
                lista.append(new_str)
                new_str = ''
                i += 1
            i += 1
        
       
        # monta uma lista com varios dicionarios
        lista_json = []
        for js in lista:
            lista_json.append(json.loads(js))
        
        dic_msg_user = {}
        list_msg_user = {}
        # item na lista de dicionarios
        for item in lista:

            item_json = json.loads(item)
            
            # agrupar por usuario
            # montar dicionario com user como chave e uma lista de mensagens dele
            if item_json['user'] in dic_msg_user:
                dic_msg_user[item_json['user']].append(item_json)
            else:
                dic_msg_user[item_json['user']] = [item_json]
            # for index in item_json.items():
            #     for j in index:
            #         print(index)
            #         break
        
        lista_total_times = []
        for item in dic_msg_user:
            lista_msg_times = []
            for msg_user in dic_msg_user[item]:
                # transforma em datetime para comparar
                times = msg_user['ts']
                times = float(times)
                data = datetime.fromtimestamp(times)
                mais2 = data + timedelta(minutes=2)
                menos2 = data - timedelta(minutes=2)
                # print('data {}, +2 {}, -2 {}'.format(data, mais2, menos2))
                
                #primeiro item adiciona
                if len(lista_total_times) == 0:
                    lista_total_times.append([msg_user])
                # se não percorre as duas listas para comparar
                else:
                    encontrou = False
                    for total in lista_total_times:
                        for item in total:
                            times_2 = item['ts']
                            times_2 = float(times_2)
                            data_2 = datetime.fromtimestamp(times_2)
                            # se o item atual esta no range com o item da lista adiona na lista equivalente
                            if data_2 <= mais2 and data_2 >= menos2:
                                # print('data {} - tem 2 de dif:  {}'.format(data, data_2))
                                if item['user'] == msg_user['user']:
                                    total.append(msg_user)
                                    encontrou = True
                                    break
                    # se percorreu todas as lista e nao achou adiona uma nova lista com esse item
                    if not encontrou:
                        lista_total_times.append([msg_user])


       

        #remover itens repetidos
        for total in lista_total_times:
            nova_lista = []
            for valor in total:
                # print(total)
                if not valor in nova_lista:
                    nova_lista.append(valor)

            lista_total_times[lista_total_times.index(total)] = nova_lista
            
            

        dic_final = {}

        # monta dicionario para salvar no arquivo
        for total in lista_total_times:
            chave = total[0]['ts']
            name = total[0]['user'] 
            corpo = total
            dic_saida = {}
            dic_saida[chave] = corpo

            if not total[0]['user'] in dic_final:
                dic_final[total[0]['user']] = [dic_saida]
            else:
                dic_final[total[0]['user']].append(dic_saida)

        # percorre o dicionario e salva nos arquivos
        for saida in dic_final:
            with open('saida/{}.json'.format(saida), 'w') as f:
                json.dump(dic_final[saida], f)
            



Main()
 