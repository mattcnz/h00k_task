import datetime
from enum import Enum

# Define some operations
class Operations(Enum):
    EQ = '='
    IN = 'IN'
    NI = 'NOT IN'
    LT = '<'
    GT = '>'


# Define a base class for fields, and set up some id / url etc. based on that.
class Field:
    allowed_operations = []
    name = None


class IdField(Field):
    allowed_operations = [Operations.EQ, Operations.IN, Operations.NI, Operations.LT, Operations.GT]
    name = 'id'


class UrlField(Field):
    allowed_operations = [Operations.EQ]
    name = 'url'


class DateField(Field):
    allowed_operations = [Operations.EQ, Operations.LT, Operations.GT]
    name = 'date'


class RatingField(Field):
    allowed_operations = [Operations.EQ, Operations.LT, Operations.GT]
    name = 'rating'


# Define a base class for tables
class TableBase(object):
    def __init__(self):
        if hasattr(self, '_meta') and self._meta.get('table_name'):
            self.name = self._meta['table_name']
        else:
            self.name = self.__class__.__name__.lower()

    def all(self,):
        return Query(self)


# Define the review table
class Review(TableBase):
    id = IdField()
    url = UrlField()
    date = DateField()
    rating = RatingField()
    _meta = {"table_name": "review"}


# A condition defines a "X [OPERATION] Y" block
class Condition:
    """A condition has a field, an operator, and a value.
    For example: name = matt, id = 5, rating = 10
    """
    def __init__(self, field, operator, value):
        self.field = field
        self.operator = operator
        self.value = value
        self._check_valid_operations()

    def _check_valid_operations(self):
        if self.operator not in self.field.allowed_operations:
            raise ValueError(f'{self.operator} is not allowed for this field. Valid operations '
                             f'are {self.field.allowed_operations}')

    def to_str(self):
        if type(self.value) == str:
            return f'{self.field.name} {self.operator.value} \'{self.value}\''
        if type(self.value) == int:
            return f'{self.field.name} {self.operator.value} {self.value}'
        if type(self.value) == datetime.datetime:
            return f'{self.field.name} {self.operator.value} \'{self.value}\''
        return f'{self.field.name} {self.operator.value} {self.value}'


# A QueryConstructor takes in a list of conditions and builds a query string
class QueryConstructor:
    def __init__(self, table):
        self.table_name = table.name
        self.conditions: [Condition] = []

    def add_condition(self, condition):
        self.conditions.append(condition)

    def build_conditions_string(self):
        output = ''
        for index, condition in enumerate(self.conditions):
            if condition.operator.value == 'IN':
                condition.value = tuple(condition.value)
            if index != len(self.conditions) - 1:
                output += f' {condition.to_str()} AND'
            else:
                output += f' {condition.to_str()}'
        return output

    def build_query(self):
        query = f'SELECT * FROM {self.table_name}'
        if len(self.conditions):
            query += f' WHERE{self.build_conditions_string()}'
        return query


class Query:
    def __init__(self, table):
        self.query_builder = QueryConstructor(table)
        self.table = table

    def filter(self, field, operation, value):
        new_condition = Condition(field, operation, value)
        self.query_builder.add_condition(new_condition)
        return self

    def build_query(self):
        return self.query_builder.build_query()


print(
    Review().all()
    .filter(Review.rating, Operations.GT, 3)
    .filter(Review.rating, Operations.LT, 9)
    .filter(Review.rating, Operations.EQ, 'great')
    .filter(Review.id, Operations.IN, [998, 779, 1112])
    .filter(Review.id, Operations.EQ, 100)
    .filter(Review.date, Operations.LT, datetime.datetime.now())
    .build_query()
)

print(
    Review().all()
    .filter(Review.id, Operations.EQ, 1234512)
    .build_query()
)
