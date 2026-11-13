from chatbot import answer_question


def main():
    while True:
        user_input = input("Votre question comptable (ou 'quit' pour fermer) : ")
        if user_input.lower() in {"quit", "exit", "q"}:
            print("Au revoir.")
            break
        print(answer_question(user_input))


if __name__ == "__main__":
    main()
