class Student:
    def __init__(self, name, group, grades):
        self.name = name
        self.group = group
        self.grades = [int(grade) for grade in grades]
    
    def average_grade(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0
    
    def is_excellent(self):
        return self.average_grade() >= 4.5

students = []
with open('students.txt', 'r', encoding='utf-8') as file:
    for line in file:
        if line.strip():
            parts = line.strip().split(';')
            if len(parts) >= 3:
                name = parts[0]
                group = parts[1]
                grades = parts[2].split(',')
                students.append(Student(name, group, grades))

with open('excellent_students.txt', 'w', encoding='utf-8') as file:
    for student in students:
        if student.is_excellent():
            file.write(f"{student.name} - {student.group}\n")

group_averages = {}
for student in students:
    if student.group not in group_averages:
        group_averages[student.group] = []
    group_averages[student.group].append(student.average_grade())

print("средний балл по группам:")
for group, grades in group_averages.items():
    avg = sum(grades) / len(grades)
    print(f"группа {group}: {avg:.2f}")