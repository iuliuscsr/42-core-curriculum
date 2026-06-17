/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/21 16:48:58 by jmalsam           #+#    #+#             */
/*   Updated: 2026/04/22 13:08:27 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include "libft.h"

char	*ft_strdup(const char *s)
{
	char	*dup;
	size_t	strlen;

	strlen = ft_strlen(s);
	dup = ft_calloc(strlen + 1, 1);
	if (!dup)
		return (NULL);
	ft_memcpy(dup, s, strlen);
	return (dup);
}
