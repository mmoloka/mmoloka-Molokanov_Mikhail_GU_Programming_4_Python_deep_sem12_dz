import csv
import json

# Создайте класс студента.
# ○ Используя дескрипторы проверяйте ФИО на первую заглавную букву и наличие только букв.
# ○ Названия предметов должны загружаться из файла CSV при создании экземпляра. Другие предметы в экземпляре
# недопустимы.
# ○ Для каждого предмета можно хранить оценки (от 2 до 5) и результаты тестов (от 0 до 100).
# ○ Также экземпляр должен сообщать средний балл по тестам для каждого предмета и по оценкам всех предметов
# вместе взятых.


class CheckFullName:

    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        if not (value.isalpha() and value.istitle()):
            raise ValueError('Элемент ФИО должен начинаться с заглавной буквы и состоять только из букв')
        setattr(instance, self.param_name, value)

    def __str__(self):
        return f'{self.__get__(self.param_name)}'


class Student:

    first_name = CheckFullName()
    last_name = CheckFullName()
    patronymic = CheckFullName()

    def __init__(self, first_name, last_name, patronymic, csv_file, subject_grades_tests):
        subject_list = []
        subject_grades_dict = {}

        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic

        with open(csv_file, 'r', newline='') as f:
            csv_file = csv.reader(f)
            for line in csv_file:
                subject_list.append(line[0])
        for subject in subject_list:
            subject_grades_dict[subject] = subject_grades_tests[subject]
        self.grades_tests = subject_grades_dict

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.patronymic}\n' + \
            '\n'.join([
                (item[0] + ': ' +
                 'grade ' + str(item[1][0]) +
                 ' tests ' + str(item[1][1]) + ',' + str(item[1][2]) + ',' + str(item[1][3])) +
                ' average test rating ' + str(round((int(item[1][1]) + int(item[1][2]) + int(item[1][3])) / 3, 2))
                for item in self.grades_tests.items()]) + \
            f'\naverage grade {self.average_grade()}'

    def average_grade(self):
        sum_ = 0
        count = 0
        for item in self.grades_tests:
            sum_ += int(self.grades_tests[item][0])
            count += 1
        return round(sum_ / count, 2)


if __name__ == '__main__':
    with open('grades.json', 'r', encoding='utf-8') as f:
        json_file = json.load(f)
    std1 = Student("Ivanov", "Ivan", "Ivanovich", "subjects.csv", json_file["Ivanov Ivan Ivanovich"])
    std2 = Student("Petrov", "Petr", "Petrovich", "subjects.csv", json_file["Petrov Petr Petrovich"])
    print(std1)
    print()
    print(std2)
    # std3 = Student("ivanov", "Ivan", "Ivanovich", "subjects.csv", json_file["Ivanov Ivan Ivanovich"])
    std4 = Student("Petrov", "Petr", "Petrov123", "subjects.csv", json_file["Petrov Petr Petrovich"])
