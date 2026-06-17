/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/11 11:10:19 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/15 20:16:53 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

void	ft_free_str1(char **src)
{
	free (*src);
	*src = NULL;
}

size_t	ft_strlen(const char *str)
{
	int		i;
	size_t	count;

	if (!str)
		return (0);
	count = 0;
	i = 0;
	while (str[i] != '\0')
	{
		count += 1;
		i++;
	}
	return (count);
}

size_t	ft_strlcpy(char *dst, const char *src, size_t size)
{
	size_t	i;
	size_t	strlen;

	strlen = ft_strlen(src);
	if (size == 0)
		return (strlen);
	i = 0;
	while (src[i] != '\0' && i < size - 1)
	{
		dst[i] = src[i];
		i++;
	}
	dst[i] = '\0';
	return (strlen);
}

char	*ft_substr(char *s, unsigned int start, size_t len)
{
	char	*subs;
	size_t	slen;

	if (!s)
		return (NULL);
	slen = ft_strlen(s);
	if (start >= slen)
		len = 0;
	else if (len > slen - start)
		len = slen - start;
	subs = malloc((len + 1) * (sizeof(char)));
	if (!subs)
		return (NULL);
	ft_strlcpy(subs, s + start, len + 1);
	return (subs);
}

char	*ft_strjoin_modified(char *s1, char const *s2)
{
	char	*s3;
	size_t	i;
	size_t	j;

	if (!s1)
	{
		s1 = malloc(1);
		if (!s1)
			return (ft_free_str1(&s1), NULL);
		s1[0] = '\0';
	}
	s3 = malloc((ft_strlen(s1) + ft_strlen(s2) + 1));
	if (!s3)
		return (free(s1), NULL);
	i = -1;
	while (s1[++i])
		s3[i] = s1[i];
	j = -1;
	while (s2[++j])
		s3[i + j] = s2[j];
	s3[i + j] = '\0';
	return (free(s1), s3);
}
