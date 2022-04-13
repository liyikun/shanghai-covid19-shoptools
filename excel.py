from enum import Enum
from typing import List
from xlwt import Workbook


class Type(Enum):
  TEXT = 1
  VALUE = 2
  RESULT = 3

class BaseNode():
    type = Type.TEXT

    def getText(self) -> str:
        pass
    def getValue(self) -> int:
        return 0


class BaseLine:
    def getList(self) -> List[BaseNode]:
        pass

    def parse(self) -> None:
        pass

    def addEnd(self, text: str) -> None:
        pass



class BaseExcel:
    def __init__(self) -> None:
        self.workbook = Workbook(encoding="utf-8")
        self.sheet = self.workbook.add_sheet("free")

    def initExcel(self, lines: List[BaseLine]):
        for i in range(len(lines)):
            list = lines[i].getList()
            for j in range(len(list)):
                n = list[j]
                self.sheet.write(i, j, n.getText())

    def outPutExcel(self):
        self.workbook.save("./result.xlsx")
