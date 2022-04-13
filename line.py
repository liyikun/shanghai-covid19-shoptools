from typing import Dict, List
from excel import BaseLine, BaseNode, Type
from utils import isDataEnd, isDataStart, isInfoEnd, isInfoStart


class TextNode(BaseNode):
    def __init__(self, text: str) -> None:
        self.text = text

    def getText(self) -> str:
        return self.text


class ResultNode(BaseNode):
    type = Type.RESULT
    def __init__(self, text: str) -> None:
        self.text = text

    def getText(self) -> str:
        return self.text



class ValueNode(BaseNode):
    type = Type.VALUE
    def __init__(self, count: str, value: str) -> None:
        super().__init__()
        self.count = count
        self.value = value

    def getText(self) -> str:
        return self.count

    def getValue(self) -> str:
        return int(self.count) * int(self.value)


class TitleLine(BaseLine):
    nodes: List[BaseNode] = []
    price: Dict[str, str] = {}

    def __init__(self, source: str) -> None:
        super().__init__()
        self.source = source
        self.parse()

    def parse(self):
        text = self.source
        texts = []

        value = ''
        goodsIndex = 1
        infoIndex = 1

        # parse text
        for i in text:
            if isInfoStart(i):
                value = ''
            elif isInfoEnd(i):
                texts.append(value)
                infoIndex += 1
                value = ''
            elif isDataStart(i):
                value = ''
            elif isDataEnd(i):
                [name, v] = value.split(":")
                texts.append(name)
                self.price[str(goodsIndex)] = v
                goodsIndex += 1
                value = ''
            else:
                value += i

        self.nodes = list(map(lambda x: TextNode(x), texts))
        self.goodsNum = goodsIndex
        self.infoIndex = infoIndex

    def addEnd(self, text: str) -> None:
        self.nodes.append(TextNode(text))

    def getList(self) -> List[BaseNode]:
        return self.nodes


class DataLine(BaseLine):
    nodes: List[BaseNode] = []

    def __init__(self, source: str, goodsNum: int, price: Dict[str, str]) -> None:
        super().__init__()
        self.source = source
        self.goodsNum = goodsNum
        self.price = price
        self.parse()

    def parse(self):
        text = self.source
        goods: Dict[str, str] = {}
        nodes: List[BaseNode] = []
        value = ''

        # parse text
        for i in text:
            if isInfoStart(i):
                value = ''
            elif isInfoEnd(i):
                nodes.append(TextNode(value))
                value = ''
            elif isDataStart(i):
                value = ''
            elif isDataEnd(i):
                [id, value] = value.split("*")
                goods[id] = value
                value = ''
            else:
                value += i

        for i in range(1, self.goodsNum):
            c = goods.get(str(i))
            if c:
                v = self.price[str(c)]
                nodes.append(ValueNode(str(c), str(v)))
            else:
                nodes.append(ValueNode('0', '0'))

        self.nodes = nodes

    def addEnd(self) -> None:
        v = 0

        for i in self.nodes:
            v += i.getValue()

        self.nodes.append(ResultNode(str(v)))

    def getList(self) -> List[BaseNode]:
        return self.nodes


class StatisticLine(BaseLine):
    nodes: List[BaseNode] = []

    def __init__(self, values: List[int]) -> None:
        super().__init__()
        self.values = values
        self.parse()

    def parse(self):
        nodes: List[BaseNode] = []
        for i in self.values:
            nodes.append(ResultNode(str(i)))
        self.nodes = nodes

    def addEnd(self, text: str) -> None:
        self.nodes.append(ResultNode(str(text)))

    def getList(self) -> List[BaseNode]:
        return self.nodes


def countLine(ls: List[BaseLine]):
    values = []

    lenLength = len(ls[0].getList())

    for index in range(lenLength):
        v = 0
        for l in ls:
            list = l.getList()
            node = list[index]
            
            if node.type == Type.VALUE:
                v += int(node.getText())
            elif node.type == Type.RESULT:
                v += int(node.getText())

        values.append(v)

    return values
