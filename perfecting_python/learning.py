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
print(white_space_var.rstrip())

