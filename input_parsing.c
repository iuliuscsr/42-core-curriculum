/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input_parsing.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/18 18:26:46 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/19 15:20:37 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack *get_input(int argc, char **argv)
{
	t_stack *stack_a;
	t_stack	*newnode;
	int		wordindex;
	int		letterindex;

	stack_a = NULL;
	wordindex = 1;
	letterindex = 0;
	if (argc < 2)
		return (NULL);
	if (!check_input(argv, wordindex, letterindex))
		return (NULL);
	while (argv[wordindex])
	{
		newnode = ft_stacknew(ft_atoi_modified(argv[wordindex]));
		if (!newnode)
			return (NULL);
		ft_stackadd_back(&stack_a, newnode);
		wordindex++;
	}
	if (!check_numbers(stack_a))
		return (NULL);
	return (stack_a);
}

int	check_input(char **argv, int i, int j)
{
	while (argv[i])
	{
		j = 0;
		while ((argv[i][j] == '-' || argv[i][j] == '+') && argv[i][j + 1] != '\0')
            	j++;
		while (argv[i][j])
		{
			if (!ft_isdigit(argv[i][j]))
				return (ft_putendl_fd("Error", 2), 0);
			j++;
		}
		i++;			
	}
	return (1);
}

int	check_numbers(t_stack *stack_a)
{
	t_stack *temp;
	t_stack *compare;
	
	temp = stack_a;
	while(temp)
	{
		compare = temp->next;
		while(compare)
		{
			if (temp->content == compare->content)
				return (ft_putendl_fd("Error", 2), 0);
			compare = compare->next;
		}
		temp = temp->next;
	}
	return (1);
}


