import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('settings.conf')
uploads = config.get('General', 'UPLOAD_FOLDER')


def get_csv(path, filters, sort_columns, file_ext):
    msg = False
    file_error = False
    if file_ext == 'csv':
        data = pd.read_csv(path, encoding='Windows-1251')
    elif file_ext == 'xlsx':
        data = pd.read_excel(path)
    elif file_ext == 'txt':
        with open(path, 'r') as f:
            data = f.readlines()
    else:
        file_error = True
        data = None
    if file_error == False:
        from_found = len(data)
        found_data = None
        try:
            if filters:
                filters_list = filters.split(',')
                combined_condition = None  # Инициализация финального условия

                for filter_part in filters_list:
                    column, value = filter_part.split(':')
                    if column in data.columns:
                        value_type = data[column].dtype
                        if value_type == int:
                            value = int(value)
                        elif value_type == float:
                            value = float(value)

                        # Создание логической Series для текущего условия
                    condition = data[column] == value

                    # Объединение с предыдущим условием
                    if combined_condition is None:
                        combined_condition = condition
                    else:
                        combined_condition &= condition

                # Фильтрация данных
                data = data[combined_condition]
                found = len(data)
                found_data = f'Найдено {found} совпадений из {from_found}'
            if sort_columns:
                data = data.sort_values(by=sort_columns)
        except Exception as e:
            print(e)


    else:
        data = None
        found_data = None
    return data, msg, found_data, file_error
