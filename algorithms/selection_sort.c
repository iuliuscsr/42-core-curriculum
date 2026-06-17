/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   selection_sort.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/21 14:24:41 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/27 05:30:33 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	three_elements(t_stack **stack_a, t_env *env)
{
	int		one;
	int		two;
	int		three;

	ft_normalize(*stack_a, stack_size(stack_a));
	one = (*stack_a)->index;
	two = (*stack_a)->next->index;
	three = (*stack_a)->next->next->index;
	if (is_sorted(stack_a))
		return ;
	else if (one > two && one > three)
		ra(stack_a, env);
	if (is_sorted(stack_a))
		return ;
	one = (*stack_a)->index;
	two = (*stack_a)->next->index;
	three = (*stack_a)->next->next->index;
	if (two > one && two > three)
		rra(stack_a, env);
	if (is_sorted(stack_a))
		return ;
	sa(stack_a, env);
}

static int	find_min(t_stack *temp)
{
	int	i;
	int	j;
	int	min;

	i = 1;
	j = 1;
	min = temp->content;
	while (temp->next)
	{
		i++;
		if (temp->next->content < min)
		{
			min = temp->next->content;
			j = i;
		}
		temp = temp->next;
	}
	return (j);
}

void	selection_sort(t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	int		i;

	if (stack_size(stack_a) == 2)
		sa(stack_a, env);
	else if (stack_size(stack_a) == 3)
		three_elements(stack_a, env);
	else
	{
		while ((stack_size(stack_a) > 3))
		{
			i = find_min(*stack_a);
			if (i <= stack_size(stack_a) / 2 + 1)
				while (i-- > 1)
					ra(stack_a, env);
			else
				while (i++ <= stack_size(stack_a))
					rra(stack_a, env);
			pb(stack_a, stack_b, env);
		}
		three_elements(stack_a, env);
	}
	while ((*stack_b))
		pa(stack_a, stack_b, env);
}
