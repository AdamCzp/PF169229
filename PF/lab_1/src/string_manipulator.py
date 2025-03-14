class StringManipulator:
    def reverse(self, string):
        return string[::-1]
    def capitalize(self, string):
        return string.capitalize()
    def count_words(self, string):
        string = string.split()
        return len(string)
string_manipulator = StringManipulator()
print(string_manipulator.capitalize("ahello"))
