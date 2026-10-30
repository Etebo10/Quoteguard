from app.services.groq_client import client


def test_groq_connection():

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: QuoteGuard AI online",
            }
        ],
        temperature=0,
    )

    content = response.choices[0].message.content

    assert content is not None
    assert "QuoteGuard AI online" in content