/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker_bonus.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jawosylu <jawosylu@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 09:48:05 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/27 17:45:51 by jawosylu         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker_bonus.h"

static void	init_env_checker(t_env *stack)
{
	stack->adaptive = 1;
	stack->bench = 0;
	stack->simple = 0;
	stack->medium = 0;
	stack->complex = 0;
	stack->total_ops = 0;
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
	stack->checker = 1;
}

static void	fr_and_m(char *m, t_stack *stack_a, t_stack *stack_b, t_env *env)
{
	ft_stackclear(&stack_a, del_int);
	ft_stackclear(&stack_b, del_int);
	free(env);
	ft_putendl_fd(m, 1);
}

void	ch_a_ou(t_stack *stack_a, t_stack *stack_b, t_env *env, int size)
{
	if (is_sorted(&stack_a) && stack_b == NULL
		&& size == stack_size(&stack_a))
	{
		fr_and_m("OK", stack_a, stack_b, env);
	}
	else
		fr_and_m("KO", stack_a, stack_b, env);
}

static int	check_ops_stack(t_stack **stack_a, t_stack **stack_b, t_env *env)
{
	char	*line;

	line = get_next_line_bonus(0);
	if (!line)
		return (ft_putendl_fd("Error", 1), 0);
	while (line != NULL)
	{
		if (c_do_o(line, stack_a, stack_b, env) == 0)
			return (free(line), ft_putendl_fd("Error", 1), 0);
		free(line);
		line = get_next_line_bonus(0);
		if (!line)
			return (free(line), 1);
	}
	return (1);
}

int	main(int argc, char **argv)
{
	t_stack	*stack_a;
	t_stack	*stack_b;
	t_env	*env;
	int		size;

	env = malloc(sizeof(t_env));
	if (!env)
		return (0);
	init_env_checker(env);
	stack_b = NULL;
	stack_a = get_input(argc, argv, env);
	if (!stack_a)
		return (free(stack_a), free(env), 0);
	size = stack_size(&stack_a);
	if ((check_ops_stack(&stack_a, &stack_b, env)) == 0)
		return (ft_stackclear(&stack_a, del_int),
			ft_stackclear(&stack_b, del_int), free(env), 0);
	ch_a_ou(stack_a, stack_b, env, size);
}
