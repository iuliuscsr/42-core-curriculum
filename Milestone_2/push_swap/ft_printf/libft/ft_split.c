/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/22 15:55:27 by jmalsam           #+#    #+#             */
/*   Updated: 2026/04/28 13:31:18 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include "libft.h"

static int	count_words(char const *s, char c)
{
	int	i;
	int	wordcounter;

	i = 0;
	wordcounter = 0;
	while (s[i] != '\0')
	{
		if (s[i] != c && (i == 0 || s[i - 1] == c))
			wordcounter++;
		i++;
	}
	return (wordcounter);
}

static char	*allocate_word(char const *s, char c, int chr_index)
{
	int	i;

	i = 0;
	while (s[chr_index + i] != '\0' && s[chr_index + i] != c)
		i++;
	return (ft_substr(s, chr_index, i));
}

static void	free_array(char	**stringarray, int arraysize)
{
	int	i;

	i = 0;
	while (i < arraysize)
	{
		free(stringarray[i]);
		i++;
	}
	free(stringarray);
}

char	**ft_split(char const *s, char c)
{
	int		chr_index;
	int		word_index;
	int		num_words;
	char	**stringarray;

	num_words = count_words(s, c);
	stringarray = malloc((num_words + 1) * sizeof(char *));
	if (!stringarray)
		return (NULL);
	word_index = 0;
	chr_index = 0;
	while (word_index < num_words)
	{
		while (s[chr_index] != '\0' && s[chr_index] == c)
			chr_index++;
		stringarray[word_index] = allocate_word(s, c, chr_index);
		if (!stringarray[word_index])
			return (free_array(stringarray, word_index), NULL);
		while ((s[chr_index] != '\0' && s[chr_index] != c))
			chr_index++;
		word_index++;
	}
	stringarray[word_index] = NULL;
	return (stringarray);
}
