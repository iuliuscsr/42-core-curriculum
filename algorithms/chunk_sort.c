/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   chunk_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jawosylu <jawosylu@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/24 11:29:35 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/27 11:09:16 by jawosylu         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	update_chunk(int *ch_mi, int *ch_ma, int chunk_size, int *pushed)
{
	*ch_mi = *ch_ma + 1;
	*ch_ma += chunk_size;
	*pushed = 0;
}

static int	ft_find_max_pos(t_stack *stack_b)
{
	t_stack	*temp;
	int		max_pos;
	int		max_val;
	int		pos;

	temp = stack_b;
	max_pos = 0;
	pos = 0;
	max_val = temp->index;
	while (temp)
	{
		if (temp->index > max_val)
		{
			max_val = temp->index;
			max_pos = pos;
		}
		temp = temp->next;
		pos++;
	}
	return (max_pos);
}

void	push_chunk_b(t_stack **stack_a, t_stack **stack_b,
			t_env *env, int chunk_size)
{
	int	chunk_min;
	int	chunk_max;
	int	ges;
	int	pushed_in_chunk;
	int	size;

	size = stack_size(stack_a);
	chunk_min = 0;
	chunk_max = chunk_size - 1;
	ges = 0;
	pushed_in_chunk = 0;
	while (ges < size)
	{
		if ((*stack_a)->index >= chunk_min && (*stack_a)->index <= chunk_max)
		{
			pb(stack_a, stack_b, env);
			ges++;
			pushed_in_chunk++;
			if (pushed_in_chunk == chunk_size)
				update_chunk(&chunk_min, &chunk_max, chunk_size,
					&pushed_in_chunk);
		}
		else
			ra(stack_a, env);
	}
}

static void	push_chunk_back_a(t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	int	max_pos;
	int	size;
	int	moves;

	while (*stack_b)
	{
		size = stack_size(stack_b);
		max_pos = ft_find_max_pos(*stack_b);
		if (max_pos <= size / 2)
		{
			while (max_pos--)
				rb(stack_b, env);
		}
		else
		{
			moves = size - max_pos;
			while (moves--)
				rrb(stack_b, env);
		}
		pa(stack_a, stack_b, env);
	}
}

void	chunk_sort(t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	int	chunk_size;
	int	total_numbers;

	set_medium(env);
	if (stack_size(stack_a) <= 5)
		return (selection_sort(stack_a, stack_b, env));
	total_numbers = stack_size(stack_a);
	chunk_size = 0;
	while ((chunk_size + 1) * (chunk_size + 1) <= total_numbers)
		chunk_size++;
	ft_normalize(*stack_a, total_numbers);
	push_chunk_b(stack_a, stack_b, env, chunk_size);
	push_chunk_back_a(stack_a, stack_b, env);
}
