import random
from matplotlib import pyplot as plt


attendance = ['Rare', 'Moderate', 'Frequent']
lecture_notes = ['Low', 'Medium', 'High']
lecture_quality = ['Awful', 'Almost Awful', 'So-So', 'Not Bad', 'Excellent']
output_rules = {
        'Rare': {
            'Low': 'Awful',
            'Medium': 'Almost Awful',
            'High': 'Almost Awful'
        },
        'Moderate': {
            'Low': 'So-So',
            'Medium': 'So-So',
            'High': 'Not Bad'
        },
        'Frequent': {
            'Low': 'Not Bad',
            'Medium': 'Not Bad',
            'High': 'Excellent'
        }
    }

def membership_function(x, y):
    attendance_dict = {elem: 0 for elem in attendance}
    lecture_notes_dict = {elem: 0 for elem in lecture_notes}

    if x <= 25:
        attendance_dict['Rare'] = 1
    elif x >= 75:
        attendance_dict['Frequent'] = 1
    elif 25 < x <= 50:
        attendance_dict['Rare'] = (50 - x) / 25
        attendance_dict['Moderate'] = (x - 25) / 25
    elif 50 < x < 75:
        attendance_dict['Frequent'] = (x - 50) / 25
        attendance_dict['Moderate'] = (75 - x) / 25

    if y <= 50:
        if y >= 25:
            lecture_notes_dict['Low'] = (50 - y) / 50
            lecture_notes_dict['Medium'] = (y - 25) / 25
        elif y < 25:
            lecture_notes_dict['Low'] = (50 - y) / 50
    elif y > 50:
        if y <= 75:
            lecture_notes_dict['High'] = (y - 50) / 50
            lecture_notes_dict['Medium'] = (75 - y) / 25
        elif y > 75:
            lecture_notes_dict['High'] = (y - 50) / 50
    print("Значення фунцій приналежності для лінгвістичної змінної \"Відвідуваність лекцій\": {0}\n"
          "Значення фунцій приналежності для лінгвістичної змінної \"Конспектування лекцій\": {1}".format(attendance_dict,
                                                                                           lecture_notes_dict))
    return attendance_dict, lecture_notes_dict


def rule_evaluation(x, y):
    rules_list = []
    att_memb_func_val, ln_memb_func_val = membership_function(x, y)
    for key, value in att_memb_func_val.items():
        for key_2, value_2 in ln_memb_func_val.items():
            if value != 0 and value_2 != 0:
                rules_list.append([(key, value), (key_2, value_2)])
    print("Приведення отриманих значень: ", *rules_list, sep='\n')
    return rules_list


def aggregation(x, y):
    min_rules = []
    input_rules = rule_evaluation(x, y)
    for rule in input_rules:
        min_rules.append([rule[0][0], rule[1][0], min(rule[0][1], rule[1][1])])
    print("Результат етапа агрегування: ", *min_rules, sep='\n')
    return min_rules


def accumulation(x, y):
    min_rules = aggregation(x, y)
    max_membership_value = -1
    result = []
    for rule in min_rules:
        if rule[2] > max_membership_value:
            max_membership_value = rule[2]
            result = rule
    print(f"Результат акумуляції: {result}")
    return result


def defuzzification(x, y):
    result = accumulation(x, y)

    juxtaposing = [output_rules[result[0]][result[1]], result[2]]
    if juxtaposing[0] == lecture_quality[0]:
        result = 25 - juxtaposing[1] * 25
    elif juxtaposing[0] == lecture_quality[1]:
        result = (juxtaposing[1] * 25 + (50 - 25 * juxtaposing[1])) / 2
    elif juxtaposing[0] == lecture_quality[2]:
        result = (juxtaposing[1] * 25 + 25 + (75 - 25 * juxtaposing[1])) / 2
    elif juxtaposing[0] == lecture_quality[3]:
        result = (juxtaposing[1] * 25 + 50 + (100 - 25 * juxtaposing[1])) / 2
    elif juxtaposing[0] == lecture_quality[4]:
        result = juxtaposing[1] * 25 + 75
    juxtaposing.append(result)
    return juxtaposing


