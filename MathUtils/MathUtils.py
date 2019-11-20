import decimal as decimal_
import math


# For clarification: probability is bounded by 0 & 1
#                     percentage is probability * 100; bound by 0 & 100...
#  If you see somewhere other than here that x has a probability of 40, then translate to .4 for use in this program

class Odds(object):
    """Odds class - maintains probabilities & conversions to types of odds used in betting"""
    def __init__(self, probability):
        self.decimal = self.moneyline = self.fractional = 0
        self.probability = probability
        self.percentage = probability * 100

    def compute_values(self):
        pass
        self.decimal = probability_to_decimal(self.probability)
        self.moneyline = probability_to_moneyline(self.probability)
        self.fractional = probability_to_fractional(self.probability)

    @property
    def probability(self):
        return self.__probability

    @probability.setter
    def probability(self, probability):
        self.__probability = probability
        self.compute_values()


class Decimal(object):
    """Decimal Betting Class"""
    def __init__(self, decimal):
        self.decimal = decimal

    def get_odds(self):
        probability = decimal_to_probability(self.decimal)
        return Odds(probability)


class MoneyLine(object):
    """Moneyline Bet class"""
    def __init__(self, line):
        self.line = line

    def get_odds(self):
        probability = line_to_probability(self.line)
        return Odds(probability)


class Fraction(object):
    """literal mathematical fraction representation, NOT the Fractional bet format"""
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def reduce(self):
        div = math.gcd(int(self.numerator), int(self.denominator))
        while div > 1:
            self.numerator /= div
            self.denominator /= div
            div = math.gcd(int(self.numerator), int(self.denominator))


class Fractional(Fraction):
    """Fractional Odds Class"""
    def get_odds(self):
        probability = fraction_to_probability(self)
        return Odds(probability)


def line_to_probability(line):
    if line <= 0:
        probability = line.__abs__() / (100 + line.__abs__())
    elif line > 0:
        probability = 100 / (100 + line)
    return probability  # defined https://www.bettingexpert.com/academy/betting-fundamentals/betting-odds-explained


def decimal_to_probability(decimal):
    return 1 / decimal  # probability of decimal 1.5 is (1 / 1.5 )


def fraction_to_probability(fraction):
    return fraction.denominator / (
                fraction.numerator + fraction.denominator)  # probability of fractional x / y is (y / (x+y))


def probability_to_moneyline(probability):
    if probability >= .5:
        rawLine = -1 * probability / (1 - probability)
    else:
        rawLine = (1 - probability) / probability
    line = rawLine * 100
    return line


def probability_to_decimal(probability):
    return Decimal(1 / probability)


def probability_to_fractional(probability):
    f = decimal_to_fraction(probability)
    f.reduce()
    return Fractional(f.denominator - f.numerator, f.numerator)


def decimal_to_fraction(decimal):
    dec = decimal_.Decimal(decimal.__str__())
    power = dec.as_tuple().exponent.__abs__()
    denom = math.pow(10, power)
    return Fraction(decimal * denom, denom)


def kelly_criterion(projected_odds: Odds, actual_odds: Odds):
    """Kelly is method of determining the amount of your bank account to hedge of a bet. Reduces risk"""
    numerator = projected_odds.probability * actual_odds.decimal
    numerator -= 1
    denominator = actual_odds.decimal - 1
    stake = numerator / denominator  # factor to multiply by value in bank account for a given bet


def main():
    lines = [+600, +450, +200, +180, +155, +135, +1500, +2400]
    probs = linesToprobs(lines)
    # print(probs)
    probabilityOfAll = 1
    for prob in probs:
        probabilityOfAll *= prob[1]
    print(probabilityOfAll * 100)
    print(probability_to_moneyline(probabilityOfAll))
    # frac = decimal_to_fraction(0.5)
    # print(frac.numerator)
    # print(frac.denominator)
    # frac.reduce()
    # print(frac.numerator)
    # print(frac.denominator)
    # print(probability_to_fractional(0.5).get_odds().probability)


def linesToprobs(lines):
    probs = []
    for line in lines:
        probs.append((line, line_to_probability(line)))
    return probs


if __name__ == '__main__':
    main()
