class Odds:
    def __init__(self, probability):
        self.decimal = self.american = self.fractional = 0
        self.probability = probability

    def compute_values(self):
        pass
        # self.decimal = self.__data[0]
        # self.american = self.__data[-1]
        # self.fractional = self.__data[math.floor(len(self.__data) / 2)]

    @property
    def probability(self):
        return self.__probability

    @probability.setter
    def probability(self, probability):
        self.__probability = probability
        self.compute_values()


class Fractional:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def get_odds(self):
        probability = fraction_to_probability(self.numerator, self.denominator)
        return Odds(probability * 100)


class Decimal:
    def __init__(self, decimal):
        self.decimal = decimal

    def get_odds(self):
        probability = decimal_to_probability(self.decimal)
        return Odds(probability * 100)


class MoneyLine:
    def __init__(self, line):
        self.line = line

    def get_odds(self):
        probability = line_to_probability(self.line)
        return Odds(probability * 100)


def line_to_probability(line):
    if line < 0:
        probability = line.__abs__() / (100 + line.__abs__())
    elif line > 0:
        probability = 100 / (100 + line)
    else:
        return ValueError('wtf kind of line is this')
    return probability  # defined https://www.bettingexpert.com/academy/betting-fundamentals/betting-odds-explained


def decimal_to_probability(decimal):
    return 1 / decimal  # probability of decimal 1.5 is (1 / 1.5 )*100


def fraction_to_probability(numerator, denominator):
    return denominator / (numerator + denominator)  # probability of fractional x / y is (y / (x+y))*100


def main():
    pass


if __name__ == '__main__':
    main()
