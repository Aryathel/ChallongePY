from aenum import MultiValueEnum

# Organizes parameters from pythonic syntax to what Challonge expects to see.
def _prepare_params(improper_params, prefix = None):
    params = {}

    for i, j in improper_params.items():
        # Challonge only accepts booleans as lowercase 'true' or 'false'
        if isinstance(j, bool):
            j = str(j).lower()

        try:
            if isinstance(j, MultiValueEnum):
                j = j.value
        except:
            pass

        if prefix:
            params[f"{prefix}[{i}]"] = j
        else:
            params[i] = j

    return params
