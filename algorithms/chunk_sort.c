/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   chunk_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/24 11:29:35 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/24 23:41:20 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"
#include <stdio.h>

int	index_min_min_in_stack(t_stack *stack_a, int min, int max)
{
	while (stack_a)
	{
		if (stack_a->index >= min && stack_a->index <= max)
			return (1);
		stack_a = stack_a->next;
	}
	return (0);
}

void	push_chunk_b(t_stack **stack_a, t_stack **stack_b, t_env *env, int	chunk_size)
{
	int	chunk_min;
	int	chunk_max;
	int size;

	size = stack_size(stack_a);
	chunk_min = 0;
	chunk_max = chunk_size - 1;

	while ((*stack_a) && index_min_min_in_stack(*stack_a, chunk_min, chunk_max))
	{
		if ((*stack_a)->index >= chunk_min && (*stack_a)->index <= chunk_max)
			pb(stack_a, stack_b, env);
		else
			ra(stack_a, env);
	}
	chunk_min+=chunk_size;
	chunk_max+=chunk_size;
}

void	chunk_sort(t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	int	chunk_size;
	int	total_numbers;

	total_numbers = stack_size(stack_a);
	chunk_size = 0;
	while ((chunk_size + 1) * (chunk_size + 1) <= total_numbers)
		chunk_size++;
	printf("%d\n", chunk_size);
	ft_normalize(*stack_a, stack_size(stack_a));
	t_stack *temp;
	temp = *stack_a;
	while (temp)
	{
		printf("Index: %d Wert: %d\n", temp->index, temp->content);
		temp = temp->next;
	}
	push_chunk_b(stack_a, stack_b, env, chunk_size);
}
