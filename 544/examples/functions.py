import math


class Functions(object):
    ''' A collection of functions that can be used to
    describe a preference for some resource.
    '''

    @staticmethod
    def linear(slope=1, shift=0):
        ''' A function with linear value along the x-axis
        with slope and shift.

        :param slope: The slope of the value line
        :param shift: The shift of the value line
        :returns: The prepared function
        '''
        return lambda x: (x * slope) + shift

    @staticmethod
    def unit(value=1):
        ''' A function with unit value along the x-axis

        :param value: The value to at each point (default 1)
        :returns: The prepared function
        '''
        return lambda x: value

    @staticmethod
    def log(base=2):
        ''' A function with log value along the x-axis

        :param base: The base of the logarithm
        :returns: The prepared function
        '''
        return lambda x: math.log(x, base)

    @staticmethod
    def exp(base=2):
        ''' A function with exponential value along
        the x-axis

        :param base: The base of the exponent
        :returns: The prepared function
        '''
        return lambda x: math.pow(base, x)

    @staticmethod
    def polynomial(power=2):
        ''' A function with polynomial value along
        the x-axis

        :param base: The base of the logarithm
        :returns: The prepared function
        '''
        return lambda x: math.pow(x, power)

    @staticmethod
    def impulse(values):
        ''' A function with value only at specific points

        :param values: The values dict where one sees value
        :returns: The prepared function
        '''
        if not isinstance(values, dict):
            values = dict((k, 1) for k in values)
        return lambda x: values.get(x, 0)
