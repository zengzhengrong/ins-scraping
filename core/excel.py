from openpyxl import Workbook


class Excel:
    
    wb = Workbook()
    
    # ws = wb.active
    def __init__(self,data):
        self.args = data
        
    def export(self,dest_filename=None):
        self.dest_filename = dest_filename
        items_dict = self.args
        items_count = len(items_dict)
        items = items_dict.items()

        for index , kw in enumerate(items):
            key , values = kw
            title = values.get('title',key)
            if index == 0:
                ws = self.wb.active
                ws.title = title
            else:
                ws = self.wb.create_sheet(title=title)
            dest_filename = values.get('dest_filename',f'{key}.xlsx')
            fields = values.get('fields','')
            data = values.get('data','')
            ws.append(fields)
            for row in data:
                ws.append(row)
        if self.dest_filename:
            dest_filename = self.dest_filename
        self.wb.save(filename=dest_filename)