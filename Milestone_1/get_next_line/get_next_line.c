/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/07 12:47:08 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/17 23:05:24 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

int	ft_strchr_modified(char *s)
{
	int		i;
	int		seperator;

	if (!s)
		return (-1);
	i = 0;
	seperator = '\n';
	while (s[i] != '\0')
	{
		if ((unsigned char)s[i] == (unsigned char)seperator)
			return (i);
		i++;
	}
	return (-1);
}

char	*extract_last(char **src, int srclen)
{
	char	*res;

	res = ft_substr(*src, 0, srclen);
	if (!res)
		return (ft_free_str1(src), NULL);
	ft_free_str1(src);
	return (res);
}

char	*extract_line(char **src, int posnl)
{
	char	*res;

	res = ft_substr(*src, 0, posnl + 1);
	if (!res)
		return (ft_free_str1(src), NULL);
	return (res);
}

char	*edit_strings(char **src)
{
	char	*temp;
	char	*res;
	int		srclen;
	int		posnl;

	if (!src || !*src)
		return (NULL);
	temp = *src;
	srclen = ft_strlen(temp);
	posnl = ft_strchr_modified(temp);
	if (posnl == -1)
		return (extract_last(src, srclen));
	res = extract_line(src, posnl);
	if (!res)
		return (NULL);
	*src = NULL;
	if (srclen - (posnl + 1) > 0)
	{
		*src = ft_substr(temp, (posnl + 1), (srclen - (posnl + 1)));
		if (!*src)
			return (free(temp), free(res), NULL);
	}
	free(temp);
	return (res);
}

char	*get_next_line(int fd)
{
	static char	*src;
	char		*buffer;
	int			bytesread;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (ft_free_str1(&src), NULL);
	buffer = malloc((BUFFER_SIZE + 1) * sizeof(char));
	if (!buffer)
		return (ft_free_str1(&src), NULL);
	bytesread = 1;
	while (ft_strchr_modified(src) == -1 && bytesread > 0)
	{
		bytesread = read(fd, buffer, BUFFER_SIZE);
		if (bytesread == -1)
			return (free(buffer), ft_free_str1(&src), NULL);
		buffer[bytesread] = '\0';
		if (bytesread > 0)
			src = ft_strjoin_modified(src, buffer);
		if (bytesread > 0 && !src)
			return (free(buffer), NULL);
	}
	free(buffer);
	if (!src || *src == '\0')
		return (ft_free_str1(&src), NULL);
	return (edit_strings(&src));
}
