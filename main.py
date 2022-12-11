
import PySimpleGUI as sg
from CalculatorQuality import calculate

def create_UI():
    data_cols_width = [5, 8, 35, 35]
    sg.theme('Dark Blue')
    layout = [[sg.Text('Відвідуваність лекцій (у відсотках):')], [sg.Input('', enable_events=True, key='attendance', )],
              [sg.Text('Рівень конспектування (у відсотках):')], [sg.Input('', enable_events=True, key='lectureNotes', )],
              [sg.Text('Результат якості лекцій')], [sg.Input('', enable_events=True, key='result', )],
              [sg.Button('Submit', visible=True, bind_return_key=True)],
              [sg.Button('Exit')],
            ]

    window = sg.Window('Якість лекцій', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if len(values['attendance']) and values['attendance'][-1] not in ('0123456789'):
            window['attendance'].update(values['attendance'][:-1])
        elif  len(values['lectureNotes']) and values['lectureNotes'][-1] not in ('0123456789'):
            window['lectureNotes'].update(values['lectureNotes'][:-1])
        elif event == 'Submit':
            quality = calculate(
                int(window['attendance'].get()),
                int(window['lectureNotes'].get())
            )
            window['result'].Update(quality)

    window.close()


if __name__ == '__main__':
    create_UI()