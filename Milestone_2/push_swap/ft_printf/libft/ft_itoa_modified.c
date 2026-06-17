/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa_modified.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/23 12:21:34 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/07 12:32:09 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include "libft.h"

int	get_len(long int n)
{
	int	len;

	len = 0;
	if (n <= 0)
		len++;
	while (n != 0)
	{
		n /= 10;
		len++;
	}
	return (len);
}

char	*ft_itoa_modified(long int n)
{
	char		*nb;
	int			len;
	long int	long_n;

	long_n = n;
	len = get_len(long_n);
	nb = malloc((len + 1) * sizeof(char));
	if (!nb)
		return (NULL);
	nb[len] = '\0';
	if (long_n == 0)
		nb[0] = '0';
	if (long_n < 0)
	{
		nb[0] = '-';
		long_n *= -1;
	}
	while (long_n > 0)
	{
		nb[len - 1] = (long_n % 10) + '0';
		long_n /= 10;
		len--;
	}
	return (nb);
}
