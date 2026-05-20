/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   compute_disorder.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/20 15:52:57 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/20 17:00:26 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	check_mistakes(t_stack *stack_a)
{
	t_stack	*temp;
	t_stack	*temp2;
	int		nb;
	int		mistakes;

	mistakes = 0;
	temp2 = stack_a;
	while (temp2)
	{
		nb = temp2->content;
		temp = temp2->next;
		while (temp)
		{
			if (nb > temp->content)
				mistakes++;
			temp = temp->next;
		}
		temp2 = temp2->next;
	}
	return (mistakes);
}

int	compute_disorder(int mistakes, int size_stack_a)
{
	int	total_pairs;

	return (mistakes / total_pairs);
}
