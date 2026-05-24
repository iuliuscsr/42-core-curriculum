/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   normalize.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jawosylu <jawosylu@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/24 11:56:49 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/24 15:49:30 by jawosylu         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	*ft_stack_to_arr(t_stack *stack, int size)
{
	int	*arr;
	int	i;

	arr = malloc(sizeof(int) * size);
	if (!arr)
		return (NULL);

	i = 0;

	while (stack)
	{
		arr[i] = stack->content;
		stack = stack->next;
		i++;
	}
	return (arr);
}

static void	ft_sort_arr(int *arr, int size)
{
	int	i;
	int	j;
	int	temp;

	i = 0;
	while (i < size)
	{
		j = i + 1;
		while (j < size)
		{
			if (arr[i] > arr[j])
			{
				temp = arr[i];
				arr[i] = arr[j];
				arr[j] = temp;
			}
			j++;
		}
		i++;
	}
}

static void	ft_index_stack(t_stack *stack, int *arr, int size)
{
	int	i;
	t_stack *temp;

	i = 0;
	while (i < size)
	{
		temp = stack;
		while (temp && arr[i] != temp->content)
			temp = temp->next;
		temp->index = i;
		i++;
	}
}

void	ft_normalize(t_stack *stack, int size)
{
	int	*arr;
	arr = ft_stack_to_arr(stack, size);
	if (!arr)
		return ;
	ft_sort_arr(arr, size);
	ft_index_stack(stack, arr, size);
	free(arr);
}

