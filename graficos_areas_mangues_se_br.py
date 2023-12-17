import geopandas as gpd
import matplotlib.pyplot as plt
from numpy import arange


def grafico_barra(dados: gpd.GeoDataFrame, coluna: str,
                  qt_barra: int, titulo: str) -> None:
    """Função para geração dos gráficos de barras de acordo com a coluna
       desejada, utilizando a contagem de cada valor da coluna.

       :param dados: Dados a serem utilizados para geração do gráfico
       :type dados: pd.DataFrame
       :param coluna: Nome da coluna para contagem dos valores dela
       :type coluna: str
       :param qt_barra: Quantidade de barras a serem exibidas no gráfico
       :type qt_barra: str
       :param titulo: Nome do título do gráfico de barra
       :type titulo: str
    """
    plt.figure(figsize=(15, 5))
    if qt_barra >= 10:
        dados.value_counts(coluna)[:qt_barra].sort_values().plot(
            kind='barh', color=plt.cm.Set1(arange(qt_barra-1, -1, -1)))
        plt.xticks(fontsize=20, rotation=0)
        plt.xlabel('Contagem', fontdict={'fontsize': 20})
        plt.yticks(fontsize=15)
    else:
        dados.value_counts(coluna)[:qt_barra].plot(
            kind='bar', color=plt.cm.Set2(arange(qt_barra)))
        plt.xticks(rotation=0, fontsize=20)
        plt.ylabel('Contagem', fontdict={'fontsize': 20})
        plt.yticks(fontsize=20)
    plt.title(titulo, fontdict={'fontsize': 20, 'fontweight': 'bold'})
    plt.show()
    return None


mangues_br: gpd.GeoDataFrame = gpd.read_file(
    'shapefile_areas_mangues/veg_mangue_a.shp')
mangues_br.dropna(subset='geometry', inplace=True)

area_mangues_uf: gpd.GeoDataFrame = mangues_br.groupby(
    'uf', as_index=False).agg(
        {'area_ha': 'sum', 'nu_area_m2': 'sum', 'uf': 'count'})
area_mangues_uf['media_ha_area_demarc'] = round(
    area_mangues_uf['area_ha'] / area_mangues_uf['uf'], 2)
area_mangues_uf['area_total_%'] = round(
    area_mangues_uf['area_ha'] / mangues_br.area_ha.sum(), 2) * 100
estados_br: list[str] = ['AL', 'AP', 'BA', 'CE', 'ES', 'MA', 'PA', 'PB',
                         'PE', 'PI', 'PR', 'RJ', 'RN', 'SC', 'SE', 'SP']
area_mangues_uf.insert(0, 'estado', estados_br)
area_mangues_uf.rename(columns={"uf": "qt_reserva"}, inplace=True)
area_mangues_uf.sort_values('area_ha', ascending=False, inplace=True)

shapefile_br: gpd.GeoDataFrame = gpd.read_file('shapefile_br/BR_UF_2022.shp')

mangues_se: gpd.GeoDataFrame = mangues_br.loc[mangues_br['uf'] == 'SE']

shapefile_se: gpd.GeoDataFrame = gpd.read_file(
    'shapefile_se/SE_Municipios_2022.shp')

grafico_barra(mangues_br, 'uf',
              10, 'Os 10 estados com a maior quantidade de áreas demarcadas')

area_mangues_uf[:10].plot(
    x="estado",
    y="area_ha",
    ylabel='Área (ha)',
    kind="bar",
    grid=True,
    figsize=(15, 5),
    color=plt.cm.Set2(arange(10)),
    title='Os 10 estados com a maior área total demarcada')
plt.show()

mangues_br.area_ha.plot(
    kind='box', figsize=(8, 6),
    ylabel='Área (ha)', title='Gráfico de caixa das áreas demarcadas - Brasil')
plt.show()

mangues_br.plot(figsize=(10, 8), edgecolor='green')
plt.show()

fig, ax = plt.subplots(figsize=(16, 14))
ax.set_title("Localização dos manguezais no Brasil (2023)",
             fontdict={'fontsize': 20, 'fontweight': 'bold'})
shapefile_br.plot(ax=ax, facecolor='white', edgecolor='black')
mangues_br.plot(ax=ax, edgecolor='green')
plt.show()

mangues_se.area_ha.plot(
    kind='box', figsize=(8, 6),
    ylabel='Área (ha)', title='Gráfico de caixa das áreas demarcadas - Sergipe')
plt.show()

fig, ax = plt.subplots(figsize=(16, 14))
ax.set_title("Localização dos manguezais no estado de Sergipe (2023)",
             fontdict={'fontsize': 20, 'fontweight': 'bold'})
shapefile_se.plot(ax=ax, facecolor='#ad5613', edgecolor='black')
mangues_se.plot(ax=ax, edgecolor='green')
plt.show()
