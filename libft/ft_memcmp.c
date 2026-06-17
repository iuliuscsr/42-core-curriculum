/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/21 12:19:19 by jmalsam           #+#    #+#             */
/*   Updated: 2026/04/21 12:27:49 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <string.h>

int	ft_memcmp(const void *s1, const void *s2, size_t n)
{
	const unsigned char	*ps1;
	const unsigned char	*ps2;
	size_t				i;

	ps1 = s1;
	ps2 = s2;
	i = 0;
	if (n == 0)
		return (0);
	while ((ps1[i] == ps2[i]) && (i < n - 1))
		i++;
	return ((unsigned char)ps1[i] - (unsigned char)ps2[i]);
}
