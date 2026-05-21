/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   compute_disorder.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/20 15:52:57 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/21 11:26:54 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

double	compute_disorder(t_stack *stack_a)
{
	t_stack	*i;
	t_stack	*j;
	int		nb;
	double	mistakes;
	double	total_pairs;

	mistakes = 0;
	total_pairs = 0;
	i = stack_a;
	while (i)
	{
		nb = i->content;
		j = i->next;
		while (j)
		{
			if (nb > j->content)
				mistakes++;
			j = j->next;
			total_pairs++;
		}
		i = i->next;
	}
	if (total_pairs == 0)
		return (0);
	return (mistakes / total_pairs);
}
