import re
import xml.etree.ElementTree as ET
from time import sleep

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

convert_usd_to_rub = lambda amount: get_currency_rate_cbr() or get_currency_rate_exc() or 90.0


def get_currency_rate_cbr(char_code_currency="USD"):
    """
    :param char_code_currency: can see here - https://www.cbr.ru/scripts/XML_daily.asp
    :return: float_number
    """
    try:
        return float(
            ET.fromstring(requests.get("https://www.cbr.ru/scripts/XML_daily.asp").text)
            .find(f"./Valute[CharCode='{char_code_currency}']/Value")
            .text.replace(",", ".")
        )
    except Exception:
        return None


def get_currency_rate_exc():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return float(data["rates"]["RUB"])
    except Exception:
        return None


def parse_car_data(url: str):
    s = requests.Session()
    headers = {"User-Agent": UserAgent().chrome}
    cookies = {
        "bm_sz": "ACEEE69C7E22483DE9ED09F8B9657364~YAAQhAVJF7CtnNyLAQAAs6zgPxZRJqa/y8zZ+O07mp1AJQSHI1hL4/3NY1Q3G91HfTYx2P5YuE/a7Jtn5aNpynSZdB8ZCFseBkIYiMBTfOH/98ofSmgdvpVBIUxVXayKQg634UNxdLsUVAF/HuQmFxxjM1EYgSJBghzkW9gCblPvAkTyh2CSZHf1zhaBCSWzBf1KI74LxNlv/NU33ndIWYcB3RB/BLHAEQuVj6pOrQBqP7Nw+FCRBHozyixn7krrhFF51Z+EIqgg2gxUsXC3saUKtX6f16g+DQ+bKGDJMz3DFA==~4534594~4469047",
        "FPLC": "jNjj15/SuKsksQJ3N+gp5foVcHmcHGE2qbdLN0mE4QgJq8TAjOyJ49hLlIUPcz5Vb0WNWRE2KJ6DrIKqOu5lbIhwlGD+3MPvgltq3SiAwj5OtlIB2aSmuW04vC8S/Q==",
        "mobile.LOCALE": "de",
        "bm_mi": "AC05CCE9C8AA0ACBDAEE260DC58D8470~YAAQhAVJF5iunNyLAQAAubrgPxYyPAiDbYnjiyNDZuNN1HZopsHF5Is21NK5CiRMLeHsrWJJBF4LFHJna95XrsK8OKlRGomJfG3RmB+HhdWt815rh2DtMSfPqcfjs6lt2WQ45dpNwtJp4L74BCu77l0xV2awKW+g45zsd/Nz9N+PvmK0MoXU+PRJ07FqKFqtEQcWwRakpKjk6LXIEjbamNH9dC3DogY9Hf0yzuHCzfgU/jkiPzOuoJ/u/hRpwjO6uZaweqZ68WuZz80gQiMIGrOcwErgR53Lom6bS3FwD/y/ZLyKiZvN5c+QBsjuX0iYBx2lTd2YDtcVqsCqIQi76+IB~1",
        "optimizelyEndUserId": "oeu1701878742016r0.252333741334152",
        "ces": "-",
        "ak_bmsc": "CAD84008C8C778835867928944F4AFDC~000000000000000000000000000000~YAAQhAVJF/8YndyLAQAAyZDmPxb6geEZaNud8x6oH3VIxwABE1Nb8b1Gh6D839wBQ1VtQW75qSZHC7XQ7fMHcukIoKPKtJApL8FRNOEdYqFsxTjAkHK5SF63smApaKnRgLYflMOKS1PkwV7swxRFozMXVzenhh1re9sqX+MKIsK/HMpWejJNhrXDZnve3EwWxNQENyOqrDqlVpYGZeWaPbLVjJh3BJ9bDJWGZSv8FMxJ3cHogS/hxan6v4ybgccj8nTcxVnTEaVs8GnfuheVAKGA3lhz0o3eknp/JpPk13l6Vkq4IUwAqUWhCPdVbZhL3xhhZNVx/F+WNfnt48rZdyhG6LlzXPeE79DR1oRs083Qd1H0ryN6VXSxLs+cdmIRYXCNJnM1w0ABHYPZagnok1rbMdctVwm8YwJ8Q23m653wI7wkNM/DPEQAmbyRxBf/dCusyaza/jTn2o6L+3DEv1a9XVwxW7RNJ442lBbEpxK9WwWWm97zbqdhmapmsIcJ78+9sET+8sAuPkx5uciZsgPWLD3kAshtVUkhpTCRyq8mogJp2R4zh8JTQdTiHuFZdNxpAARnGXWdHlVH8Z1cmqtxgjibxadEkVxv2dxLQzwoYeba2niKOGIb1UNJz7o7m68UpKH+Qx11TmMhIQAlb3YzRnAWi611kHY15lOYSD/JagOyvQ==",
        "_abck": "1E5E9CBFA45E8E9558469038BCDB3CB0~0~YAAQhAVJF1MZndyLAQAA4ZXmPwt5uAlx2Z3xfzdLCFr0g2c1YfonMYaUOJ79lH46H6Z4NdbQIPzLEDv0uVP9plVNt8YElDmFfM/98hnInDr/dnnmqBL1f6oqb/s0rzNJcwGdFY8mS3twJpaPfhahAToBP7B9jioqRNSuC96xF9xAfgvmffz1HPlgs0Qta4UkSaKu+F2Q5wgBJ3ZImB9MJRnuSMqz767yNvGLnGnfZ3OztPo9Di8lZHmWusOh2BpGjh3LybTmdYT4TL/YMtLSNf3rbOyqPBaTOyQN9NhZioNq832wx/gghd3p0Ji3U3/Iu1TFa9csYGjm4MX1g4/S41lQfJAtR8CyxdGvQcmjOqDVOWi4nG6Z2GvwAO3DyK0PtEbNmthHQfm6Zt6dCGTKBbM4e9S8bok=~-1~-1~-1",
        "AMP_067b9b07c8": "JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIwZmE0YWVhNi02ZDc0LTQzYTYtOGIxMy0yMWYzOWM3MmI0YjQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNjk2MTkxMDI0MzkyJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlN0Q=",
        "mdeConsentDataGoogle": "1",
        "mdeConsentData": "CP2ZKiRP2ZKiREyAHADEAdEgAP_gAELAAAYgJepV5DzdbWFBcXp3aPswOY0X1tDTIsQhAhSAAyAFgBOQ8JQA02EyNASgBiACEAAAoxZBAAEEHAFEAQCAQAAEAAHsIgAEgAAIIABEgAEQAAJYAAoKAIAgEAAIgAIFEgAAmBiQIdLkXUCAgIAACgAQAAABAIAAAgMAAAAIAAIAAAAAAgAAAAAAAAIAAAAAARAAAAAAAAAAAAAAIF5wBAAQAA0ACYAvMAYJAzAAQAAsACoAHAAPAAyAB4AEQAKoAZgA3gB6AD8AIQAQ0AiACJAEcAJYATQAwABhgDuAHtAPsA_QCKAEaAJEASUAlIBcwC9AGKANoAbgBIgCdgFDgKPAUiApsBbADBgGGgMkAZOAzMBq4DWQHBAPHAhyOgbgALAAqABwAGQAPAAiABVgC4ALoAYgAzABvAD0AH4AQ0AiACJAEsAJoAUYAwABhgDRAHcAPaAfYB-gEUAIsAR0AkQBJQCUgFzgLyAvQBigDaAG4AOoAi8BIgCdgFDgKPAU2AtgBgwDDQGSAMnAZUAywBmYDVwHFgPHAgCBDkhASAAWAFUALgAYgA3gB6AEcAMAAdwBFACUgFzAMUAbQA6gC0QGTgPHJQGAAEAALAA4ADwAIgAVQAuABiAENAIgAiQBHACjAGAAPwAuYBigDqAIvASIAo8BbADJAGTgQBKQKgAFgAVAA4ADIAHgARAApABVADEAGYAPwAhoBEAESAKMAYAA0YB-AH6ARYAjoBIgCSgEpALmAXkAxQBtADcAHUAReAkQBOwChwFNgLYAYaAyQBk4DLAGsgOCAeOBDktAGAEcAMAAdwBegGZgPHA.YAAAAAAAD4AAAKcAAAAA",
        "bm_sv": "BE615AB5F36DC409DDD02BD2E8D15CA4~YAAQhAVJFxcandyLAQAAD6LmPxYxNYqEluw+PB9q+PLEN+c6HQA1i7emvOdWpd+6wcqfFg9hL/r3/2xzXDvSgK4RhfmQ+X3JjYHeo7k+5XHcISfwi4khzd62fiEI5j1LwVV5jWUgDntpEGtqLpFvgRC5OqD/EqgmPiXX3nt3fCBQXQ6MzrFDDR5NF3hHONgVtnYYHR7uYrjSwNBbz+XYn6xg/w9HEoIchTlwhyTh2Y/enJGJlkSlGeUecWWF8DMV~1",
        "lux_uid": "170187912863263781",
        "_gid": "GA1.2.954571687.1701879129",
        "_gat_UA-3584729-32": "1",
        "_gcl_au": "1.1.404145772.1701879129",
        "_ga": "GA1.1.1858185808.1701879129",
        "_ga_2H40T2VTNP": "GS1.1.1701877848.7.1.1701879128.0.0.0",
        "iom_consent": "0107ff0000&1701879129007",
        "ioam2018": "0019a0977cb97b43565709d58:1730823129009:1701879129009:.mobile.de:2:mobile:DE/DE/OB/S/P/D/D:noevent:1701879129009:etqzsa",
        "_uetsid": "d472f460939011ee8c7903337aaff7f1|gb0nf6|2|fhb|0|1434",
        "dicbo_id": "{\"dicbo_fetch\":1701879129559}",
        "_uetvid": "54758d208c6c11eeaa4963873241364b|l0wj11|1701879129644|4|1|bat.bing.com/p/insights/c/x"
    }
    r = s.get(url, headers=headers, allow_redirects=True, cookies=cookies)
    res = r.text
    with open("o.html", "w") as f:
        f.write(res)

    soup = BeautifulSoup(res, "html.parser")

    # Parse price
    price_span = soup.find("span", {"class": "h3", "data-testid": "prime-price"})
    if price_span:
        price_text = price_span.text
        price = int(re.sub(r"[^\d,]", "", price_text).replace(",", "."))

    # Parse first image
    image_div = soup.find("div", {"class": "gallery-img-wrapper"})
    if image_div:
        image = image_div.find("img")
        if image:
            image_url = image["src"]

    title_div = soup.find("div", {"class": "listing-title"})
    if title_div:
        title_h1 = title_div.find("h1", {"id": "ad-title"})
        if title_h1:
            title = title_h1.text

    # Parse technical data
    tech_data_div = soup.find("div", {"id": "td-box"})
    if tech_data_div:
        tech_data_rows = tech_data_div.find_all("div", {"class": "g-row"})
        tech_data = {}
        for row in tech_data_rows:
            key_div = row.find("div", {"class": "g-col-6"})
            value_div = row.find("div", {"id": key_div["id"] + "-v"})
            if key_div and value_div:
                key = key_div.text.strip()
                if key in ["CO₂-Effizienz", "HU", "Umweltplakette"]:
                    continue
                value = value_div.text.strip()
                tech_data[key] = value

    data = {
        "price": price,
        "image_url": image_url,
        "title": title,
        "tech_data": tech_data,
    }

    return data
