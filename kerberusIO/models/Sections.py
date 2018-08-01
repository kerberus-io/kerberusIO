import abc
from abc import ABC
from typing import Union
from kerberusIO.models.Enum.section_types import SectionType
from kerberusIO.utils.db.connection import DataBase


class Section(ABC):

    _db:        DataBase

    _id:        int = None
    _order:     int = None
    _name:      str
    _parent_id: int = None
    _type:      SectionType
    _sub_sec_a: int = None
    _sub_sec_b: int = None
    _file:      str = None

    def __init__(self, db: DataBase=None, args: dict=None):

        if db:
            self._db = db
        if args:
            if 'id' in args.keys():
                self._id = args['id']
            if 'order' in args.keys():
                self._order = args['order']
            if 'sub_sec_a' in args.keys():
                self._sub_sec_a = args['sub_sec_a']
            if 'sub_sec_b' in args.keys():
                self._sub_sec_b = args['sub_sec_b']
            if 'file' in args.keys():
                self._sub_sec_b = args['file']
            if 'parent' in args.keys():
                self._parent_id = args['parent']
        else:
            self._id = None
            self._order = None
            self._parent_id = None

    @abc.abstractmethod
    def save(self):
        pass

    def delete(self):
        del_qry = """
        DELETE FROM sections
          WHERE section_id = ?
        """
        self._db.execute_query(del_qry, (self.id,))

    def set_order(self, new_order: int):
        self._order = new_order

    @property
    def id(self):
        if self._id:
            return self._id
        else:
            return False

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return str(self._type.name).lower()

    @property
    def order(self):
        if self._order:
            return str(self._order)
        else:
            return False

    @property
    def parent(self):
        if self._parent_id:
            return self._parent_id
        else:
            return None

    def set_parent(self, parent_id: Union[int, str]=None):
        if isinstance(parent_id, str):
            parent_id = int(parent_id)

        self._parent_id = parent_id

    @property
    def file(self):
        return self._file


class Splash(Section):

    _headline:  str
    _copy:      str

    def __init__(self, name: str = None, headline: str = None, copy: str = None, args: dict = None, db: DataBase=None):
        super().__init__(db=db, args=args)
        self._type = SectionType.SPLASH

        if args:
            self._name = args['name']
            self._headline = args['headline']
            self._copy = args['copy']
        else:
            self._name = name
            self._headline = headline
            self._copy = copy

    def save(self):
        if self.id:
            args = (self.order, self.name, self._type.value, self.headline, self.ad_copy, self.parent, self.id)
            update_qry = """
            UPDATE sections
              SET sec_order = ?, name = ?, type = ?, headline = ?, copy = ?, parent = ?
              WHERE section_id = ?
            """
            self._db.execute_query(update_qry, args)
        else:
            args = (self.name, self._type.value, self.headline, self.ad_copy, self.parent,)
            new_qry = """
            INSERT INTO sections
              (name, type, headline, copy, parent)
              VALUES ( ?, ?, ?, ?, ?)
            """
            self_id = self._db.execute_query(new_qry, args)
            self._id = self_id

    def set_headline(self, headline: str):
        self._headline = headline

    def set_copy(self, copy: str):
        self._copy = copy

    @property
    def headline(self):
        return self._headline

    @property
    def ad_copy(self):
        return self._copy


class ListItem(Section):

    _title:     str
    _copy:      str

    def __init__(self, db: DataBase=None, args: dict=None, title: str=None, copy: str=None):
        super().__init__(db=db, args=args)
        self._type = SectionType.LIST_ITEM
        if args:
            self._title = args['headline']
            self._copy = args['copy']
        else:
            self._title = title
            self._copy = copy

    def save(self):
        if self.id:
            args = (self.order, self._type.value, self._title, self._copy, self._parent_id, self.id)
            save_qry = """
            UPDATE sections
              SET sec_order = ?, type = ?, headline = ?, copy = ?, parent = ? 
              WHERE section_id = ?
            """
            self._db.execute_query(save_qry, args)
        else:
            args = (self._type.value, self._title, self._copy, self._parent_id)

            save_qry = """
            INSERT INTO sections
              (type, headline, copy, parent)
              VALUES ( ?, ?, ?, ? )
            """
            self._db.execute_query(save_qry, args)

    @property
    def title(self):
        return self._title

    @property
    def copy(self):
        return self._copy


