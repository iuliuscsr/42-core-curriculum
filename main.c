/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/18 16:05:53 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/21 11:28:15 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"
#include <stdio.h>

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
	t_strg *control = init_control(control, stack_a, stack_b);
	disorder = compute_disorder(stack_a);
	printf("%f", disorder);
	// rb(&stack_b);
	// temp = stack_a;
	// while (temp)
	// {
	// 	ft_printf("%d\n", temp->content);
	// 	temp = temp->next;
	// }
	ft_stackclear(&stack_a, del_int);
}
