/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_ops_swap.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/19 11:10:04 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/26 16:31:21 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	ft_swap(t_stack **stack)
{
	int		tmp;
	t_stack	*first;
	t_stack	*second;

	if (!stack || !*stack || !(*stack)->next)
		return ;
	first = *stack;
	second = first->next;
	tmp = second->content;
	second->content = first->content;
	first->content = tmp;
}

void	sa(t_stack **stack_a, t_env *env)
{
	ft_swap(stack_a);
	if (env->checker == 0 && env->print_operations == 1)
		ft_putendl_fd("sa", 1);
	env->total_ops++;
	env->total_sa++;
}

void	sb(t_stack **stack_b, t_env *env)
{
	ft_swap(stack_b);
	if (env->checker == 0 && env->print_operations == 1)
		ft_putendl_fd("sb", 1);
	env->total_ops++;
	env->total_sb++;
}

void	ss(t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	ft_swap(stack_a);
	ft_swap(stack_b);
	if (env->checker == 0 && env->print_operations == 1)
		ft_putendl_fd("ss", 1);
	env->total_ops++;
	env->total_ss++;
}
