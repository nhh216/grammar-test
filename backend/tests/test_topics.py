"""Tests for GET /api/topics."""

import pytest


@pytest.mark.asyncio
async def test_list_topics_returns_12(client):
    resp = await client.get("/api/topics")
    assert resp.status_code == 200
    topics = resp.json()
    assert len(topics) == 12


@pytest.mark.asyncio
async def test_list_topics_schema(client):
    resp = await client.get("/api/topics")
    topic = resp.json()[0]
    assert "id" in topic
    assert "name" in topic
    assert "slug" in topic
    assert "description" in topic


@pytest.mark.asyncio
async def test_list_topics_ordered_by_name(client):
    resp = await client.get("/api/topics")
    names = [t["name"] for t in resp.json()]
    assert names == sorted(names)
