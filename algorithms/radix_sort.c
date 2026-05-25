/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   radix_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/24 22:52:40 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/25 03:41:49 by jmalsam          ###   ########.fr       */
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

void	radix_sort(t_strg *config, t_env *env)
{
	int	i;
	int	j;
	int	size;

	ft_normalize(config->stack_a, config->size_stack_a);
	size = config->size_stack_a;
	i = 0;
	while (i < max_bits(config->size_stack_a))
	{
		j = 0;
		while (j < size)
		{
			if (((config->stack_a->index >> i) & 1) == 0)
				pb(&config->stack_a, &config->stack_b, env);
			else
				ra(&config->stack_a, env);
			j++;
		}
		while (config->stack_b)
			pa(&config->stack_a, &config->stack_b, env);
		i++;
	}
}
