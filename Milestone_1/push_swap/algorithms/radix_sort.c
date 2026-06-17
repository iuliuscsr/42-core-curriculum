/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   radix_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/24 22:52:40 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/27 05:53:22 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	max_bits(int max)
{
	long	i;
	int		bits;

	bits = 0;
	i = 1;
	if (max == 0)
		return (0);
	while (i <= (long)max)
	{
		i *= 2;
		bits++;
	}
	return (bits);
}

void	radix_sort(t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	int	i;
	int	j;
	int	size;

	set_complex(env);
	if (stack_size(stack_a) <= 5)
		return (selection_sort(stack_a, stack_b, env));
	size = stack_size(stack_a);
	ft_normalize(*stack_a, size);
	i = 0;
	while (i < max_bits(size))
	{
		j = 0;
		while (j < size)
		{
			if ((((*stack_a)->index >> i) & 1) == 0)
				pb(stack_a, stack_b, env);
			else
				ra(stack_a, env);
			j++;
		}
		while ((*stack_b))
			pa(stack_a, stack_b, env);
		i++;
	}
}
