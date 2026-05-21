/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   control_struct.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/20 16:09:33 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/22 00:23:45 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_strg	*init_control(t_stack *stack_a, t_stack *stack_b)
{
	int		i;
	t_stack	*temp;
	t_strg	*control;

	control = malloc(sizeof(t_strg));
	if (!control)
		return (NULL);
	control->stack_a = stack_a;
	temp = stack_a;
	i = 0;
	while (temp)
	{
		temp = temp->next;
		i++;
	}
	control->size_stack_a = i;
	control->stack_b = stack_b;
	control->size_stack_b = 0;
	return (control);
}
