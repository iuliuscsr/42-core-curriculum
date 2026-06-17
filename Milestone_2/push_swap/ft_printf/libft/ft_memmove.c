/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/16 18:57:36 by jmalsam           #+#    #+#             */
/*   Updated: 2026/04/20 16:29:12 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <string.h>
#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	unsigned char		*pdest;
	const unsigned char	*psrc;

	pdest = dest;
	psrc = src;
	if (dest == src)
		return (dest);
	if (dest < src)
		return (ft_memcpy(dest, src, n));
	while (n > 0)
	{
		n--;
		pdest[n] = psrc[n];
	}
	return (dest);
}
