/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker_bonus_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jawosylu <jawosylu@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 10:16:20 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/27 15:15:12 by jawosylu         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker_bonus.h"

int	c_do_o(char *l, t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	if (ft_strncmp(l, "pa\n", ft_strlen(l)) == 0)
		return (pa(stack_a, stack_b, env), 1);
	else if (ft_strncmp(l, "pb\n", ft_strlen(l)) == 0)
		return (pb(stack_a, stack_b, env), 1);
	else if (ft_strncmp(l, "sb\n", ft_strlen(l)) == 0)
		return (sb(stack_b, env), 1);
	else if (ft_strncmp(l, "sa\n", ft_strlen(l)) == 0)
		return (sa(stack_a, env), 1);
	else if (ft_strncmp(l, "ss\n", ft_strlen(l)) == 0)
		return (ss(stack_a, stack_b, env), 1);
	else if (ft_strncmp(l, "ra\n", ft_strlen(l)) == 0)
		return (ra(stack_a, env), 1);
	else if (ft_strncmp(l, "rb\n", ft_strlen(l)) == 0)
		return (rb(stack_b, env), 1);
	else if (ft_strncmp(l, "rr\n", ft_strlen(l)) == 0)
		return (rr(stack_a, stack_b, env), 1);
	else if (ft_strncmp(l, "rra\n", ft_strlen(l)) == 0)
		return (rra(stack_a, env), 1);
	else if (ft_strncmp(l, "rrb\n", ft_strlen(l)) == 0)
		return (rrb(stack_b, env), 1);
	else if (ft_strncmp(l, "rrr\n", ft_strlen(l)) == 0)
		return (rrr(stack_a, stack_b, env), 1);
	else
		return (0);
}
