import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # CAZY processing

        Parses KBase HMMER App outputs into a single succinct CSV for downstream
        annotation integration, then parses the KBase HMMER Custom Model Profile
        HTML into per-organism hit tables.
        """
    )
    return


@app.cell
def _():
    from pandas import DataFrame, concat
    from glob import glob
    return DataFrame, concat, glob


@app.cell
def _(DataFrame, concat, glob):
    _dfs = []
    for _hits_path in glob("HMMER_output_TAB/*.txt"):
        with open(_hits_path, "r") as _fh:
            _lines = _fh.readlines()
        _newLines = []
        for _line in _lines:
            if any(_x in _line for _x in ["---", "[ok]", ": ", "#\n"]):
                continue
            if _line.strip() == "#":
                continue
            _newLines.append(
                _line.replace("description of target", "KBaseObj").replace(" name", "")
            )
        if not _newLines:
            continue
        _columns = [_x.strip() for _x in _newLines[0].split()][1:]
        _rows = [[_x.strip() for _x in _l.split()] for _l in _newLines[1:]]
        if not _rows:
            continue
        _dfs.append(DataFrame(_rows, columns=_columns))

    totDF = concat(_dfs, ignore_index=True)
    totDF.to_csv("CAZY_H100_hits.csv", index=False)
    print(f"wrote CAZY_H100_hits.csv: {totDF.shape[0]} rows x {totDF.shape[1]} cols")
    totDF
    return (totDF,)


@app.cell
def _(totDF):
    totDF.columns
    return


@app.cell
def _(mo):
    mo.md("# Process the CAZY HTML output into a CSV")
    return


@app.cell
def _():
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(
        open("KBase HMMER Custom Model Profile.html", "r").read(), "html.parser"
    )
    return (soup,)


@app.cell
def _(mo):
    mo.md("## parse the labels")
    return


@app.cell
def _(soup):
    _horizontal_rows = soup.find_all(class_="horz-text")
    organisms = []
    for _content in _horizontal_rows:
        _label = _content.find("nobr")
        if _label is None:
            continue
        organisms.append(_label.text.replace(".gbff_genome.RAST", ""))

    _vertical_cols = soup.find_all(class_="vertical-text")
    features = []
    for _content in _vertical_cols:
        _label = _content.find("nobr")
        if _label is None:
            continue
        features.append(_label.text.replace("\n", ""))
    print(f"{len(organisms)} organisms, {len(features)} CAZy features")
    return features, organisms


@app.cell
def _(mo):
    mo.md("## parse the # hits from each cell")
    return


@app.cell
def _(soup):
    _rows = soup.find_all("tr")
    elements = {}
    for _rowIndex, _row in enumerate(_rows):
        if _rowIndex < 2:
            continue
        _label = _row.find("nobr")
        if _label is None:
            break
        _label = _label.text.replace(".gbff_genome.RAST", "")
        elements[_label] = []
        _first = True
        for _td in _row.find_all("td"):
            if _first:
                _first = False
                continue
            _hits = _td.get("title")
            if _hits is None:
                _hits = "0"
            elements[_label].append(_hits)
    print(f"parsed hit cells for {len(elements)} organism rows")
    return (elements,)


@app.cell
def _(mo):
    mo.md("# DataFrame creation")
    return


@app.cell
def _(DataFrame, elements, features):
    from re import search
    from json import dump

    df_titles = DataFrame(elements, index=features).T
    df_titles.to_csv("CAZY_hits.csv")

    miniElements = {}
    for _org, _hits in elements.items():
        _hitsSet = set(_hits)
        _hitsSet.discard("0")
        miniElements[_org] = list(_hitsSet)
    dump(miniElements, open("nonZeroHits.json", "w"), indent=3)

    df_numeric = DataFrame(
        {
            _org: [
                search(r"(\d+)(?= hit)", _h).group() if "hit" in _h else "0"
                for _h in _hits
            ]
            for _org, _hits in elements.items()
        },
        index=features,
    ).T
    df_numeric.to_csv("CAZY_hits_numerical.csv")
    print(
        f"wrote CAZY_hits.csv ({df_titles.shape}), "
        f"CAZY_hits_numerical.csv ({df_numeric.shape}), "
        f"nonZeroHits.json"
    )
    df_numeric
    return df_numeric, df_titles, miniElements


if __name__ == "__main__":
    app.run()
