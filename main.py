import requests
import bs4


def main(username: str, password: str):
    data = dict()
    session = requests.Session()
    with session.get("https://dienynas.tamo.lt/Prisijungimas/Login") as r:
        assert r.status_code == 200
        first_soup = bs4.BeautifulSoup(r.text, "html.parser")

    for i in first_soup.find_all("input"):
        key = i.get("id")
        if key is None:
            key = i.get("name")
        value = i.get("value")
        if key is not None and value is not None:
            data[key] = value
    data["UserName"] = username
    data["Password"] = password
    with session.post("https://dienynas.tamo.lt/?clickMode=True", data=data) as r:
        assert r.status_code == 200
    with session.get("https://dienynas.tamo.lt/Darbai/NamuDarbai") as r:
        assert r.status_code == 200
        soup = bs4.BeautifulSoup(r.text, "html.parser")
    lines = []
    # data
    for i in soup.find_all(style="font-size:1.3em;font-weight:bold"):
        lines.append((i.text.strip(), i.sourceline))
    # dalykas
    for i in soup.find_all(style="font-size:1.5em;font-weight:bold;color:#3F6877;margin-bottom:5px"):
        lines.append(("\t" + i.text.strip().replace("\n", "\n\t"), i.sourceline))
    # namu darbas
    for i in soup.find_all(class_="col-md-13 col-md-offset-1"):
        lines.append(("\t\t" + i.text.strip().replace("\n", "\n\t\t"), i.sourceline))

    lines.sort(key=lambda x: x[1])
    output = "\n".join(i for i, _ in filter(lambda x: x[0].strip() != "", lines))
    session.close()
    return output


if __name__ == "__main__":
    # situs reikia pakeisti savo tikru tamo username ir password
    main_output = main("USERNAME", "PASSWORD")
    if main_output == "":
        print("No homework")
    else:
        print(main_output)
    # lengviausias butas uztikrint kad window iskart neuzsidarys
    input()
