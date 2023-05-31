import csv
import os

class CSVUtil:

    def __init__(self, filepath, itemNames):
        self.filepath = filepath

        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))

        if os.path.exists(filepath):
            print('CSV文件已存在，无需创建:', filepath)
            return

        csv_file = open(filepath, 'w', newline='', encoding='gbk')
        writer = csv.writer(csv_file)
        writer.writerow(itemNames)
        csv_file.close()

    def append(self, areaName, areaAll, houseCount, houseArea, otherArea):
        csv_file = open(self.filepath, 'a', newline='', encoding='gbk')
        writer = csv.writer(csv_file)
        writer.writerow([areaName, areaAll, houseCount, houseArea, otherArea])
        csv_file.close()

    def append(self, data):
        csv_file = open(self.filepath, 'a', newline='', encoding='gbk')
        writer = csv.writer(csv_file)
        writer.writerow(data)
        csv_file.close()


