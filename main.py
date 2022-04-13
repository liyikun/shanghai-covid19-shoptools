import statistics
from typing import List
from excel import BaseExcel, BaseLine
from line import DataLine, StatisticLine, TitleLine, countLine
from utils import readFile


def main():
    list = readFile('require.txt')

    lines : List[BaseLine] = []

    title = TitleLine(list[0])

    title.addEnd('')

    lines.append(title)

    for i in range(1, len(list)):
        lineNode = DataLine(list[i], title.goodsNum, title.price)
        lineNode.addEnd()
        lines.append(lineNode)

    values = countLine(lines)

    statisticsLint = StatisticLine(values)
    statisticsLint.parse()
    
    lines.append(statisticsLint)

    excel = BaseExcel()
    excel.initExcel(lines)
    excel.outPutExcel()


main()