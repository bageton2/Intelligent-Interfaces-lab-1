
import PySimpleGUI as sg
from faker import Faker
from faker.providers import DynamicProvider
import pandas as pd


flatsfile ='flats.csv'
flatsfuzzfile ='flats_fuzz.csv'

flat_size_provider = DynamicProvider(
     provider_name="flat_size",
     elements=range(20,100))

flat_floor_provider = DynamicProvider(
     provider_name="flat_floor",
     elements=range(1,25))

flat_district_provider = DynamicProvider(
     provider_name="flat_district",
     elements=['Голосіївський','Оболонський','Печерський','Подільський',
               'Святошинський','Солом''янський','Шевченківський','Дарницький','Деснянський','Дніпровський'])

flat_metro_distance = DynamicProvider(
     provider_name="flat_metro",
     elements=range(100,5_000))

flat_rooms_provider = DynamicProvider(
     provider_name="flat_rooms",
     elements=range(1,4))

flat_renovation_provider = DynamicProvider(
     provider_name="flat_renovation",
     elements=['old','new','fashion','classic'])

flat_price_provider = DynamicProvider(
     provider_name="flat_price",
     elements=range(10_000, 100_000))


fake = Faker()
fake.add_provider(flat_size_provider)
fake.add_provider(flat_floor_provider)
fake.add_provider(flat_district_provider)
fake.add_provider(flat_metro_distance)
fake.add_provider(flat_rooms_provider)
fake.add_provider(flat_renovation_provider)
fake.add_provider(flat_price_provider)

def generate_data():
    df_faker = pd.DataFrame(create_rows_faker(5000))
    df_faker.to_csv(flatsfile)

def analyze_data():
    df = pd.read_csv(flatsfile, index_col=0)

    df['size_fuzz'] = df.apply(lambda a: size_to_fuzz(a['size']), axis=1)
    df['floor_fuzz'] = df.apply(lambda a: floor_to_fuzz(a.floor), axis=1)
    df['metro_fuzz'] = df.apply(lambda a: metro_to_fuzz(a.metro), axis=1)
    df['rooms_fuzz'] = df.apply(lambda a: rooms_to_fuzz(a.rooms), axis=1)
    df['price_fuzz'] = df.apply(lambda a: price_to_fuzz(a.price), axis=1)

    df.to_csv(flatsfuzzfile)
    return

sizes = ['Small','Normal', 'Large']

def size_to_fuzz(size):
    if 20 <= size <= 35:
        return sizes[0]
    elif 35 < size <= 65:
        return sizes[1]
    elif 65 < size <= 100:
        return sizes[2]

floors = ['Low','Normal', 'High']

def floor_to_fuzz(floor):
    if 1 <= floor <= 4:
        return floors[0]
    elif 4 < floor <= 12:
        return floors[1]
    elif 12 < floor <= 25:
        return floors[2]

metros = ['Near', 'Normal', 'Far']

def metro_to_fuzz(metro):
    if 100 <= metro <= 500:
        return metros[0]
    elif 500 < metro <= 2_500:
        return metros[1]
    elif 2_500 < metro <= 5_000:
        return metros[2]

rooms = ['Few', 'Normal', 'Many']

def rooms_to_fuzz(room):
    if 1 <= room <= 1:
        return rooms[0]
    elif 1 < room <= 3:
        return rooms[1]
    elif 3 < room <= 4:
        return rooms[2]

prices = ['Cheap', 'Normal', 'Expensive']

def price_to_fuzz(price):
    if 10_000 <= price <= 30_000:
        return prices[0]
    elif 30_000 < price <= 50_000:
        return prices[1]
    elif 50_000 < price <= 100_000:
        return prices[2]

def create_rows_faker(num=1):
    output = [{"size":fake.flat_size(),
                   "floor":fake.flat_floor(),
                   "district":fake.flat_district(),
                   "metro":fake.flat_metro(),
                   "rooms":fake.flat_rooms(),
                   "renovation":fake.flat_renovation(),
                   "price":fake.flat_price()} for x in range(num)]
    return output


header = ['size','floor','district','metro','rooms','renovation','price','size_fuzz','floor_fuzz','metro_fuzz','rooms_fuzz','price_fuzz']
def create_UI():
    data_values = pd.read_csv(flatsfuzzfile, index_col=0).values
    data_cols_width = [5, 8, 35, 35]
    sg.theme('Dark Blue')
    layout = [[sg.Text('Area:')], [sg.Input('', enable_events=True, key='area', )],
              [sg.Text('floor:')], [sg.Listbox(range(1, 25), size=(20,4), enable_events=False, key='floor')],
              [sg.Text('district:')], [sg.Listbox(flat_district_provider.elements, size=(20,4), enable_events=False, key='district')],
              [sg.Text('metro distance:')], [sg.Input('', enable_events=True, key='metroDistance', )],
              [sg.Text('rooms:')], [sg.Input('', enable_events=True, key='rooms', )],
              [sg.Text('renovation:')], [sg.Listbox(flat_renovation_provider.elements, size=(20,4), enable_events=False, key='renovation')],
              [sg.Text('price:')], [sg.Input('', enable_events=True, key='price', )],
              [sg.Button('Submit', visible=True, bind_return_key=True)],

              [sg.Table(values=data_values, headings=header,
                        max_col_width=65,
                        col_widths=data_cols_width,
                        auto_size_columns=False,
                        justification='left',
                        num_rows=6, key='_filestable_')],
              [sg.Button('Exit')],
              ]

    window = sg.Window('Window Title', layout)

    while True:  # Event Loop
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        # if last char entered not a digit
        if len(values['area']) and values['area'][-1] not in ('0123456789'):
            # delete last char from input
            window['area'].update(values['area'][:-1])
        elif  len(values['rooms']) and values['rooms'][-1] not in ('0123456789'):
            # delete last char from input
            window['rooms'].update(values['rooms'][:-1])
        elif len(values['price']) and values['price'][-1] not in ('0123456789'):
            # delete last char from input
            window['price'].update(values['price'][:-1])
        elif event == 'Submit':
            doCalculate(
                window['area'].get(),
                window['floor'].get()[0],
                window['district'].get()[0],
                window['metroDistance'].get(),
                window['rooms'].get(),
                window['renovation'].get()[0],
                )

    window.close()
def doCalculate(area, floor, district, metroDist, rooms, renovation):
    print(area, floor, district, metroDist, rooms, renovation)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # generate_data()
    # analyze_data()
    create_UI()
    # table_example()