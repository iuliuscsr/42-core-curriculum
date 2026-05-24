/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_ops_reverse_rotate.c                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/20 01:39:16 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/24 23:32:59 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	ft_reverse_rotate(t_stack **stack)
{
	t_stack	*temp;

	if (!stack || !*stack || !(*stack)->next)
		return ;
	temp = *stack;
	while (temp->next)
		temp = temp->next;
	temp->prev->next = NULL;
	temp->prev = NULL;
	ft_stackadd_front(stack, temp);
}

void	rra(t_stack **stack_a, t_env *env)
{
	ft_reverse_rotate(stack_a);
	if (!env->bench)
		ft_putendl_fd("rra", 1);
	env->total_ops++;
	env->total_rra++;
}

void	rrb(t_stack **stack_b, t_env *env)
{
	ft_reverse_rotate(stack_b);
	if (!env->bench)
		ft_putendl_fd("rrb", 1);
	env->total_ops++;
	env->total_rrb++;
}

void	rrr(t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	ft_reverse_rotate(stack_a);
	ft_reverse_rotate(stack_b);
	if (!env->bench)
		ft_putendl_fd("rrr", 1);
	env->total_ops++;
	env->total_rrr++;
}
