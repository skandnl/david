ft_list = ["Hello","tata!"]
ft_tuple = ("Hello","toto!")
ft_set = {"Hello","tutu!"}
ft_dict = {"Hello":"titi!"}

ft_list[1] = "World"
tmp = list(ft_tuple)
tmp[1] = "Korea!"
ft_tuple = tuple(tmp)
ft_set.remove("tutu!")
ft_set.add("Seoul!")
tmp2 = sorted(ft_set)
ft_set = tmp2
ft_dict["Hello"] = "codyssey!"

print(ft_list)
print(ft_tuple)
print(ft_set)
print(ft_dict)