def build_membership_plots():
    attendance_plot_points = {
        'Rare': {
            'X': [],
            'Y': []
        },
        'Moderate': {
            'X': [],
            'Y': []
        },
        'Frequent': {
            'X': [],
            'Y': []
        }
    }

    for x in range(0, 101):
        if x <= 25:
            attendance_plot_points['Rare']['X'].append(x)
            attendance_plot_points['Rare']['Y'].append(1)
        elif x >= 75:
            attendance_plot_points['Frequent']['X'].append(x)
            attendance_plot_points['Frequent']['Y'].append(1)
        elif 25 < x <= 50:
            attendance_plot_points['Rare']['X'].append(x)
            attendance_plot_points['Moderate']['X'].append(x)
            attendance_plot_points['Rare']['Y'].append((50 - x) / 25)
            attendance_plot_points['Moderate']['Y'].append((x - 25) / 25)
        elif 50 < x < 75:
            attendance_plot_points['Frequent']['X'].append(x)
            attendance_plot_points['Moderate']['X'].append(x)
            attendance_plot_points['Frequent']['Y'].append((x - 50) / 25)
            attendance_plot_points['Moderate']['Y'].append((75 - x) / 25)

    note_taking_plot_points = {
        'Low': {
            'X': [],
            'Y': []
        },
        'Medium': {
            'X': [],
            'Y': []
        },
        'High': {
            'X': [],
            'Y': []
        }
    }

    for x in range(0, 101):
        if x <= 50:
            if x >= 25:
                note_taking_plot_points['Low']['X'].append(x)
                note_taking_plot_points['Medium']['X'].append(x)
                note_taking_plot_points['Low']['Y'].append((50 - x) / 50)
                note_taking_plot_points['Medium']['Y'].append((x - 25) / 25)
            elif x < 25:
                note_taking_plot_points['Low']['X'].append(x)
                note_taking_plot_points['Low']['Y'].append((50 - x) / 50)
        elif x > 50:
            if x <= 75:
                note_taking_plot_points['High']['X'].append(x)
                note_taking_plot_points['Medium']['X'].append(x)
                note_taking_plot_points['High']['Y'].append((x - 50) / 50)
                note_taking_plot_points['Medium']['Y'].append((75 - x) / 25)
            elif x > 75:
                note_taking_plot_points['High']['X'].append(x)
                note_taking_plot_points['High']['Y'].append((x - 50) / 50)

    fig = plt.figure()

    ax_1 = fig.add_subplot(1, 3, 1)
    ax_2 = fig.add_subplot(1, 3, 2)

    ax_1.set(xlabel='Рівень відвідуваності',
             ylabel='Функція приналежності')
    ax_2.set(xlabel='Рівень конспектування',
             ylabel='Функция приналежності')

    ax_1.set(title='Відвідуваність лекцій')
    ax_2.set(title='Конспектування лекцій')

    ax_1.plot(attendance_plot_points['Rare']['X'],
              attendance_plot_points['Rare']['Y'],
              label="Rare", lw=5, color='#A60000')
    ax_1.plot(attendance_plot_points['Moderate']['X'],
              attendance_plot_points['Moderate']['Y'],
              label="Moderate", lw=5, color='#06266F')
    ax_1.plot(attendance_plot_points['Frequent']['X'],
              attendance_plot_points['Frequent']['Y'],
              label="Frequent", lw=5, color='#A6A600')

    ax_2.plot(note_taking_plot_points['Low']['X'],
              note_taking_plot_points['Low']['Y'],
              label="Rare", lw=5, color='#FFAA00')
    ax_2.plot(note_taking_plot_points['Medium']['X'],
              note_taking_plot_points['Medium']['Y'],
              label="Moderate", lw=5, color='#7109AA')
    ax_2.plot(note_taking_plot_points['High']['X'],
              note_taking_plot_points['High']['Y'],
              label="Frequent", lw=5, color='#00CC00')

    quality_plot_points = {
        'Awful': {
            'X': [],
            'Y': []
        },
        'Almost Awful': {
            'X': [],
            'Y': []
        },
        'So-So': {
            'X': [],
            'Y': []
        },
        'Not Bad': {
            'X': [],
            'Y': []
        },
        'Excellent': {
            'X': [],
            'Y': []
        }
    }

    for x in range(0, 101):
        if x <= 25:
            quality_plot_points['Awful']['X'].append(x)
            quality_plot_points['Almost Awful']['X'].append(x)
            quality_plot_points['Awful']['Y'].append((25 - x) / 25)
            quality_plot_points['Almost Awful']['Y'].append(x / 25)
        elif x > 75:
            quality_plot_points['Excellent']['X'].append(x)
            quality_plot_points['Not Bad']['X'].append(x)
            quality_plot_points['Excellent']['Y'].append((x - 75) / 25)
            quality_plot_points['Not Bad']['Y'].append((100 - x) / 25)
        elif 25 < x <= 50:
            quality_plot_points['Almost Awful']['X'].append(x)
            quality_plot_points['So-So']['X'].append(x)
            quality_plot_points['Almost Awful']['Y'].append((50 - x) / 25)
            quality_plot_points['So-So']['Y'].append((x - 25) / 25)
        elif 50 < x <= 75:
            quality_plot_points['So-So']['X'].append(x)
            quality_plot_points['Not Bad']['X'].append(x)
            quality_plot_points['So-So']['Y'].append((75 - x) / 25)
            quality_plot_points['Not Bad']['Y'].append((x - 50) / 25)

    ax_3 = fig.add_subplot(1, 3, 3)

    ax_3.plot(quality_plot_points['Awful']['X'],
              quality_plot_points['Awful']['Y'],
              label="Awful", lw=3, color='#FFDA00')
    ax_3.plot(quality_plot_points['Almost Awful']['X'],
              quality_plot_points['Almost Awful']['Y'],
              label="Almost Awful", lw=3, color='#FF4100')
    ax_3.plot(quality_plot_points['So-So']['X'],
              quality_plot_points['So-So']['Y'],
              label="So-So", lw=3, color='#00B25C')
    ax_3.plot(quality_plot_points['Not Bad']['X'],
              quality_plot_points['Not Bad']['Y'],
              label="Not Bad", lw=3, color='#00CC00')
    ax_3.plot(quality_plot_points['Excellent']['X'],
              quality_plot_points['Excellent']['Y'],
              label="Excellent", lw=3, color='#CD0074')

    ax_3.set(xlabel='Рівень конспектування',
             ylabel='Функція приналежності',
             title='Якість лекцій')

    plt.show()


def calculate(x, y):
    print('Відображення графіків функцій приналежності...')
    build_membership_plots()
    result = defuzzification(x, y);
    print('Значення вихідної логістичної змінної дорівнює: ', result)
    return result
