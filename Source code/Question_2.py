input_list = [('John', ('Physics', 80)),
              ('Daniel', ('Science', 90)),
              ('John', ('Science', 95)),
              ('Mark', ('Maths', 100)),
              ('Daniel', ('History', 75)),
              ('Mark', ('Social', 95))]

# Sort the list items
new_list = sorted(input_list)
print(new_list)

# initiate empty dictionary that we'll add end results to
unique_list = {}

for i in new_list:
    if i[0] in unique_list:
        unique_list[i[0]].append(i[1])
    else:
        unique_list[i[0]] = [i[1]]
print(unique_list)
