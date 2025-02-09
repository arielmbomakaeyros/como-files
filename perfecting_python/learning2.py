newvariable="hello world"
print(newvariable)
newvariable="you said what"
print(newvariable)
name = "We are here for you"
print(name.title())
print(name.upper())
print(name.lower())

gather_all = f"{newvariable.upper()} {name.title()}"
print(gather_all)
print(gather_all.upper())
our_parents = "our parents"
action_parents = "Left Us"
discussion = "without heritage"

our_parent_result = f"Let me tell you something \n{our_parents.title()} you uncles, \n{action_parents.lower()} \n{discussion.upper()}"
print(f"My point: \n{our_parent_result.upper()}. \n{our_parent_result}")

# STRIPPING WHITE SPACE
white_space_var = " hello  i am here "
# print(white_space_var.rstrip()) 
# print(white_space_var.lstrip())
print(white_space_var.strip())

nostarch_url = 'https://nostarch.com'
print(nostarch_url.removeprefix("https://"))
print(nostarch_url.removesuffix(".com").removeprefix("https://"))

# exercise
vially_name= "Vially"
quote='“A person who never made a mistake never tried anything new.”'
my_son_age = 2**2
my_son_name = "godwin"
print(f'{ vially_name } once said, { quote.title() }. \nMy son is called { my_son_name.title() }. \nHe is aged { my_son_age }')

first_list = ['trek', 'cannondale', 'redline', 'specialized']
print(first_list[-1])
print(first_list[-2])
print(first_list[-3])

first_list.insert(10, "hello")
print(first_list)
print(first_list[-1])

motorcycles = ['honda', 'yamaha', 'suzuki']
print (motorcycles)

def delete_element (param): 
    del motorcycles[param]

# del(motorcycles[2])
delete_element(1)
print(motorcycles)

motorcycles.insert(0, "lamborghini")
print(motorcycles)

motorcycles.append("Nestor ford")
print(motorcycles)

# EXERCISE

my_people = ["betyna", "marie", "yvana"]
print(my_people)

# 1-) who is the last person
print(my_people[-1])
# 2-) Complet the name of that last person
last_person_complete_name = f"jennifer {my_people[-1]}"
print(last_person_complete_name)
# 3-) add that complete last person's name to the list
my_people.remove(my_people[-1])
print(my_people)
my_people.append(last_person_complete_name)

print(my_people)

# 4-) Invite people
print(f"I solemnly invite you to have a wonderful dinner with me {my_people[0].title()}")
print(f"I solemnly invite you to have a wonderful dinner with me {my_people[1].title()}")
print(f"I solemnly invite you to have a wonderful dinner with me {my_people[-1].title()}")

# 5-) Marie is not coming replace her with severine
print(f"Unfortunately {my_people[1].title()} will not be able to make it to the invitation.")

del my_people[1]
my_people.insert(1, "Severine")

print(my_people)
# 6-) send another bunch of invitation
print(f"I solemnly invite you to have a wonderful dinner with me {my_people[0].title()}")
print(f"I solemnly invite you to have a wonderful dinner with me {my_people[1].title()}")
print(f"I solemnly invite you to have a wonderful dinner with me {my_people[-1].title()}")


# 7-) We got a bigger table let us invite more poeple:
print(my_people)
my_people.insert(0, "Vanina")
my_people.insert(2, "Marina")
my_people.append("Wendi")

print(my_people)
for someone in my_people:
    print(f"I solemnly invite you to have a wonderful dinner with me {someone.title()}")


print("Hello guy i can only invite 2 people i got only 2 sits")