/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input_parsing_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/19 14:19:09 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/27 04:54:01 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	del_int(int content)
{
	(void)content;
}

void	free_and_exit(void)
{
	ft_putendl_fd("Error", 2);
	exit(1);
}

void	free_split(char **split_input)
{
	int	i;

	i = 0;
	while (split_input[i])
	{
		free(split_input[i]);
		i++;
	}
	free(split_input);
}

long	ft_atoi_modified(const char *nptr)
{
	int			i;
	int			sign;
	long		result;

	i = 0;
	result = 0;
	sign = 1;
	while ((nptr[i] > 8 && nptr[i] < 14) || nptr[i] == 32)
		i++;
	if (nptr[i] == '-' || nptr[i] == '+')
	{
		if (nptr[i] == '-')
			sign = -1;
		i++;
	}
	while (nptr[i] >= '0' && nptr[i] <= '9')
	{
		result = result * 10 + (nptr[i] - '0');
		i++;
	}
	return (result * sign);
}
