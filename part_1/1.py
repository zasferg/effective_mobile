from typing import Optional, List


class ObjList:

    def __init__(self, data: str) -> None:
        self.__prev: Optional[ObjList] = None
        self.__next: Optional[ObjList] = None
        self.__data: str = data

    def get_prev(self) -> Optional["ObjList"]:
        return self.__prev

    def set_prev(self, obj: Optional["ObjList"]) -> None:
        self.__prev = obj

    def get_next(self) -> Optional["ObjList"]:
        return self.__next

    def set_next(self, obj: Optional["ObjList"]) -> None:
        self.__next = obj

    def get_data(self) -> str:
        return self.__data


class LinkedList:

    def __init__(self) -> None:
        self.head: Optional[ObjList] = None
        self.tail: Optional[ObjList] = None

    def add_obj(self, obj: ObjList) -> None:
        if self.head is None:
            self.head = obj
            self.tail = obj
        else:
            obj.set_prev(self.tail)
            if self.tail:
                self.tail.set_next(obj)
            self.tail = obj

    def remove_obj(self) -> None:
        if self.tail is None:
            return

        if self.tail == self.head:
            self.head = None
            self.tail = None
        else:
            ptr = self.tail.get_prev()
            if ptr:
                ptr.set_next(None)
            self.tail = ptr

    def get_data(self) -> List[str]:
        ptr = self.head
        data_list: List[str] = []
        while ptr is not None:
            data_list.append(ptr.get_data())
            ptr = ptr.get_next()
        return data_list


link_list = LinkedList()

link_list.add_obj(ObjList("data1"))
link_list.add_obj(ObjList("data2"))
link_list.add_obj(ObjList("data3"))

print(link_list.get_data())
