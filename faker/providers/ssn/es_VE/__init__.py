from .. import Provider as SsnProvider

# https://es.wikipedia.org/wiki/C%C3%A9dula_de_identidad_(Venezuela)
# https://es.wikipedia.org/wiki/Registro_%C3%9Anico_de_Informaci%C3%B3n_Fiscal
# https://github.com/arthurdejong/python-stdnum/blob/master/stdnum/ve/rif.py

# Valid RIF type letters and the value each contributes to the check digit calculation
RIF_TYPES = {
    "V": 4,  # natural person, Venezuelan
    "E": 8,  # natural person, foreign
    "J": 12,  # legal entity
    "P": 16,  # passport
    "G": 20,  # government
}

RIF_WEIGHTS = (3, 2, 7, 6, 5, 4, 3, 2)


def rif_check_digit(rif_type: str, body: str) -> str:
    """
    Calculate the check digit of a Venezuelan RIF.

    :param rif_type: the RIF type letter (one of ``V``, ``E``, ``J``, ``P`` or ``G``)
    :param body: the 8 digits following the type letter
    :return: the check digit for the given type and body
    """
    if rif_type not in RIF_TYPES:
        raise ValueError(f"Invalid RIF type: {rif_type!r}")
    if len(body) != 8 or not body.isdigit():
        raise ValueError(f"Invalid RIF body: {body!r}")

    total = RIF_TYPES[rif_type] + sum(weight * int(digit) for weight, digit in zip(RIF_WEIGHTS, body))
    return "00987654321"[total % 11]


class Provider(SsnProvider):
    """
    A Faker provider for Venezuelan national identification documents: the
    cédula de identidad and the RIF (Registro Único de Información Fiscal).
    """

    cedula_types = ("V", "E")
    rif_types = tuple(RIF_TYPES)

    def cedula(self) -> str:
        """
        Generate a Venezuelan cédula de identidad: a type letter (``V`` for Venezuelan
        nationals, ``E`` for naturalized/foreign residents) followed by a number.

        :return: a random Venezuelan cédula de identidad

        :sample:
        """
        cedula_type = self.random_element(self.cedula_types)
        number = self.random_int(min=1000000, max=99999999)
        return f"{cedula_type}-{number}"

    def rif(self) -> str:
        """
        Generate a Venezuelan RIF (Registro Único de Información Fiscal): a type
        letter (one of ``V``, ``E``, ``J``, ``P`` or ``G``), 8 digits and a check
        digit computed the same way as in :mod:`stdnum.ve.rif`.

        :return: a random Venezuelan RIF

        :sample:
        """
        rif_type = self.random_element(self.rif_types)
        body = f"{self.random_int(min=0, max=99999999):08d}"
        check_digit = rif_check_digit(rif_type, body)
        return f"{rif_type}-{body}-{check_digit}"

    def ssn(self) -> str:
        """
        :return: a random Venezuelan cédula de identidad

        :sample:
        """
        return self.cedula()
