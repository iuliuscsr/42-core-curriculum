/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   control_struct.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/20 16:09:33 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/20 16:37:22 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_strg	*init_control(t_strg *control, t_stack *stack_a, t_stack *stack_b)
{
	int		i;
	t_stack	*temp;

	if (!control)
		return (NULL);
	temp = stack_a;
	control->stack_a = temp;
	i = 0;
	while (temp)
	{
		temp = temp->next;
		i++;
	}
	control->size_stack_a = i;
	temp = stack_b;
	control->stack_b = temp;
	i = 0;
	while (temp)
	{
		temp = temp->next;
		i++;
	}
	control->size_stack_b = i;
	return (control);
}
