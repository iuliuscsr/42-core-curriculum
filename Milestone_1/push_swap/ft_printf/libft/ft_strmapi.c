/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/25 19:03:21 by jmalsam           #+#    #+#             */
/*   Updated: 2026/04/27 18:38:31 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include "libft.h"

char	*ft_strmapi(char const *s, char (*f)(unsigned int, char))
{
	size_t	slen;
	size_t	i;
	char	*news;

	if (!s || !f)
		return (NULL);
	slen = ft_strlen(s);
	news = malloc((slen + 1) * sizeof(char));
	if (!news)
		return (NULL);
	i = 0;
	while (s[i] != '\0')
	{
		news[i] = f((unsigned int)i, s[i]);
		i++;
	}
	news[i] = '\0';
	return (news);
}
