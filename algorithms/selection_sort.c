/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   selection_sort.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/21 14:24:41 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/22 00:47:35 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	find_min(t_stack *temp)
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

void	selection_sort(t_strg *config)
{
	t_stack	*temp;
	int		i;
	int		j;

	while (config->stack_a)
	{
		temp = config->stack_a;
		j = find_min(temp);
		i = 1;
		while (i < j)
		{
			ra(&config->stack_a);
			i++;
		}
		pb(&config->stack_a, &config->stack_b);
	}
	while (config->stack_b)
		pa(&config->stack_a, &config->stack_b);
}
