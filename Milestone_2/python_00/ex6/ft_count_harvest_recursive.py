def ft_harvest_helper(days):
    if days <= 0:
        return
    ft_harvest_helper(days - 1)
    print("Day", days)


def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))
    ft_harvest_helper(days)
    print("Harvest time!")
