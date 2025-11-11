import csv
import json
from statistics import mean, median

# comentarii generale
# cand vorbim de oop tinem minte cei 4 piloni:
# 1. incapsulare
# 2. mostenire
# 3. abstractizare
# 4. polimorfism

# in python exista o conventie cu privire la modul de definire al atributelor
# daca atributele sunt de forma self.attr => acest atribut este public
# daca atributele sunt de forma self._attr => acest atribut este protected
# daca atributele sunt de forma self.__attr => acest atribut este private

class DataSet:
    """Clasa de baza pentru gestiunea seturilor de date numerice"""

    # exemplu de dunder method - metoda precedata si urmata de 2 __
    # metoda __init__ este echivalentul unui constructor din alte limbaje de programare
    # self in python e echivalent cu this in Java
    def __init__(self, filename, data):
        self.filename = filename
        self._data = data


    # incapsulare: getters si setters
    def get_data(self):
        return self._data

    def set_data(self, new_data):
        self._data = [float(x) for x in new_data if DataSet._validate(x)]

    # metode statice
    # metodele statice (@staticmethod) sunt metode de uz general/utilitare care nu au legatura cu clasa, nici cu instanta curenta (self)
    # metodele clasei (@classmethod) sunt metode care nu depinde de instanta curenta (self), insa depind de clasa care le defineste

    @staticmethod
    def _validate(x):
        """Validam daca x poate fi convertit la tipul float"""
        try:
            float(x)
            return True
        # sau simplu Exception
        except (ValueError, TypeError):
            return False

    def describe(self):
        return {
            "name": self.filename,
            "count": len(self._data),
            "mean": mean(self._data) if self._data else None,
            "median": median(self._data) if self._data else None,
            "min": min(self._data) if self._data else None,
            "max": max(self._data) if self._data else None,
        }

    # metode ale instantelor
    def save_to_list(self):
        """Returneaza un obiect de tip Python list"""
        return self._data

    def save_to_json(self, path):
        """Salveaza data intr-un fisier json"""
        with open(path, "w") as f:
            json.dump(self._data, f)
        print(f"Date salvate in json {path}")

    def save_to_csv(self, path):
        """Salveaza data intr-un fisier csv"""
        with open(path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(self._data)
        print(f"Date salvate in csv {path}")

    # dunder methods (un fel de suprascriere)
    def __len__(self): # lungimea
        return len(self._data)

    def __repr__(self): # un fel de toString
        return f"DataSet(name={self.filename}, size={len(self._data)}"

    def __add__(self, other):
        if not isinstance(other, DataSet):
            raise TypeError("Putem aduna doar instante ale clasei DataSet")

        result = self._data + other._data

        return DataSet(f"{self.filename}_{other.filename}", result)

# inheritance

class CsvDataSet(DataSet): # aceasta sintaxa inseamna: clasa CsvDataSet mosteneste clasa DataSet
    """Opereaza cu date in format csv"""

    def __init__(self, path, name=None):
        self.path = path

        actual_name = name or path.split('/')[-1]
        data = self._load_csv(path)
        super().__init__(name, data)

    def _load_csv(self, path):
        data = []
        with open(path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                for value in row:
                    if self._validate(value):
                        data.append(float(value))
        return data

    def describe(self):
        common = super().describe()
        common['path'] = self.path
        common['type'] = 'csv'

        return common

class JSONDataSet(DataSet):
    """Opereaza cu date in format json"""

    def __init__(self, path, name=None):
        self.path = path

        actual_name = name or path.split('/')[-1]
        data = self._load_json(path)
        super().__init__(name, data)

    def _load_json(self, path):
        with open(path, "r") as f:
            continut = json.load(f)
        return [float(x) for x in continut if self._validate(x)]

    def describe(self):
        common = super().describe()
        common['path'] = self.path
        common['type'] = 'json'

        return common


# class methods
class DataSetFactory:
    """Clasa de tip factory (factory pattern) pentru constructia de dataset din surse diferite"""

    # tipuri recunoscute o sa fie un dictionar de forma:
    # {
    #   'csv': create_from_csv(),
    #   'json': create_from_json()
    _tipuri_recunoscute = {}

    @classmethod
    def register(cls, extensie, dataset_class):
        """Asociaza un handler (o implementare) pentru extensia de fisier"""
        cls._tipuri_recunoscute[extensie] = dataset_class

    @classmethod
    def from_list(cls, name, data):
        """Constructor simplu ce are la baza liste"""
        return DataSet(name, data)

    @classmethod
    def from_source(cls, path):
        for extensie, dataset_class in cls._tipuri_recunoscute.items():
            if path.endswith(extensie):
                return dataset_class(path)
        # daca ajungem la aceasta instructiune inseamna ca nu am gasit extensia din path in tipurile recunoscute si
        # vom folosi o metoda generica de parsare
        with open(path, 'r') as f:
            data = [float(x.strip()) for x in f.readlines()]

        return DataSet(path, data)

DataSetFactory.register('.csv', CsvDataSet)
DataSetFactory.register('.csv', JSONDataSet)


if __name__ == '__name__':
    data_set_1 = DataSetFactory.from_list('demo_1', [1,2,3,4,5])
    print(data_set_1.describe())

    data_set_csv = DataSetFactory.from_source('data.csv')
    data_set_json = DataSetFactory.from_source('data.json')

    print(data_set_csv.describe())
    print(data_set_json.describe())

    # combined
    combined = data_set_csv + data_set_json
    print(combined.describe())

    combined.save_to_csv('oop_csv.csv')
    combined.save_to_json('oop_json.json')

    # exemplificare polimorfism
    for data_set in [data_set_1, data_set_csv, data_set_json, combined]:
        print(f"{type(data_set)}: - mean: {data_set.describe()['mean']}")