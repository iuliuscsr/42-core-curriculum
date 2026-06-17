/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   hex_conversion.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmalsam <jmalsam@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/06 00:53:53 by jmalsam           #+#    #+#             */
/*   Updated: 2026/05/06 01:06:35 by jmalsam          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	convert_hex(unsigned long nb, char specifier)
{
	char			hex[100];
	int				remainder;
	int				i;
	unsigned long	originalnb;

	originalnb = nb;
	i = 0;
	if (originalnb == 0 && specifier != 'p')
		return (ft_putchar_fd('0', 1), 1);
	while (nb > 0)
	{
		remainder = nb % 16;
		if (remainder < 10)
			hex[i++] = remainder + '0';
		else if (specifier == 'X')
			hex[i++] = remainder + 'A' - 10;
		else if (specifier == 'x')
			hex[i++] = remainder + 'a' - 10;
		else if (specifier == 'p')
			hex[i++] = remainder + 'a' - 10;
		nb /= 16;
	}
	return (output_hex(hex, i, specifier, originalnb));
}
