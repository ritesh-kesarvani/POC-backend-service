def shorten_name_initial(name):
    parts1 = name.split()
    parts2 = name.split("-")

    if len(parts2) > 1:
        return f"{parts2[0]} {parts2[-1][0]}."
    elif len(parts1) > 1:
        return f"{parts1[0]} {parts1[-1][0]}."
    return name