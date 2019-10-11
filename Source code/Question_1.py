# Program to find the longest substring without repeating characters
string_input = input("Enter a string containing the word python: ")
list_string = list(string_input)

# print(list_string)

# initiate an empty list that will be used to get unique list
unique_string_list = []
for i in list_string:
    if i not in unique_string_list:
        unique_string_list.append(i)
print(''.join(unique_string_list))
