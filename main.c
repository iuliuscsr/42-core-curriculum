/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/18 16:05:53 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/19 19:54:52 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_stack	*stack_a;
	t_stack	*temp;

	stack_a = get_input(argc, argv);
	if (!stack_a)
		return (1);
	temp = stack_a;
	while (temp)
	{
		ft_printf("%d\n", temp->content);
		temp = temp->next;
	}
	ft_stackclear(&stack_a, del_int);
}
