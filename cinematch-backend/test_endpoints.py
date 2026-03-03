"""Quick endpoint smoke test."""
import httpx
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = "http://127.0.0.1:8002"
headers = {}

def test(label, method, path, **kwargs):
    fn = getattr(httpx, method)
    url = BASE + path
    r = fn(url, headers=headers, timeout=30.0, **kwargs)
    status = r.status_code
    body = r.json()
    tag = "PASS" if status < 400 else "FAIL"
    print(f"  [{tag}] [{status}] {label}")
    return body

print("=" * 55)
print("  CineMatch AI - Endpoint Smoke Test")
print("=" * 55)

# 1. Health
test("Health Check", "get", "/health")

# 2. Root
test("Root Info", "get", "/")

# 3. Register
tokens = test("Register User", "post", "/api/v1/auth/register", json={
    "email": "smoke@cinematch.ai",
    "username": "smoketest",
    "full_name": "Smoke Tester",
    "password": "Pass1234"
})
print(f"       -> Keys: {list(tokens.keys())}")

# 4. Login
tokens = test("Login", "post", "/api/v1/auth/login", json={
    "email": "smoke@cinematch.ai",
    "password": "Pass1234"
})
access = tokens.get("access_token", "")
refresh = tokens.get("refresh_token", "")
headers = {"Authorization": f"Bearer {access}"}
print(f"       -> Got access + refresh tokens")

# 5. Auth/Me
me = test("GET /auth/me", "get", "/api/v1/auth/me")
uname = me.get("username", "?")
role = me.get("role", "?")
tier = me.get("subscription_tier", "?")
print(f"       -> User: {uname} | Role: {role} | Tier: {tier}")

# 6. User Profile
profile = test("GET /users/me/profile", "get", "/api/v1/users/me/profile")
print(f"       -> Ratings: {profile.get('total_ratings')}")

# 7. Update Profile
updated = test("PATCH /users/me", "patch", "/api/v1/users/me", json={
    "full_name": "Smoke Tester Updated"
})
print(f"       -> Name: {updated.get('full_name')}")

# 8. DNA Profile
dna = test("GET /users/dna", "get", "/api/v1/users/dna")
arch = dna.get("archetype", "?")
print(f"       -> Archetype: {arch}")

# 9. Movies List
movies = test("GET /movies", "get", "/api/v1/movies")
print(f"       -> Count: {len(movies)}")

# 10. Refresh Token
new_tokens = test("POST /auth/refresh", "post", "/api/v1/auth/refresh", json={
    "refresh_token": refresh
})
has_new = bool(new_tokens.get("access_token"))
print(f"       -> New tokens received: {has_new}")

# 11. Hidden Gems
headers_bak = headers
headers = {}
gems = test("GET /movies/hidden-gems", "get", "/api/v1/movies/hidden-gems")
print(f"       -> Gems: {len(gems)}")
headers = headers_bak

# 12. Recommendations
recs = test("POST /recommendations", "post", "/api/v1/recommendations", json={
    "movie_title": "Interstellar",
    "mood": "emotional",
    "country_code": "IN",
    "limit": 5
})
total = recs.get("total_results", "?")
print(f"       -> Results: {total}")

# 13. Semantic Search
search = test("POST /semantic-search", "post",
              "/api/v1/recommendations/semantic-search", json={
    "query": "mind bending sci-fi",
    "limit": 5
})
results = search.get("results", [])
print(f"       -> Results: {len(results)}")

# 14. Admin (should 403)
test("GET /admin/stats (expect 403)", "get", "/api/v1/admin/stats")

print()
print("=" * 55)
print("  ENDPOINT TESTING COMPLETE!")
print("=" * 55)
