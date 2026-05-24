/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/18 16:05:53 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/24 23:36:37 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_strg	*control;
	t_env	*env;
	t_stack	*stack_a;
	t_stack	*stack_b;
	t_stack	*temp;
	double	disorder;

	env = malloc(sizeof(t_env));
	if (!env)
		return (0);
	init_env(env);
	stack_b = NULL;
	stack_a = get_input(argc, argv, env);
	if (!stack_a)
		return (1);
	control = init_control(stack_a, stack_b);
	selection_sort(control, env);
	ft_stackclear(&stack_a, del_int);
}
