import json, os, sys, urllib.request, datetime
USER = os.environ.get("GH_USER", "priyanshumakes")
Q = "query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{weeks{contributionDays{contributionCount date weekday}}}}}}"
def fetch():
    if len(sys.argv) > 1: return json.load(open(sys.argv[1]))
    req = urllib.request.Request("https://api.github.com/graphql", json.dumps({"query": Q, "variables": {"u": USER}}).encode(),
        {"Authorization": "bearer " + os.environ["GITHUB_TOKEN"], "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))
weeks = fetch()["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"][-53:]
counts = [c for w in weeks for c in [d["contributionCount"] for d in w["contributionDays"]] if c]
mx = max(counts) if counts else 1
def lv(n):
    if n == 0: return 0
    r = n / mx
    return 1 if r <= .25 else 2 if r <= .5 else 3 if r <= .75 else 4
cols = len(weeks); cell, gap, ox, oy = 11, 3, 14, 14; st = cell + gap
pal = ["#1a1426", "#3b1d63", "#6d28d9", "#a855f7", "#35c4df"]
W = ox * 2 + cols * st; H0 = oy * 2 + 7 * st; H = H0 + 22; T = 8.0
span = W - 2 * ox - 18
cat = "".join(f'<rect x="{a*2}" y="{b*2}" width="{w*2}" height="2" fill="#35c4df"/>' for a, b, w in [(1,0,1),(5,0,1),(1,1,5),(0,2,7),(0,3,7),(0,4,7),(1,5,6),(1,6,1),(3,6,1),(5,6,1),(7,2,1),(8,1,1),(8,0,1)])
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>Contribution graph with a pixel cat walking across</title><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="#0e1117" stroke="#302044"/>']
css = f".cat{{animation:w {T}s linear infinite}}@keyframes w{{0%{{transform:translateX({ox}px)}}100%{{transform:translateX({W-ox-18}px)}}}}@keyframes b{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-2px)}}}}.bob{{animation:b .4s steps(1) infinite}}"
cells = []
for x, w in enumerate(weeks):
    d = x * st / span * T; p = max(d / T * 100 - .5, 0)
    css += f"@keyframes cw{x}{{0%,{p:.2f}%{{opacity:.3}}{d/T*100:.2f}%,85%{{opacity:1}}100%{{opacity:.3}}}}"
    for y, day in enumerate(w["contributionDays"]):
        l = lv(day["contributionCount"]); rx_, ry_ = ox + x * st, oy + y * st
        a = f' style="animation:cw{x} {T}s linear infinite"' if l else ""
        cells.append(f'<rect x="{rx_}" y="{ry_}" width="{cell}" height="{cell}" rx="2" fill="{pal[l]}"{a}/>')
o.append(f"<style>{css}</style>" + "".join(cells))
o.append(f'<g transform="translate(0,{H0-6})"><g class="cat"><g class="bob">{cat}</g></g></g></svg>')
open("cat-graph.svg", "w").write("".join(o))
print("wrote cat-graph.svg", W, H, "weeks", cols)
