/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/04 12:30:42 by jawosylu          #+#    #+#             */
/*   Updated: 2026/05/27 03:23:46 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ft_isnewline(char *str)
{
	int	i;

	i = 0;
	if (!str)
		return (0);
	while (str[i])
	{
		if (str[i] == '\n')
			return (1);
		i++;
	}
	return (0);
}

char	*get_input_gnl(int fd, char *buffer)
{
	char	*readval;
	char	*temp;
	int		bytes_read;

	bytes_read = 1;
	while (!ft_isnewline(buffer) && bytes_read > 0)
	{
		readval = ft_calloc(BUFFER_SIZE + 1, 1);
		if (readval == NULL)
			return (NULL);
		bytes_read = read(fd, readval, BUFFER_SIZE);
		if (bytes_read < 0)
			return (free(readval), free(buffer), (NULL));
		temp = buffer;
		buffer = ft_strjoin(temp, readval);
		free(temp);
		free(readval);
		if (buffer == NULL)
			return (NULL);
	}
	if (buffer[0] == '\0')
		return (free(buffer), (NULL));
	return (buffer);
}

char	*line(char *str)
{
	int		i;
	char	*output;
	int		a;

	i = 0;
	a = 0;
	if (!str || !str[0])
		return (NULL);
	while (str[i] != 0 && str[i] != '\n')
		i++;
	if (str[i] == '\n')
		i++;
	output = ft_calloc(i + 1, 1);
	if (output == NULL)
		return (NULL);
	while (a < i)
	{
		output[a] = str[a];
		a++;
	}
	return (output);
}

void	get_rest(char *str, char *buffer)
{
	int		i;

	i = 0;
	if (str == NULL || buffer == NULL)
		return ;
	while (str[i] != 0 && str[i] != '\n')
		i++;
	if (str[i] == '\n')
		i++;
	if (!str[i])
	{
		buffer[0] = '\0';
		return ;
	}
	ft_strlcpy(buffer, str + i, BUFFER_SIZE + 1);
}

char	*get_next_line(int fd)
{
	static char	buffer[BUFFER_SIZE + 1];
	char		*output;
	char		*temp;

	if (fd < 0 || BUFFER_SIZE < 1)
		return (NULL);
	temp = ft_strdup(buffer);
	if (temp == NULL)
		return (NULL);
	buffer[0] = '\0';
	temp = get_input_gnl(fd, temp);
	if (temp == NULL || !temp[0])
	{
		free(temp);
		return (NULL);
	}
	output = line(temp);
	if (output == NULL)
		return (NULL);
	get_rest(temp, buffer);
	free(temp);
	return (output);
}
