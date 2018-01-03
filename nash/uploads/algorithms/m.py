import openpyxl

def get_result(input_path, output_path):
    return xlsx_generate(input_path, output_path)


def xlsx_generate(input_path, output_path):
    import openpyxl

    wb = openpyxl.load_workbook(filename = input_path)
    sheet = wb['Worksheet']

    val = sheet['B4'].value
    sheet['B2'] = val

    wb.save(output_path)