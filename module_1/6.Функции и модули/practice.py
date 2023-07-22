import random

ROCK = "к"
SCISSORS = "н"
PAPER = "б"


def get_user_choice():
	while True:
		choice = input("Выберите: камень, ножницы или бумага: ").lower()
		if choice in [ROCK, SCISSORS, PAPER]:
			return choice
		else:
			print("Некорректный ввод. Попробуйте еще раз.")


def get_computer_choice():
	choices = [ROCK, SCISSORS, PAPER]
	return random.choice(choices)


def determine_winner(user_choice, computer_choice):
	if user_choice == computer_choice:
		return "Ничья!"
	elif (
			(user_choice == ROCK and computer_choice == SCISSORS) or
			(user_choice == SCISSORS and computer_choice == PAPER) or
			(user_choice == PAPER and computer_choice == ROCK)
	):
		return "Вы выиграли!"
	else:
		return "Компьютер выиграл!"


def play_game():
	print("Игра 'Камень, ножницы, бумага'")

	while True:
		user_choice = get_user_choice()
		computer_choice = get_computer_choice()

		print(f"Ваш выбор: {user_choice}")
		print(f"Выбор компьютера: {computer_choice}")

		winner = determine_winner(user_choice, computer_choice)
		print(winner)

		play_again = input("Хотите сыграть еще раз? (да/нет): ").lower()
		if play_again != "да":
			break

	print("Спасибо за игру!")


play_game()
