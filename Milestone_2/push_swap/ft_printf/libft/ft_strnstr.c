/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/21 12:28:29 by jmalsam           #+#    #+#             */
/*   Updated: 2026/04/28 13:09:59 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <string.h>

char	*ft_strnstr(const char *big, const char *little, size_t len)
{
	size_t	i;
	size_t	j;

	i = 0;
	j = 0;
	if (little[0] == '\0')
		return ((char *)big);
	while (1)
	{
		if (big[j] == '\0' || j == len)
			return (NULL);
		if (little[i] == big[j])
		{
			if (little[i + 1] == '\0')
				return ((char *) &big[j - i]);
			i++;
			j++;
			continue ;
		}
		j = j - i + 1;
		i = 0;
	}
}
