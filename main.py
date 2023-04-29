import os


class Quiz:
    def __init__(self, name, questions):
        self.name = name
        self.questions = questions

    def run_quiz(self):
        score = 0
        for question in self.questions:
            print(question.prompt)
            for i, option in enumerate(question.options):
                print(f"{i+1}. {option}")
            answer = input("Enter your answer: ")
            if answer.lower() == question.answer.lower():
                score += 1
        print("You got", score, "out of", len(self.questions),
              "questions correct")


class Question:
    def __init__(self, prompt, options, answer):
        self.prompt = prompt
        self.options = options
        self.answer = answer


def get_quizzes():
    quiz_files = [
        f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.txt')
    ]
    quizzes = []
    for file in quiz_files:
        name = file[:-4]
        questions = []
        with open(file, 'r') as f:
            lines = f.readlines()
            for i in range(0, len(lines) - len(lines) % 6, 6):
                prompt, *options, answer = map(str.strip, lines[i:i + 6])
                question = Question(prompt, options, answer)
                questions.append(question)
        quizzes.append(Quiz(name, questions))
    return quizzes


def print_quizzes(quizzes):
    print("Available quizzes:")
    for i, quiz in enumerate(quizzes):
        print(f"{i+1}. {quiz.name}")


def delete_quiz(quizzes):
    print_quizzes(quizzes)
    while True:
        try:
            quiz_index = int(
                input("Enter the number of the quiz you want to delete: ")) - 1
            if quiz_index < 0 or quiz_index >= len(quizzes):
                raise ValueError
            break
        except:
            print("Invalid input. Please try again.")
    quiz = quizzes[quiz_index]
    file_name = quiz.name + '.txt'
    os.remove(file_name)
    quizzes.remove(quiz)
    print(f"{quiz.name} deleted successfully.")


def load_quiz(quizzes):
    print_quizzes(quizzes)
    while True:
        try:
            quiz_index = int(
                input("Enter the number of the quiz you want to load: ")) - 1
            quiz = quizzes[quiz_index]
            break
        except:
            print("Invalid input. Please try again.")
    return quiz


def add_quiz():
    quiz_name = input("Enter the name for the new quiz: ")
    questions = []
    while True:
        prompt = input(
            "Enter the question prompt (or type 'exit' to finish adding questions): "
        )
        if prompt == 'exit':
            break
        options = []
        for i in range(4):
            option = input(f"Enter option {i+1}: ")
            options.append(option)
        answer = input("Enter the answer: ")
        question = Question(prompt, options, answer)
        questions.append(question)
    quiz = Quiz(quiz_name, questions)
    save_quiz(quiz)


def save_quiz(quiz):
    file_name = quiz.name + '.txt'
    with open(file_name, 'w') as f:
        for question in quiz.questions:
            f.write(question.prompt + '\n')
            for option in question.options:
                f.write(option + '\n')
            f.write(question.answer + '\n')


def edit_quizzes(quizzes):
    print_quizzes(quizzes)
    while True:
        try:
            quiz_index = int(
                input("Enter the number of the quiz you want to edit: ")) - 1
            quiz = quizzes[quiz_index]
            break
        except:
            print("Invalid input. Please try again.")
    # Prompt the user for new questions and options
    questions = []
    for question in quiz.questions:
        prompt = input(f"Enter new prompt for '{question.prompt}': ")
        options = []
        for i in range(4):
            option = input(f"Enter new option {i+1} for '{question.prompt}': ")
            options.append(option)
        answer = input(f"Enter new answer for '{question.prompt}': ")
        question = Question(prompt or question.prompt, options
                            or question.options, answer or question.answer)
        questions.append(question)
    quiz.questions = questions
    save_quiz(quiz)
    print("Quiz edited successfully.")


quizzes = get_quizzes()
while True:
    print("What do you want to do?")
    print("1. Load a quiz")
    print("2. Add a new quiz")
    print("3. Edit an existing quiz")
    print("4. Delete an existing quiz")
    print("5. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        if quizzes:
            quiz = load_quiz(quizzes)
            quiz.run_quiz()
        else:
            print("No quizzes found.")
    elif choice == '2':
        add_quiz()
        quizzes = get_quizzes()
    elif choice == '3':
        edit_quizzes(quizzes)
        quizzes = get_quizzes()
    elif choice == '4':
        delete_quiz(quizzes)
        quizzes = get_quizzes()
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please try again.")
