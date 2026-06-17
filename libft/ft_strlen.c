/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlen.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/16 14:07:51 by jmalsam           #+#    #+#             */
/*   Updated: 2026/04/20 16:27:46 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <string.h>

size_t	ft_strlen(const char *str)
{
	int		i;
	size_t	count;

	count = 0;
	i = 0;
	while (str[i] != '\0')
	{
		count += 1;
		i++;
	}
	return (count);
}
