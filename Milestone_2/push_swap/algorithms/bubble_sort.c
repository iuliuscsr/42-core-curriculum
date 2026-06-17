/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bubble_sort.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/20 11:35:52 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/27 05:52:18 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	is_sorted(t_stack **stack)
{
	t_stack	*temp;

	temp = *stack;
	while (temp && temp->next)
	{
		if (temp->next->content < temp->content)
			return (0);
		temp = temp->next;
	}
	return (1);
}

int	stack_size(t_stack **stack)
{
	t_stack	*tmp;
	int		count;

	count = 0;
	tmp = *stack;
	while (tmp && tmp->next)
	{
		count++;
		tmp = tmp->next;
	}
	count++;
	return (count);
}

void	bubble_sort(t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	int	size;
	int	i;

	set_simple(env);
	if (stack_size(stack_a) <= 5)
		selection_sort(stack_a, stack_b, env);
	size = stack_size(stack_a);
	if (is_sorted(stack_a))
		return ;
	while (!is_sorted(stack_a))
	{
		i = 0;
		while (i < size - 1)
		{
			if ((*stack_a)->content > (*stack_a)->next->content)
				sa(stack_a, env);
			if (is_sorted(stack_a))
				return ;
			ra(stack_a, env);
			if (is_sorted(stack_a))
				return ;
			i++;
		}
		ra(stack_a, env);
	}
}
