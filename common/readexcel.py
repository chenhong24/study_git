import openpyxl


class ReadExcel(object):
    def __init__(self, file_name, sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name

    def open(self):
        self.wb = openpyxl.load_workbook(self.file_name)
        self.sh = self.wb[self.sheet_name]

    def read_data(self):
        self.open()
        datas = list(self.sh.rows)
        title = [i.value for i in datas[0]]
        cases = []
        for i in datas[1:]:
            values = [c.value for c in i]
            case = dict(zip(title, values))
            cases.append(case)
        return cases

    def write_data(self, row, column, value):
        self.open()
        self.sh.cell(row=row, column=column, value=value)
        self.wb.save(self.file_name)
