import decimal as decimal_
import math


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


class Fraction:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def reduce(self):
        div = math.gcd(int(self.numerator), int(self.denominator))
        while div > 1:
            self.numerator /= div
            self.denominator /= div
            div = math.gcd(int(self.numerator),int(self.denominator))


    def getDecimal(self):
        return self.numerator / self.denominator



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


def probability_to_fractional(probability):
    f = decimal_to_fraction(probability/100)
    f.reduce()
    return Fractional(f.denominator - f.numerator, f.numerator)

    # return denominator / (numerator + denominator)  # probability of fractional x / y is (y / (x+y))*100


def decimal_to_fraction(decimal):
    dec = decimal_.Decimal(decimal.__str__())
    power = dec.as_tuple().exponent.__abs__()
    denom = math.pow(10, power)
    return Fraction(decimal * denom, denom)


def main():
    frac = decimal_to_fraction(0.5)
    # print(frac.numerator)
    # print(frac.denominator)
    frac.reduce()
    # print(frac.numerator)
    # print(frac.denominator)
    print(probability_to_fractional(0.5).get_odds().probability)


if __name__ == '__main__':
    main()
