# def test_create_and_redirect(client):
#     response = client.post(
#         "/links/shorten",
#         json={"original_url": "https://example.com"}
#     )
#     assert response.status_code == 200
#     short_code = response.json()["short_code"]
#
#     response = client.get(f"/{short_code}", follow_redirects=False)
#     assert response.status_code == 302
#     assert response.headers["location"] == "https://example.com"