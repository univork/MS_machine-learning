"""სტუდენტის ქულების ვიზუალიზაცია (მათემატიკა, პროგრამირება, ინგლისური) განსხვავებული მარკერებითა და ფერებით.

განსაზღვრეთ სტუდენტის მონაცემების შესანახად შესაბამისი კოლექცია (სტუდენტის
სახელი გვარი, საგანი, შესაბამისი საგნის ქულები (მინიმუმ 4 ან 5 ქულა). მაგ:
Student("Alice", "Math", [85, 90, 78, 87]), განსაზღვრეთ რამოდენიმე სტუდენტი (მინიმუმ 3
სტუდენტი).

"""
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns


@dataclass
class ClassSet:
    math: list[int]
    programming: list[int]
    english: list[int]


class Student:
    def __init__(self, first_name: str, last_name: str, classes: ClassSet) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.classes: ClassSet = classes
    
    def __repr__(self) -> str:
        return f"Student({self.first_name}, {self.last_name}, {self.classes})"


students: list[Student] = [
    Student("Abraham", "Lincoln", ClassSet(math= [10, 10, 40, 40], programming=[8, 7, 20, 35], english= [10, 10, 38, 39])),
    Student("George", "Washington", ClassSet(math=[8, 7, 20, 29], programming=[5, 7, 22, 32], english=[6, 9, 32, 36])),
    Student("Thomas", "Jefferson", ClassSet(math=[10, 10, 40, 38], programming=[2, 4, 16, 25], english= [10, 10, 40, 37])),
]

# ახალი სტუდენტის დამატების.
def add_student() -> list[Student]:
    # students = students.copy()
    first_name = input("First name: ")
    last_name = input("Last name: ")

    math_grades = list(map(int, input("Math grades (seperated by comma): ").replace(" ", "").split(",")))
    programming_grades = list(map(int, input("Programming grades (seperated by comma): ").replace(" ", "").split(",")))
    english_grades = list(map(int, input("English grades (seperated by comma): ").replace(" ", "").split(",")))

    students.append(
        Student(
            first_name, 
            last_name, 
            ClassSet(math=math_grades, programming= programming_grades, english=english_grades)
        )
    )
    return students
    

# სტუდენტის წაშლის.
def delete_student(first_name: str, last_name: str) -> None:
    for i, student in enumerate(students):
        if student.first_name == first_name and student.last_name == last_name:
            students.pop(i)
            break
    else:
        print("Student Not Found")


# სტუდენტის მონაცემების რედაქტირების.
def update_student() -> list[Student]:
    # students = old_students.copy()

    name = input("Enter name: ")
    first_name, last_name = name.split(" ")

    for student in students:
        if student.first_name == first_name and student.last_name == last_name:
            subject = input("Subject to update: ")
            grades = list(map(int, input("Grades (seperated by comma): ").replace(" ", "").split(",")))
            student.classes.__setattr__(subject.lower(), grades)
            break
    else:
        print("Student Not Found")

    return students


# ააგეთ თითოეული საგნისთვის ქულების განაწილება ვიზუალიზაცია (სტუდენტების სახელებს მნიშვნელობა არ აქვს).
def grade_dist_for_all():
    grades = {
        "math": [],
        "programming": [],
        "english": []
    }

    for student in students:
        grades["math"].extend(student.classes.math)
        grades["programming"].extend(student.classes.programming)
        grades["english"].extend(student.classes.english)

    sns.displot(grades, kind="kde")
    plt.show()


# ააგეთ თითოეული სტუდენტის ქულების განაწილება სხვადასხვა საგნებში.
def grade_dist_for_each_student():
    for student in students:
        fig, axs = plt.subplots(1, 3, figsize=(16, 6))
        fig.suptitle(f"{student.first_name} {student.last_name} grades")

        sns.kdeplot(student.classes.math, ax=axs[0])
        axs[0].set_title("Math grades")


        sns.kdeplot(student.classes.programming, ax=axs[1])
        axs[1].set_title("Programming grades")

        sns.kdeplot(student.classes.english, ax=axs[2])
        axs[2].set_title("English grades")
        plt.show()


if __name__ == "__main__":
    add_student()
    delete_student("Abraham", "Lincoln")
    update_student()

    grade_dist_for_all()

    grade_dist_for_each_student()
