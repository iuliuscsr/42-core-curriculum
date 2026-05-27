/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/18 16:05:53 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/27 04:44:22 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_env	*env;
	t_stack	*stack_a;
	t_stack	*stack_b;

	env = malloc(sizeof(t_env));
	if (!env)
		return (0);
	init_env(env);
	stack_b = NULL;
	stack_a = get_input(argc, argv, env);
	if (!stack_a)
		return (free(stack_a), free(env), 0);
	dispatch_agorithm(&stack_a, &stack_b, env);
	ft_stackclear(&stack_a, del_int);
	free(env);
}
