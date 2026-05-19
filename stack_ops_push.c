/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_ops_push.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/19 11:45:50 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/19 19:24:09 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	ft_push(t_stack **dst, t_stack **src)
{
	t_stack	*srcnode;

	srcnode = *src;
	if (!srcnode)
		return ;
	*src = (*src)->next;
	if (*src)
		(*src)->prev = NULL;
	srcnode->next = *dst;
	srcnode->prev = NULL;
	if (*dst)
		(*dst)->prev = srcnode;
	*dst = srcnode;
}

void	pa(t_stack **stack_a, t_stack **stack_b)
{
	ft_push(stack_a, stack_b);
	ft_putendl_fd("pa", 1);
}

void	pb(t_stack **stack_a, t_stack **stack_b)
{
	ft_push(stack_b, stack_a);
	ft_putendl_fd("pb", 1);
}