class List(Section):

    _items: [ListItem]

    def __init__(self, db: DataBase=None, args: dict=None, name: str=None, list_items: [ListItem]=list()):
        super().__init__(db=db, args=args)
        self._type = SectionType.LIST
        self._items = list_items

        if args:
            self._name = args['name']

            if 'id' in args.keys():
                self._get_items()
        else:
            self._name = name

    def save(self):
        for item in self._items:
            item.save()

        if self.id:
            args = (self.order, self.name, self._type.value, self.parent, self.id)
            save_qry = """
            UPDATE sections
              SET sec_order = ?, name = ?, type = ?, parent = ?
              WHERE section_id = ?
            """
            self._db.execute_query(save_qry, args)
        else:
            args = (self.name, self._type.value, self.parent)

            print("args in new List().save()")
            print(args)

            save_qry = """
            INSERT INTO sections
              (name, type, parent)
              VALUES ( ?, ?, ? )
            """
            self_id = self._db.execute_query(save_qry, args)
            self._id = self_id

    def delete(self):
        for item in self._items:
            item.delete()

        super().delete()

    @property
    def items(self):
        return self._items

    def add_item(self, item: ListItem):
        if item.order:
            # TODO: This needs a more robust solution to actually place in the proper order
            self._items.append(item)
        else:
            end_of_list = len(self._items)
            item.set_order(end_of_list)
            self._items.append(item)

    def _get_items(self):
        args = self.id,
        itm_qry = """
        SELECT * FROM sections
          WHERE parent = ?
        """
        rs = self._db.get_result_set(itm_qry, args)

        items = []

        if len(rs):
            for item in rs:
                args = {"id": item[0], "parent": self.id, "order": item[1], "headline": item[4], "copy": item[5]}
                i = section_factory(9, db=self._db, args=args)
                items.append(i)

        self._items = items


class Image(Section):

    _headline:  str = None
    _copy:      str = None

    def __init__(self, db: DataBase=None, args: dict=None, name: str=None, headline: str=None, copy: str=None, file: str=None):
        super().__init__(db=db, args=args)
        self._type = SectionType.IMAGE

        print(args)

        if args:
            self._name = args['name']
            self._headline = args['headline']
            self._copy = args['copy']
            self._file = args['file']
        else:
            self._name = name
            self._headline = headline
            self._copy = copy
            self._file = file

    def save(self):
        if self.id:
            args = (self.order, self.name, self._type.value, self.headline, self.ad_copy, self.parent, self.file, self.id)
            update_qry = """
            UPDATE sections
              SET sec_order = ?, name = ?, type = ?, headline = ?, copy = ?, parent = ?, filename = ?
              WHERE section_id = ?
            """
            self._db.execute_query(update_qry, args)
        else:
            args = (self.name, self._type.value, self.headline, self.ad_copy, self.file, self.parent,)
            new_qry = """
            INSERT INTO sections
              (name, type, headline, copy, filename, parent)
              VALUES ( ?, ?, ?, ?, ?, ?)
            """
            self_id = self._db.execute_query(new_qry, args)
            self._id = self_id

    @property
    def headline(self):
        return self._headline

    @property
    def ad_copy(self):
        return self._copy


class Cards(Section):

    def __init__(self, db: DataBase=None):
        super().__init__(db=db)
        self._type = SectionType.CARDS


class Icons(Section):

    def __init__(self, db: DataBase=None):
        super().__init__(db=db)
        self._type = SectionType.ICONS


class Text(Section):

    def __init__(self, db: DataBase=None):
        super().__init__(db=db)
        self._type = SectionType.TEXT


