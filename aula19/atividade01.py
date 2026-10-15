import subprocess
import pandas as pd
import numpy as np


subprocess.run('cls', shell=True)

try:
    print('Obteno dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    df_estelionato = df_ocorrencias[['estelionato', 'mes_ano']]
    df_estelionato = df_estelionato.groupby('mes_ano', as_index=False)['estelionato'].sum()

    print(30*'-')
    print('Estelionatos Mês/Ano:')
    print(30*'-')
    print(df_estelionato)

except Exception as e:
    print(f'Erro ao obter os dados - {e}')


try:
    array_estelionato = np.array(df_estelionato['estelionato'])

    media_estelionato = np.mean(array_estelionato)
    mediana_estelionato = np.median(array_estelionato)

    distancia = abs((media_estelionato - mediana_estelionato) / mediana_estelionato * 100)

    print()
    print(30*'-')
    print('Medias de tendência Central:')
    print(30*'-')
    print(f'Média: {media_estelionato:.2f}')
    print(f'Mediana: {mediana_estelionato}')
    print(f'Distancia Entre Média e Mediana: {distancia:.2f}%\n')

except Exception as e:
    print(f'Obtendo Medidas - {e}')


try:
    q1 = np.quantile(array_estelionato, .25)
    q2 = np.quantile(array_estelionato, .50)
    q3 = np.quantile(array_estelionato, .75)

    df_estelionato_menores = df_estelionato[df_estelionato['estelionato'] < q1]
    df_estelionato_maiores = df_estelionato[df_estelionato['estelionato'] > q3]

    print(70*'-')
    print(f'Os Meses/Ano com menos estelionato estão abaixo de {q1} estelionatos: ')
    print(70*'-')
    print(df_estelionato_menores.sort_values(by='estelionato', ascending=True))

    print(70*'-')
    print(f'Os Meses/Ano com mais estelionato estão acima de {q3} estelionatos: ')
    print(70*'-')
    print(df_estelionato_maiores.sort_values(by='estelionato', ascending=False))

    print(f'''
------------------------------------
Não exite um padrão nas ocorrências:
------------------------------------
A distancia de Média e a Mediana está superior a {distancia:.2f}%,
então foi considerado que a mediana que é de {mediana_estelionato} estelionatos
como mediad central para realizar a análise.

25% dos casos de estelionato estão de abaixo de {q1} estelionatos.
Os Meses/Ano acima de 75% dos casos de estelionato estão de acima de {q3} estelionatos.
''')

except Exception as e:
    print(f'Erro ao Analizar a distribuição - {e}')


try:
    iqr = q3 - q1
    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)
    
    # Filtrando outliers menores
    df_estelionato_outliers_menores = (
        df_estelionato[df_estelionato['estelionato'] < limite_inferior]
    )

    # Filtrando outliers maiores
    df_estelionato_outliers_maiores = (
        df_estelionato[df_estelionato['estelionato'] > limite_superior]
    )


    print('''
------------------------------------
Estelionatos com outliers inferiores
------------------------------------
    ''')
    if len(df_estelionato_outliers_menores) == 0:
        print('Não há outliers Inferiores')
    else:
        print(f'\nOs Outliers estão abaixo de: {limite_inferior}\n')
        print(df_estelionato_outliers_menores)
    
    print('''
------------------------------------
Estelionatos com outliers Superiores
------------------------------------''')
    if len(df_estelionato_outliers_maiores) == 0:
        print('Não há outliers superiores')
    else:
        print(f'\nOs Outliers estão acima de: {limite_superior}\n')
        print(df_estelionato_outliers_maiores)

except Exception as e:
    print(f'Erro ao calcular os outliers- {e}')
