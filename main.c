/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/18 16:05:53 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/20 02:04:49 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_stack	*stack_a;
	t_stack	*stack_b;
	t_stack	*temp;

	stack_b = NULL;
	stack_a = get_input(argc, argv);
	if (!stack_a)
		return (1);
	rb(&stack_b);
	temp = stack_a;
	while (temp)
	{
		ft_printf("%d\n", temp->content);
		temp = temp->next;
	}
	ft_stackclear(&stack_a, del_int);
}
