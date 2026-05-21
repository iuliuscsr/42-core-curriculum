/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/18 16:05:53 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/22 00:31:23 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_strg	*control;
	t_stack	*stack_a;
	t_stack	*stack_b;
	t_stack	*temp;
	double	disorder;

	stack_b = NULL;
	stack_a = get_input(argc, argv);
	if (!stack_a)
		return (1);
	control = init_control(stack_a, stack_b);
	disorder = compute_disorder(stack_a);
	// if (disorder < 0.2)
		selection_sort(control);
	ft_stackclear(&stack_a, del_int);
}
