/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dispatch_algorithm.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/20 22:37:54 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/27 05:56:16 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	dispatch_agorithm(t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	double	disorder;

	disorder = compute_disorder(*stack_a);
	env->disorder = disorder * 100;
	if (is_sorted(stack_a))
		return ;
	if (env->simple == 1)
		bubble_sort(stack_a, stack_b, env);
	else if (env->medium == 1)
		chunk_sort(stack_a, stack_b, env);
	else if (env->complex == 1)
		radix_sort(stack_a, stack_b, env);
	else if (env->adaptive == 1)
		adaptive(stack_a, stack_b, env, disorder);
	if (env->bench == 1)
		print_bench(env);
}

void	adaptive(t_stack **stack_a, t_stack **stack_b,
			t_env *env, double disorder)
{
	if (disorder < 0.2 || stack_size(stack_a) <= 5)
	{
		set_simple(env);
		selection_sort(stack_a, stack_b, env);
	}
	else if (disorder >= 0.2 && disorder < 0.5)
		chunk_sort(stack_a, stack_b, env);
	else
		radix_sort(stack_a, stack_b, env);
}

void	set_simple(t_env *env)
{
	env->simple = 1;
	env->strategy1 = "Simple";
	env->strategy2 = "O(n²)";
}

void	set_medium(t_env *env)
{
	env->medium = 1;
	env->strategy1 = "Medium";
	env->strategy2 = "O(n√n)";
}

void	set_complex(t_env *env)
{
	env->complex = 1;
	env->strategy1 = "Complex";
	env->strategy2 = "O(n log n)";
}
