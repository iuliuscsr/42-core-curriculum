/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input_parsing.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/18 18:26:46 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/27 05:57:11 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"
#include <stdio.h>

t_stack	*get_input(int argc, char **argv, t_env *env)
{
	t_stack	*stack_a;
	char	*input;
	char	**split_str;
	int		wordindex;

	stack_a = NULL;
	if (argc < 2)
		return (NULL);
	wordindex = check_flags(argc, argv, env);
	input = concenate_input(argc, argv, wordindex);
	if (!input)
		return (NULL);
	split_str = ft_split(input, ' ');
	if (!split_str)
		return (free(input), NULL);
	if (!check_input(split_str, 0, 0))
		return (free(input), free_split(split_str), NULL);
	stack_a = create_stack(split_str, 0, stack_a);
	if (!stack_a)
		return (free_split(split_str), free(input), NULL);
	if (!check_numbers(stack_a))
		return (ft_stackclear(&stack_a, del_int),
			free_split(split_str), free(input), NULL);
	return (free(input), free_split(split_str), stack_a);
}

char	*concenate_input(int argc, char **argv, int wordindex)
{
	char	*input;
	char	*temp;
	int		i;

	input = ft_strdup("");
	if (!input)
		return (NULL);
	i = wordindex;
	while (i < argc)
	{
		if (argv[i][0] == '\0' || argv[i][0] == 32)
			return (ft_putendl_fd("Error", 2), free(input), NULL);
		temp = input;
		input = ft_strjoin(input, argv[i]);
		free(temp);
		if (!input)
			return (NULL);
		temp = input;
		input = ft_strjoin(input, " ");
		free(temp);
		if (!input)
			return (NULL);
		i++;
	}
	return (input);
}

t_stack	*create_stack(char **split_input, int wordindex, t_stack *stack_a)
{
	t_stack	*newnode;
	long	number;

	while (split_input[wordindex])
	{
		number = ft_atoi_modified(split_input[wordindex]);
		if (number > INT_MAX || number < INT_MIN)
		{
			ft_putendl_fd("Error", 2);
			ft_stackclear(&stack_a, del_int);
			return (NULL);
		}
		newnode = ft_stacknew(number);
		if (!newnode)
			return (ft_stackclear(&stack_a, del_int), NULL);
		ft_stackadd_back(&stack_a, newnode);
		wordindex++;
	}
	return (stack_a);
}

int	check_input(char **argv, int i, int j)
{
	while (argv[i])
	{
		j = 0;
		while ((argv[i][j] == '-' || argv[i][j] == '+')
		&& argv[i][j + 1] != '\0')
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
	t_stack	*temp;
	t_stack	*compare;

	temp = stack_a;
	while (temp)
	{
		compare = temp->next;
		while (compare)
		{
			if (temp->content == compare->content)
				return (ft_putendl_fd("Error", 2), 0);
			compare = compare->next;
		}
		temp = temp->next;
	}
	return (1);
}
