/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/22 12:57:22 by jmalsam           #+#    #+#             */
/*   Updated: 2026/04/23 11:27:33 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include "libft.h"

char	*ft_strjoin(char const *s1, char const *s2)
{
	char	*s3;
	size_t	s1len;
	size_t	s2len;

	s1len = ft_strlen(s1);
	s2len = ft_strlen(s2);
	s3 = malloc((s1len + s2len + 1) * (sizeof(char)));
	if (!s3)
		return (NULL);
	ft_strlcpy(s3, s1, s1len + 1);
	ft_strlcpy(s3 + s1len, s2, s2len + 1);
	return (s3);
}
