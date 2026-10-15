import subprocess
import pandas as pd
import numpy as np


subprocess.run('cls', shell=True)
# Obtendo os dados
try:
    print('Obteno dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    
    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    #print(df_ocorrencias)

    # Delimitando dados
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    #print(df_roubo_veiculo.head(30))
    #print(df_roubo_veiculo.tail(30))


    # ### PREPARANDO OS DADOS

    # Totalizando os roubos por cidade (Var Qualitativa 'munic' e Var Quantitativa 'roubo_veiculo')
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()
    #print(df_roubo_veiculo.head(30))

    # Ordenando os dados
    df_roubo_veiculo = df_roubo_veiculo.sort_values(
        by='roubo_veiculo',
        ascending=False
    )
    print(df_roubo_veiculo.head(10))
    #print(df_roubo_veiculo.tail(10))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')


try:
    print(f'\nObtendo informações a cerca dos roubos dos veículos... ')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    # distancia da média para a mediana
    distancia = abs(
        (media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100
    )

    print('\nMedias de tendência Central')
    print(f'Média: {media_roubo_veiculo:.2f}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distancia Entre Média e Mediana: {distancia:.2f}%')



except Exception as e:
    print(f'Obtendo Medidas - {e}')


try:
    q1 = np.quantile(array_roubo_veiculo, .25)
    q2 = np.quantile(array_roubo_veiculo, .50)
    q3 = np.quantile(array_roubo_veiculo, .75)

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # Cidades c/ Menos ocorrencias de roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] < q1
    ]

    # Cidades c/ Maiores ocorrencias de roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] > q3
    ]

    print('\nMunicipios com menores roubos ')
    print(30*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    df_roubo_veiculo_menores.to_csv('menores.csv', index=False, sep=';', encoding='iso-8859-1')

    print('\nMunicipios com Maiores roubos ')
    print(30*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))
    df_roubo_veiculo_maiores.to_csv('maiores.csv', index=False, sep=';', encoding='iso-8859-1')


except Exception as e:
    print(f'Erro ao Analizar a distribuição - {e}')

# Achando os outliers
try:
    # Intervalo Interquartil
    # É a amplitude dos dados mais centrais
    iqr = q3 - q1

    # Calcular os limites
    # Superior 
    limite_superior = q3 + (1.5 * iqr)
    print(f'\nLimite superior: {limite_superior}')

    # Inforior
    limite_inferior = q1 - (1.5 * iqr)
    print(f'\nLimite inferior: {limite_inferior}')

    # Filtrando outliers menores
    df_roubo_veiculo_outliers_menores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    )

    print('\nMunicipios com outliers inferiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_menores) == 0:
        print('Não há outliers Inferiores')
    else:
        print(df_roubo_veiculo_outliers_menores)

    # Filtrando outliers maiores
    df_roubo_veiculo_outliers_maiores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    )

    print('\nMunicipios com outliers superiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_maiores) == 0:
        print('Não há outliers maiores')
    else:
        print(df_roubo_veiculo_outliers_maiores)


except Exception as e:
    print(f'Erro ao calcular os outliers- {e}')
