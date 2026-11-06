import requests
import scenarios

U = "http://127.0.0.1:5000"


def appeal_count():
    entries = requests.get(U + "/log").json()["entries"]
    return sum(1 for e in entries if e.get("event") == "appeal")


texts = scenarios.SCENARIOS[0]["texts"][:5]
before = appeal_count()
real_ok = 0
for i, t in enumerate(texts):
    r = requests.post(U + "/submit", json={"text": t, "creator_id": f"appeal_test_{i}"}).json()
    a = requests.post(U + "/appeal", json={"content_id": r["content_id"], "reasoning": "I wrote this myself."})
    if a.status_code == 200 and a.json().get("status") == "under_review":
        real_ok += 1
added_real = appeal_count() - before

before = appeal_count()
fake_ok = 0
for i in range(5):
    a = requests.post(U + "/appeal", json={"content_id": f"c_fake{i}", "reasoning": "test"})
    if a.status_code == 404:
        fake_ok += 1
added_fake = appeal_count() - before

print(f"real appeals ok: {real_ok}/5, log entries added: {added_real}")
print(f"fake appeals 404: {fake_ok}/5, log entries added: {added_fake}")