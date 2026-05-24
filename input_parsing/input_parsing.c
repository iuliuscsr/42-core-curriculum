/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input_parsing.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jawosylu <jawosylu@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/18 18:26:46 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/22 11:45:25 by jawosylu         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack	*get_input(int argc, char **argv, t_env *env)
{
	t_stack	*stack_a;
	char	*input;
	char	**split_str;
	int		wordindex;
	int		letterindex;

	stack_a = NULL;
	wordindex = check_flags(argc, argv, env);
	letterindex = 0;
	if (argc < 2)
		return (NULL);
	input = concenate_input(argc, argv);
	split_str = ft_split(input, ' ');
	free(input);
	if (!split_str)
		return (NULL);
	if (!check_input(split_str, wordindex, letterindex))
		return (free_split(split_str), NULL);
	stack_a = create_stack(split_str, wordindex, stack_a);
	if (!stack_a)
		return (free_split(split_str), NULL);
	if (!check_numbers(stack_a))
		return (ft_stackclear(&stack_a, del_int), free_split(split_str), NULL);
	free_split(split_str);
	return (stack_a);
}

char	*concenate_input(int argc, char **argv)
{
	char	*input;
	char	*temp;
	int		i;

	input = ft_strdup("");
	if (!input)
		return (NULL);
	i = 1;
	while (i < argc)
	{
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

	while (split_input[wordindex])
	{
		newnode = ft_stacknew(ft_atoi_modified(split_input[wordindex]));
		if (!newnode)
			return (NULL);
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
