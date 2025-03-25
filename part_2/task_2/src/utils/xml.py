import pandas





def group_to_list_generator(data:str, fname: str):
    data = pandas.read_excel(data,skipfooter=2)
    column_name = data.columns[1]
    row_index = data[data[column_name] == "Единица измерения: Метрическая тонна"].index

    if not row_index.empty:
            splitted_fname = fname.lstrip("result_ ").rstrip(".xlsx")
            start_index = row_index[0]
            filtered_data = data.iloc[start_index + 3:]
            filtered_data = filtered_data[filtered_data['Unnamed: 14']!= "-"]

            rows_as_lists = filtered_data.values.tolist()
            

            for item in rows_as_lists:
                yield item[1:] + [splitted_fname]
            









