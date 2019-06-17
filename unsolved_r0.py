#!/bin/python
DESCRIPTION = """Lists the unsolved challenges on R0 (using the given
PHPSESSID), sorted to help pick the next challenge to solve.
"""

import argparse
import collections
import re
from bs4 import BeautifulSoup
from requests import get
from tabulate import tabulate

Challenge = collections.namedtuple("Challenge",
        "id name category points solves solved")

def parse_category_name(category_text):
    """Parses something like 'Coding Challenges (17 / 17)' to only return the
    name of the category."""
    match = re.match(r'(.*?)\s*\(.*', category_text)
    assert match is not None and len(match.groups()) >= 1,\
           "Format of category header unexpected: '%s'" % category_text
    return match.groups()[0]
assert parse_category_name("Cryptography (30 / 31)") == "Cryptography"

def parse_solved(name_node):
    solved_node = name_node.find("span", class_="glyphicon")
    assert solved_node is not None,\
            ("Can't figure out if challenges are solved or not. " +
             "Are you sure you recently logged in with that PHPSESSID?")
    return "glyphicon-thumbs-up" in solved_node.attrs["class"]

def parse_name(name_node):
    return name_node.get_text().strip()

def parse_id(name_node):
    url = name_node.a.attrs["href"]
    id_str = re.match(r".*/(\d+).*", url)
    return int(id_str.groups()[0])

def parse_challenge(challenge_row, category):
    name_node, points_node, solves_node = challenge_row.find_all('td')[:3]
    solved = parse_solved(name_node)
    name = parse_name(name_node)
    id_ = parse_id(name_node)
    points = int(points_node.get_text())
    solves = int(solves_node.get_text())
    return Challenge(name=name, solved=solved, id=id_, points=points,
                     solves=solves, category=category)

def parse_category(category_node):
    challenges = []
    # special handling for Web's warning
    ssl_warning = category_node.find(id="ssl")
    if ssl_warning: ssl_warning.clear()  
    category_name = parse_category_name(category_node.get_text())

    table = category_node.find_next("table").tbody.extract()
    row = table.tr
    while row:
        challenges.append(parse_challenge(row, category_name))
        row = row.find_next("tr")
    return challenges

def fetch_challenges(sessid):
    r = get("https://ringzer0ctf.com/challenges", cookies={"PHPSESSID": sessid})
    assert r.status_code == 200

    challenges = []
    html = BeautifulSoup(r.text, "html.parser")
    for category in html.find_all(attrs={"data-id": True},
                                  class_="title_hover"):
        challenges.extend(parse_category(category))
    return challenges

def challenge_score(challenge, points_weight):
    multiplier = (challenge.points - 1) * points_weight
    return challenge.solves * (1.0 + multiplier)

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("phpsessid",
                        help="PHPSESSID cookie for your R0 session")
    parser.add_argument("--points-weight", type=float, default=1.0,
                        help="Weight contributed by the challenge points to " +
                              "the sorting score.")
    parser.add_argument("-n", "--max-challenges", type=int, default=10,
                        help="Max number of challenges to display. " +
                             "Set to high number to display all.")
    args = parser.parse_args()

    challenges = fetch_challenges(args.phpsessid)
    unsolved = [chal for chal in challenges if not chal.solved]
    points_weight = args.points_weight
    unsolved.sort(key=lambda chal: challenge_score(chal, points_weight),
                  reverse=True)

    display_n = args.max_challenges
    print(tabulate([[challenge_score(c, points_weight), c.name, c.id, c.solves,
                     c.points] for c in unsolved[:display_n]],
                   headers=["Score", "Name", "Id", "# Solves", "# Points"]))


if __name__ == "__main__":
    main()
