/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_sorting.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/20 22:37:54 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/24 23:36:48 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"
#include <stdio.h>

double	compute_disorder(t_stack *stack_a)
{
	t_stack	*i;
	t_stack	*j;
	int		nb;
	double	mistakes;
	double	total_pairs;

	mistakes = 0;
	total_pairs = 0;
	i = stack_a;
	while (i)
	{
		nb = i->content;
		j = i->next;
		while (j)
		{
			if (nb > j->content)
				mistakes++;
			j = j->next;
			total_pairs++;
		}
		i = i->next;
	}
	if (total_pairs == 0)
		return (0);
	return (mistakes / total_pairs);
}

void    init_env(t_env *stack)
{
    stack->adaptive = 1;
    stack->bench = 0;
    stack->simple = 0;
    stack->medium = 0;
    stack->complex = 0;
	stack->total_ops= 0;
	stack->total_sa = 0;
	stack->total_sb = 0;
	stack->total_ss = 0;
	stack->total_pa = 0;
	stack->total_pb = 0;
	stack->total_ra = 0;
	stack->total_rb = 0;
	stack->total_rr = 0;
	stack->total_rra = 0;
	stack->total_rrb = 0;
	stack->total_rrr = 0;
	stack->disorder = 0;
	stack->strategy1 = NULL;
	stack->strategy2 = NULL;
}

int check_flags(int argc, char **argv, t_env *stack)
{
    int i = 0;
    int length;

    while (argc > 1 && argv[i + 1] && i < 2)
    {
		length = ft_strlen(argv[i]);
        if (ft_strncmp("--simple", argv[i + 1], length) == 0)
        {
            stack->simple = 1;
			stack->strategy1 = "simple";
			stack->strategy2 = "O(n^2)";
            i++;
        }
        if (ft_strncmp("--bench", argv[i + 1], length) == 0)
        {
			stack->bench = 1;
            i++;
        }
		if (ft_strncmp("--medium", argv[i + 1], length) == 0)
		{
			stack->medium = 1;
			i++;
		}
        else
            break;
    }
    return i;
}

void	print_bench(t_env *env)
{

	printf("[bench] disorder: %.2f\n", env->disorder); //problematisch weil kein printf darf benutzt werden -> wir koennen 'f' in unser ft_printf implementieren?
	ft_printf("[bench] strategy: %s %s\n", env->strategy1, env->strategy2);
	ft_printf("[bench] total_ops: %d\n", env->total_ops);
	ft_printf("[bench] sa: %d sb: %d ss: %d pa: j%d pb: %d\n", env->total_sa, env->total_sb, env->total_ss, env->total_pa, env->total_pb);
	ft_printf("[bench] ra: %d rb: %d rr: %d rra: %d rrb: %d rrr: %d\n", env->total_ra, env->total_rb, env->total_rr, env->total_rra, env->total_rrb, env->total_rrr);
}


void    stack_sorting(t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	double disorder;

	disorder = compute_disorder(*stack_a);
	env->disorder = disorder * 100;
    if (env->simple == 1)
        bubble_sort(stack_a, env);
	else if (env->medium == 1)
		chunk_sort(stack_a, stack_b, env);
    else if (env->adaptive == 1)
	{
		if (disorder < 0.2)
			bubble_sort(stack_a, env); // easy algo
		else if (disorder >= 0.2 && disorder < 0.5)
			chunk_sort(stack_a, stack_b, env); // medium algo noch nix da deshalb printf
		else
			bubble_sort(stack_a, env); // complex algo
	}
	if (env->bench == 1)
		print_bench(env);
}