class VerticalSplit(Section):

    _left_section:  Section
    _right_section: Section

    def __init__(self, db: DataBase=None, name: str=None, args: dict=None):

        super().__init__(db=db, args=args)
        self._type = SectionType.VERTICAL_SPLIT

        if args:

            self._name = args['name']

            if args['left']:

                left = section_factory(db=db, sec_type=int(args['left']['type']), args=args['left'])
                left.save()
                self.add_left_section(left)
            else:
                left = section_factory(db=db, id=self._sub_sec_a)
                left.save()
                self.add_left_section(left)

            if args['right']:

                right = section_factory(db=db, sec_type=int(args['right']['type']), args=args['right'])
                right.save()
                self.add_right_section(right)
            else:
                right = section_factory(db=db, id=self._sub_sec_b)
                right.save()
                self.add_right_section(right)

        else:
            self._name = name

    @property
    def left(self):
        return self._left_section

    @property
    def right(self):
        return self._right_section

    def save(self):

        if self.id:
            pass
        else:
            args = (self.name, self._type.value, self._sub_sec_a, self._sub_sec_b)

            save_qry = """
            INSERT INTO sections
              (name, type, sub_sec_a, sub_sec_b) 
              VALUES ( ?, ?, ?, ? )
            """

            self_id = self._db.execute_query(save_qry, args)

            self._left_section.set_parent(self_id)
            self._right_section.set_parent(self_id)

            self._right_section.save()
            self._left_section.save()

    def add_left_section(self, sec: Section=None):
        self._sub_sec_a = sec.id
        self._left_section = sec

    def add_right_section(self, sec: Section=None):
        self._sub_sec_b = sec.id
        self._right_section = sec


class HorizontalSplit(Section):

    _top_section:       Section
    _bottom_section:    Section

    def __init__(self, db: DataBase=None):
        super().__init__(db=db)
        self._type = SectionType.HORIZONTAL_SPLIT

    @property
    def top(self):
        return self._top_section

    @property
    def bottom(self):
        return self._bottom_section

    def add_top_section(self, sec: Section=None):
        self._top_section = sec

    def add_bottom_section(self, sec: Section=None):
        self._bottom_section = sec


def section_factory(sec_type: Union[SectionType, int]=None, db: DataBase=None, db_rs: tuple=None, args: dict=None, id: int=None):

    if isinstance(sec_type, int):
        sec_type = SectionType(sec_type)

    if id:

        sec_qry = """
        SELECT * FROM sections
          WHERE section_id = ?
        """
        args = int(id),

        rs = db.get_result_set(sec_qry, args)[0]

        sf_args = {"name": rs[2], "type": rs[3], "headline": rs[4], "copy": rs[5],
                   "id": rs[0], "order": rs[1], "parent": rs[6]}

        return section_factory(sec_type=rs[3], db=db, args=sf_args)

    if db_rs:
        print("id db_rs in factory")
        print(db_rs)
        pass
    else:
        if sec_type == SectionType(1):  # Splash Screen
            if db:
                return Splash(db=db, args=args)
            else:
                pass
                return Splash()
        if sec_type == SectionType(2):  # List
            if db:

                return List(db=db, args=args)
            else:
                return List()
        if sec_type == SectionType(3):  # Image
            if db:
                return Image(db=db, args=args)
            else:
                return Image()
        if sec_type == SectionType(4):
            if db:
                return Cards(db=db)
            else:
                return Cards()
        if sec_type == SectionType(5):
            if db:
                return Cards(db=db)
            else:
                return Cards()
        if sec_type == SectionType(6):
            if db:
                return Text(db=db)
            else:
                return Text()
        if sec_type == SectionType(7):
            if db:

                base_args = {}
                left_args = {}
                right_args = {}

                for key in args.keys():
                    if '-a' in key:
                        left_args[key[:-2]] = args[key]
                    elif '-b' in key:
                        right_args[key[:-2]] = args[key]
                    else:
                        base_args[key] = args[key]

                base_args['left'] = left_args
                base_args['right'] = right_args

                print(base_args)

                return VerticalSplit(db=db, args=base_args)
            else:
                return VerticalSplit()
        if sec_type == SectionType(8):
            if db:
                return HorizontalSplit(db=db)
            else:
                return HorizontalSplit()

        if sec_type == SectionType(9):

            if db:
                return ListItem(db=db, args=args)
            else:
                return ListItem()

