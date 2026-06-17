/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   env_setup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/25 15:17:11 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/27 18:22:29 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

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

void	init_env(t_env *stack)
{
	stack->adaptive = 1;
	stack->simple = 0;
	stack->medium = 0;
	stack->complex = 0;
	stack->bench = 0;
	stack->print_operations = 1;
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
	stack->strategy1 = "Adaptive";
	stack->strategy2 = "O(n log n)";
	stack->checker = 0;
}

int	check_flags(int argc, char **argv, t_env *env)
{
	int	i;

	i = 1;
	while (i < argc && argv[i][0] == '-' && argv[i][1] == '-')
	{
		if (ft_strncmp("--bench", argv[i], 8) == 0)
		{
			env->bench = 1;
			env->print_operations = 1;
		}
		else if (ft_strncmp("--simple", argv[i], 9) == 0)
			env->simple = 1;
		else if (ft_strncmp("--medium", argv[i], 9) == 0)
			env->medium = 1;
		else if (ft_strncmp("--complex", argv[i], 10) == 0)
			env->complex = 1;
		else if (ft_strncmp("--adaptive", argv[i], 11) == 0)
			env->adaptive = 1;
		else
			return (0);
		i++;
	}
	if ((env->simple || env->medium || env->complex) && env->adaptive)
		env->adaptive = 0;
	return (i);
}

static void	print_bench_operations(t_env *env)
{
	ft_putstr_fd("\n[bench] sa: ", 2);
	ft_putnbr_fd(env->total_sa, 2);
	ft_putstr_fd(" sb: ", 2);
	ft_putnbr_fd(env->total_sb, 2);
	ft_putstr_fd(" ss: ", 2);
	ft_putnbr_fd(env->total_ss, 2);
	ft_putstr_fd(" pa: ", 2);
	ft_putnbr_fd(env->total_pa, 2);
	ft_putstr_fd(" pb: ", 2);
	ft_putnbr_fd(env->total_pb, 2);
	ft_putstr_fd("\n[bench] ra: ", 2);
	ft_putnbr_fd(env->total_ra, 2);
	ft_putstr_fd(" rb: ", 2);
	ft_putnbr_fd(env->total_rb, 2);
	ft_putstr_fd(" rr: ", 2);
	ft_putnbr_fd(env->total_rr, 2);
	ft_putstr_fd(" rra: ", 2);
	ft_putnbr_fd(env->total_rra, 2);
	ft_putstr_fd(" rrb: ", 2);
	ft_putnbr_fd(env->total_rrb, 2);
	ft_putstr_fd(" rrr: ", 2);
	ft_putnbr_fd(env->total_rrr, 2);
}

void	print_bench(t_env *env)
{
	int		prekomma;
	int		postkomma;

	prekomma = (int)env->disorder;
	postkomma = (int)(env->disorder * 100) % 100;
	if (postkomma < 0)
		postkomma = -postkomma;
	ft_putstr_fd("[bench] disorder: ", 2);
	ft_putnbr_fd(prekomma, 2);
	ft_putchar_fd('.', 2);
	ft_putnbr_fd(postkomma, 2);
	ft_putchar_fd('%', 2);
	ft_putstr_fd("\n[bench] strategy: ", 2);
	ft_putstr_fd(env->strategy1, 2);
	ft_putchar_fd(' ', 2);
	ft_putchar_fd('/', 2);
	ft_putchar_fd(' ', 2);
	ft_putstr_fd(env->strategy2, 2);
	ft_putstr_fd("\n[bench] total_ops: ", 2);
	ft_putnbr_fd(env->total_ops, 2);
	print_bench_operations(env);
	write(1, "\n", 1);
}
