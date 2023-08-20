class Student():
	have_textbook = False
	def learn_math(self):
		if self.have_textbook is True:
			return 5
		return 2

s = Student()
s.have_textbook = True
print(s.learn_math())
