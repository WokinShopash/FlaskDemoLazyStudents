import random
import string


class Student:
    def __init__(self, name, creativity):
        self.name = name
        self.creativity = creativity

    def get_idea(self):
        if random.random() < self.creativity:
            return ''.join(random.choice(string.ascii_lowercase+" ") for _ in range(100))
        else:
            return None


class Group:
    def __init__(self):
        self._students = []

    def add_student(self, name):
        self._students.append(Student(name, random.random()))

    def free(self, i):
        if i >= self.count():
            raise ValueError('Incorrect ID')
        del self._students[i]

    def count(self):
        return len(self._students)

    def get_ideas(self):
        ideas = []

        for i, student in enumerate(self._students):
            idea = student.get_idea()

            if idea is not None:
                ideas.append({
                    'id': i,
                    'name': student.name,
                    'text': idea
                })

        return ideas
