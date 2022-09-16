from sklearn.cluster import KMeans

colunas_quantitativas_ordinais = ['hp',
                                  'attack',
                                  'defense',
                                  'special_attack',
                                  'special_defense',
                                  'speed',
                                  'height',
                                  'weight',
                                  'female_rate',
                                  'base_experience',
                                  'capture_rate',
                                  'egg_cycles',
                                  'base_happiness',
                                  'number_pokemon_with_typing',
                                  'normal_attack_effectiveness',
                                  'fire_attack_effectiveness',
                                  'water_attack_effectiveness',
                                  'electric_attack_effectiveness',
                                  'grass_attack_effectiveness',
                                  'ice_attack_effectiveness',
                                  'fighting_attack_effectiveness',
                                  'poison_attack_effectiveness',
                                  'ground_attack_effectiveness',
                                  'fly_attack_effectiveness',
                                  'psychic_attack_effectiveness',
                                  'bug_attack_effectiveness',
                                  'rock_attack_effectiveness',
                                  'ghost_attack_effectiveness',
                                  'dragon_attack_effectiveness',
                                  'dark_attack_effectiveness',
                                  'steel_attack_effectiveness',
                                  'fairy_attack_effectiveness',
                                  'gen_introduced']
colunas_categorias_nominais = ['typing', 'genus',
                               'egg_groups', 'primary_color', 'shape']
colunas_booleanas = ['genderless', 'baby_pokemon', 'legendary',
                     'mythical', 'is_default', 'forms_switchable', 'can_evolve']

def normalize(dataframe):
    for column in colunas_quantitativas_ordinais:
        dataframe[column] = (dataframe[column]-dataframe[column].min()) / (
            dataframe[column].max()-dataframe[column].min())

def type_one_hot_encode(dataframe):
    unique_val = dataframe["typing"].unique()

    type_iterator = list()
    for type in unique_val:
        if not ("~" in type):
            type_iterator.append(type)

    for i in range(len(dataframe)):
        type_aux = type_iterator[:]
        if '~' in dataframe.loc[i, 'typing']:
            pokemon_types = dataframe.loc[i, 'typing'].split('~')
            dataframe.loc[i, pokemon_types[0]] = int(1)
            dataframe.loc[i, pokemon_types[1]] = int(1)
            type_aux.pop(type_aux.index(pokemon_types[0]))
            type_aux.pop(type_aux.index(pokemon_types[1]))
            for j in type_aux:
                dataframe.loc[i, j] = int(0)
        else:
            mono_type = dataframe.loc[i, 'typing']
            dataframe.loc[i, mono_type] = int(1)
            type_aux.pop(type_aux.index(mono_type))
            for k in type_aux:
                dataframe.loc[i, k] = int(0)

    dataframe.drop(['typing'], axis=1, inplace=True)

def one_hot_encode_column(dataframe, col):

    unique_val = dataframe[col].unique()

    var_iterator = [itemlist for itemlist in unique_val]
    for index in range(len(dataframe)):
        varIterator_aux = var_iterator[:]
        current_val = dataframe.loc[index, col]
        dataframe.loc[index, current_val] = 1
        varIterator_aux.pop(varIterator_aux.index(current_val))
        for index_i in varIterator_aux:
            dataframe.loc[index, index_i] = 0

    dataframe.drop([col], axis=1, inplace=True)


# def one_hot_encode_column(dataFrame, col):

#    unique_val = dataFrame[col].unique()
#    ds_aux = pd.DataFrame(columns=unique_val)   
#    var_iterator = [itemlist for itemlist in unique_val]
#    for index in range(len(dataFrame)):
#        dataAux = list()
#        current_val = dataFrame.loc[index, col]
#        for index_i in var_iterator:
#          if current_val == index_i:
#            dataAux.append(1)
#          else:
#            dataAux.append(0)
#        ds_aux.loc[index] = dataAux
   
#    new_dataFrame = pd.concat([dataFrame, ds_aux], axis= 1)
#    new_dataFrame.drop([col], axis=1, inplace=True)
#    return new_dataFrame




def one_hot_encode_all(dataframe):
    all_but_type = colunas_categorias_nominais.copy()
    all_but_type.remove('typing')
    for coluna in all_but_type:
        one_hot_encode_column(dataframe,coluna)
    
def bool_to_int(dataframe):
    for coluna in colunas_booleanas:
        dataframe[coluna] = dataframe[coluna].astype(int)

def create_cluster(dataframe, k):
    dataframe_copy = dataframe.copy()
    dataframe_done = dataframe_copy[colunas_booleanas+colunas_categorias_nominais+colunas_quantitativas_ordinais]
    normalize(dataframe_done)
    type_one_hot_encode(dataframe_done)
    one_hot_encode_all(dataframe_done)
    bool_to_int(dataframe_done)
    cluster = KMeans(n_clusters=k)
    cluster.fit(dataframe_done)
    
    return cluster.labels_
