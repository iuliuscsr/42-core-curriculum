/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/21 11:50:51 by jmalsam           #+#    #+#             */
/*   Updated: 2026/04/21 12:06:27 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <string.h>

void	*ft_memchr(const void *s, int c, size_t n)
{
	const unsigned char	*psrc;
	size_t				i;

	psrc = s;
	i = 0;
	while (i < n)
	{
		if (psrc[i] == (unsigned char)c)
			return ((void *)&psrc[i]);
		i++;
	}
	return (NULL);
}
