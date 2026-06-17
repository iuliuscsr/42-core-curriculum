/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   output_functions.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/06 00:56:23 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/07 12:36:29 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	output_hex(char *hex, int i, char specifier, unsigned long nb)
{
	int	countoutput;

	countoutput = 0;
	if (specifier == 'x' || specifier == 'X')
	{
		countoutput = i;
		while (i > 0)
		{
			i--;
			ft_putchar_fd(hex[i], 1);
		}
	}
	else if (specifier == 'p')
	{
		countoutput = i + 2;
		if (nb == 0)
			return (ft_putstr_fd("(nil)", 1), 5);
		ft_putstr_fd("0x", 1);
		while (i > 0)
		{
			i--;
			ft_putchar_fd(hex[i], 1);
		}
	}
	return (countoutput);
}

int	output_str(char *str)
{
	int	len;

	if (!str)
		str = "(null)";
	len = ft_strlen(str);
	ft_putstr_fd(str, 1);
	return (len);
}

int	output_nb(long int nb)
{
	char	*snb;
	long	n;
	int		len;

	n = nb;
	snb = ft_itoa_modified(n);
	if (!snb)
		return (0);
	len = ft_strlen(snb);
	ft_putstr_fd(snb, 1);
	free (snb);
	return (len);
}
