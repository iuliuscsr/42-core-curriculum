/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_ops_rotate.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/19 14:37:48 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/24 23:33:24 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	ft_rotate(t_stack **stack)
{
	t_stack	*temp;

	if (!stack || !*stack || !(*stack)->next)
		return ;
	temp = *stack;
	*stack = (*stack)->next;
	if (*stack)
		(*stack)->prev = NULL;
	temp->next = NULL;
	ft_stackadd_back(stack, temp);
}

void	ra(t_stack **stack_a, t_env *env)
{
	ft_rotate(stack_a);
	if (!env->bench)
		ft_putendl_fd("ra", 1);
	env->total_ops++;
	env->total_ra++;
}

void	rb(t_stack **stack_b, t_env *env)
{
	ft_rotate(stack_b);
	if (!env->bench)
		ft_putendl_fd("rb", 1);
	env->total_ops++;
	env->total_rb++;
}

void	rr(t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	ft_rotate(stack_a);
	ft_rotate(stack_b);
	if (!env->bench)
		ft_putendl_fd("rr", 1);
	env->total_ops++;
	env->total_rr++;
}
