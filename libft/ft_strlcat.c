/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/20 12:01:17 by jmalsam           #+#    #+#             */
/*   Updated: 2026/04/20 16:29:45 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <string.h>
#include "libft.h"

size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	i;
	size_t	strlensrc;
	size_t	strlendst;

	strlensrc = ft_strlen(src);
	strlendst = ft_strlen(dst);
	if (strlendst >= size)
		return (size + strlensrc);
	i = 0;
	while (src[i] != '\0' && strlendst + i < size - 1)
	{
		dst[strlendst + i] = src[i];
		i++;
	}
	dst[strlendst + i] = '\0';
	return (strlendst + strlensrc);
}
