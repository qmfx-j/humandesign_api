import pytest
from fastapi.testclient import TestClient
from humandesign.api import app
from humandesign.dependencies import verify_token

# Override dependency to skip auth
def override_verify_token():
    return True

app.dependency_overrides[verify_token] = override_verify_token

client = TestClient(app)

def test_transits_metadata_v181_structure():
    """
    Verify the v1.8.1 'meta' enrichment in /transits/daily.
    Checks for:
    - New Bio fields (age, gender, islive, zodiac_sign)
    - HD Core fields (energy_type, strategy, signature, etc.)
    - Centers (defined, undefined)
    - Channels (nested structure and formatting)
    """
    # Use the new default values (implied by just calling the endpoint without params, 
    # but let's be explicit to ensure we test the specific outcome we expect).
    # Wait, the requirement was to UPDATE defaults, so calling without params should work 
    # and return the 1968-02-21 data.
    
    response = client.get("/transits/daily") 
    assert response.status_code == 200
    data = response.json()
    
    meta = data.get("meta")
    assert meta is not None, "Meta object missing"
    
    # 1. Check Bio/Astrology
    assert "birth_date" in meta
    assert "create_date" in meta
    assert meta["age"] == 57 # 2025 - 1968
    assert meta["gender"] == "male"
    assert meta["islive"] is True
    assert meta["zodiac_sign"] == "Pisces"
    assert "Kirikkale" in meta["place"]
    
    # 2. Check HD Core
    assert meta["energy_type"] == "Manifesting Generator" # Known for this logic (1968-02-21 11:00)
    assert meta["strategy"] == "Wait to Respond"
    assert "Satisfaction" in meta["signature"]
    assert "Frustration" in meta["not_self"]
    assert "Emotional Authority" in meta["inner_authority"] # v1.8.0+ constant
    assert meta["profile"] == "2/4: Hermit Opportunist"
    
    # 3. Check Centers
    assert isinstance(meta["defined_centers"], list)
    assert isinstance(meta["undefined_centers"], list)
    # Check for known expected centers for this chart
    assert "Sacral" in meta["defined_centers"]
    assert "Solar Plexus" in meta["defined_centers"]
    assert "Head" in meta["undefined_centers"]
    
    # 4. Check Channels
    assert "channels" in meta
    assert "Channels" in meta["channels"]
    channels_list = meta["channels"]["Channels"]
    assert isinstance(channels_list, list)
    assert len(channels_list) > 0
    
    # Verify string format
    first_channel = channels_list[0]
    assert "channel" in first_channel
    val = first_channel["channel"]
    # Check format regex-like: "Gate/Gate: Name (Desc)"
    assert "/" in val
    assert ": " in val
    assert "(" in val
    assert ")" in val
    
    print("\nVerified Meta Structure v1.8.1 successfully.")
