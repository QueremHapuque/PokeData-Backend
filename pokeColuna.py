def pokeId(ds):
    listaId = []
    cont = -1
    for i in ds['pokedex_number']:
        cont += 1
        if len(listaId) >= 1:
            if listaId[cont - 1].count('-') > 0:
                if listaId[cont - 1][:listaId[cont-1].index('-')] != str(i):
                    listaId.append(str(i))
                else:
                    proxIndex = 0
                    proxIndex = int(listaId[cont - 1][listaId[cont-1].index('-') + 1:]) + 1
                    r = str(i).replace(str(i), '{}-{}'.format(i, proxIndex))
                    listaId.append(r)
            else:
                if listaId[cont - 1] == str(i):
                    r = str(i).replace(str(i), '{}-1'.format(i))
                    listaId.append(r)
                else:
                    listaId.append(str(i))
        else:
            listaId.append(str(i))

    ds['id'] = listaId
    
    return ds
