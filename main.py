import requests
from bs4 import BeautifulSoup
from pprint import pprint

from Imovel import Imovel


Imovel.create_table()
teste_quantidade = Imovel.select().count()
if teste_quantidade == 0:
    r = requests.get('https://venda-imoveis.caixa.gov.br/listaweb/Lista_imoveis_RJ.htm').text
    soup = BeautifulSoup(r, "lxml")
    imoveis = soup.find_all("tr")
    del imoveis[0]

    for imovel in imoveis:
        endereco = imovel.find_all("td")[1].text.strip()
        bairro = imovel.find_all("td")[2].text.strip()
        preco = float(imovel.find_all("td")[4].text.strip().replace(".", "").replace(",", "."))
        desconto = float(imovel.find_all("td")[6].text.strip())
        modalidade = imovel.find_all("td")[7].text.strip()

        objeto_imovel = Imovel(endereco=endereco, bairro=bairro, preco=preco, desconto=desconto, modalidade=modalidade)

        objeto_imovel.save()

lista_imoveis = Imovel.select()

favoritos = []
encontrou_imovel = False

while True:
    print("1) Bairro"
          "\n2) Ordenado por preço (menor para o maior)"
          "\n3) Desconto"
          "\n4) Modalidade de venda"
          "\n5) Filtro de preco personalizado"
          "\n6) Mostrar imóveis salvos"
          "\n7) Deletar imóveis salvos"
          "\n8) Para fechar o menu")

    p1 = input("Como deseja filtrar os imoveis?(Escolha uma opção acima) ")

    if p1 == "1":
        b = input("Por qual bairro você quer procurar? ").upper().strip()
        for imovel in lista_imoveis:
            if imovel.bairro == b:
                pprint(f'Imóvel encontrado: {imovel}')
                encontrou_imovel = True
        if not encontrou_imovel:
            print('O bairro que você procura não está na lista')
        if encontrou_imovel:
            try:
                op_id_do_imovel = int(input('Qual imóvel gostaria de salvar? Digite o ID '))
                for imovel in lista_imoveis:
                    if op_id_do_imovel == imovel.id:
                        if imovel not in favoritos:
                            favoritos.append(imovel)
                        else:
                            print('Este imóvel já está na lista')
            except ValueError:
                print('Um erro ocorreu: você usou palavras invés de números')
            pprint('Lista dos imóveis salvos: {}'.format(favoritos))
        op_continuar = input('Gostaria de fazer mais alguma operação?[S/N] ').upper()
        if op_continuar == 'N':
            break

    if p1 == '2':
        ordenada = sorted(lista_imoveis, key=lambda k: k.preco)
        pprint(ordenada)
        encontrou_imovel = True
        if encontrou_imovel:
            try:
                op_id_do_imovel = int(input('Qual imóvel gostaria de salvar? Digite o ID '))
                for imovel in lista_imoveis:
                    if op_id_do_imovel == imovel.id:
                        if imovel not in favoritos:
                            favoritos.append(imovel)
                        else:
                            print('Este imóvel já está salvo')
            except ValueError:
                print('Um erro ocorreu: você usou palavras invés de números')
            pprint(f'Lista dos imóveis salvos: {favoritos}')
        op_continuar = input('Gostaria de fazer mais alguma operação?[S/N] ').upper()
        if op_continuar == 'N':
            break

    if p1 == '3':
        try:
            p = int(input('Quanto de desconto você quer procurar?(em %) '))
            for imovel in lista_imoveis:
                if imovel.desconto == p:
                    print(f'Imóvel encontrado: \n%s' % imovel)
                    encontrou_imovel = True
            if not encontrou_imovel:
                print('Não há itens na lista que correspondem a esta porcentagem')
        except ValueError:
            print('Um erro ocorreu! Digite apenas números, sem pontuação')
        if encontrou_imovel:
            try:
                op_id_do_imovel = int(input('Qual imóvel gostaria de salvar? Digite o ID '))
                for imovel in lista_imoveis:
                    if op_id_do_imovel == imovel.id:
                        if imovel not in favoritos:
                            favoritos.append(imovel)
                        else:
                            print('Este imóvel já está na lista')
            except ValueError:
                print('Um erro ocorreu: você usou palavras invés de números')
            pprint(f'Lista dos imóveis salvos: {favoritos}')
        op_continuar = input('Gostaria de fazer mais alguma operação?[S/N] ').upper()
        if op_continuar == 'N':
            break

    if p1 == '4':
        e = input('Escolha uma das seguintes opções:'
                  '\n1) Venda Online'
                  '\n2) Venda Direta Online'
                  '\n3)2º Leilão SFI ')
        for imovel in lista_imoveis:
            if e == '1':
                if imovel.modalidade == 'Venda Online':
                    print(f'Imóvel encontrado: {imovel}')
                    encontrou_imovel = True
            elif e == '2':
                if imovel.modalidade == 'Venda Direta Online':
                    print(f'Imóvel encontrado: {imovel}')
                    encontrou_imovel = True
            elif e == '3':
                if imovel.modalidade == '2º Leilão SFI':
                    print(f'imovel encontrado: {imovel}')
                    encontrou_imovel = True
        if encontrou_imovel:
            try:
                op_id_do_imovel = int(input('Qual imóvel gostaria de salvar? Digite o ID '))
                for imovel in lista_imoveis:
                    if op_id_do_imovel == imovel.id:
                        if imovel not in favoritos:
                            favoritos.append(imovel)
                        else:
                            print('Este imóvel já foi salvo')
            except ValueError:
                print('Um erro ocorreu: você usou palavras invés de números')
            pprint(f'Lista dos imóveis salvos: {favoritos}')
        op_continuar = input('Gostaria de fazer mais alguma operação?[S/N] ').upper()
        if op_continuar == 'N':
            break


    if p1 == '5':
        try:
            min = int(input('Preço inicial: '))
            teto = int(input('Preço máximo: '))
            for imovel in lista_imoveis:
                if imovel.preco in range(min, teto):
                    encontrou_imovel = True
                    print(f'Imóvel encontrado: {imovel}')
        except ValueError:
            print('Digite apenas números, sem pontuação')
        if encontrou_imovel:
            try:
                op_id_do_imovel = int(input('Qual imóvel gostaria de salvar? Digite o ID '))
                for imovel in lista_imoveis:
                    if op_id_do_imovel == imovel.id:
                        if imovel not in favoritos:
                            favoritos.append(imovel)
                        else:
                            print('Este imóvel já foi salvo')
            except ValueError:
                print('Um erro ocorreu: você usou palavras invés de números')
            pprint(f'Lista dos imóveis salvos: {favoritos}')
        op_continuar = input('Gostaria de fazer mais alguma operação?[S/N] ').upper()
        if op_continuar == 'N':
            break

    if p1 == '6':
        print(favoritos)
        op_continuar = input('Gostaria de fazer mais alguma operação?[S/N] ').upper()
        if op_continuar == 'N':
            break

    if p1 == '7':
        op_del_quant = input('Quantos itens da lista você quer deletar?\n'
                             '1) Todos os itens\n'
                             '2) Apenas 1 ')
        if op_del_quant == '1':
            favoritos.clear()
        if op_del_quant == '2':
            id_do_imovel_deletar = int(input('Escolha um imóvel para deletar: '))
            for numero, imovel in enumerate(lista_imoveis):
                if id_do_imovel_deletar == imovel.id:
                    favoritos.remove(imovel)
                    #del favoritos[numero]
        op_continuar = input('Gostaria de fazer mais alguma operação?[S/N] ').upper()
        if op_continuar == 'N':
            break

    if p1 == '8':
        break


