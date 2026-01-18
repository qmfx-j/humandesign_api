from .. import features as hd
from .date_utils import to_iso_utc, clean_birth_date_to_iso

# --- Helper to process transit data ---
def process_transit_data(transit_date_timestamp, birth_timestamp, birth_place):
    # 1. Calculate birth chart to get natal features (prs + des)
    birth_features = hd.calc_single_hd_features(birth_timestamp, report=False, channel_meaning=True, day_chart_only=False)
    natal_gate_dict = birth_features[6]

    # 2. Calculate day chart (transit features only)
    day_gate_dict = hd.calc_single_hd_features(transit_date_timestamp, day_chart_only=True)
    # Round longitude to 3 decimal places for clean output
    if 'lon' in day_gate_dict:
        day_gate_dict['lon'] = [round(x, 3) for x in day_gate_dict['lon']]
    
    # 3. Prepare composite dict: Natal (prs+des) + Transit (day chart)
    # The composite analysis expects both natal and a day chart to be concatenated.
    # We explicitly select keys to merge to avoid KeyErrors (e.g., 'ch_gate')
    keys_to_merge = ["label", "planets", "lon", "gate", "line", "color", "tone", "base"]
    composite_dict = {
        key: natal_gate_dict[key] + day_gate_dict[key] 
        for key in keys_to_merge if key in natal_gate_dict and key in day_gate_dict
    }
    
    # 4. Analyze composite features
    active_channels_dict, active_chakras = hd.get_channels_and_active_chakras(composite_dict, meaning=True)
    typ = hd.get_typ(active_channels_dict, active_chakras) # The resulting 'transit' type
    auth = hd.get_auth(active_chakras, active_channels_dict) # The resulting 'transit' authority
    
    # 5. Get comparison data (New and Duplicated Channels/Chakras)
    # Refactored to avoid using hd.composite_chakras_channels which incorrectly 
    # calculates the full chart (Personality + Design) for the transit timestamp.
    # We only want to compare Composite (Natal + Transit Personality) vs Natal.
    
    # Natal features from Step 1
    # birth_features structure:
    # 0:typ, 1:auth, 2:inc_cross, 3:inc_cross_typ, 4:profile, 5:definition, 
    # 6:date_to_gate_dict, 7:active_chakras, 8:active_channels_dict
    natal_active_chakras = set(birth_features[7])
    natal_active_channels_dict = birth_features[8]

    # Calculate New Centers
    # active_chakras is the Composite set (from Step 4)
    new_centers_list = list(set(active_chakras) - natal_active_chakras)
    
    # Calculate New Channels
    # We compare the 'meaning' list (tuples of Name, Desc) or formatted strings.
    # active_channels_dict is Composite.
    
    new_channels_data = {
        "gate": [],
        "ch_gate": [],
        "meaning": []
    }
    
    # Helper to create a unique key for channels (sorted tuple of gates)
    def ch_key(g1, g2):
        return tuple(sorted((g1, g2)))

    # Get Natal Channel Keys
    natal_keys = set()
    if 'gate' in natal_active_channels_dict:
        n_gates = natal_active_channels_dict['gate']
        n_ch_gates = natal_active_channels_dict['ch_gate']
        count_n = len(n_gates)
        for i in range(count_n):
            natal_keys.add(ch_key(n_gates[i], n_ch_gates[i]))

    # Iterate Composite Channels and find new ones
    if 'gate' in active_channels_dict:
        c_gates = active_channels_dict['gate']
        c_ch_gates = active_channels_dict['ch_gate']
        c_meanings = active_channels_dict.get('meaning', [])
        
        count_c = len(c_gates)
        for i in range(count_c):
            g1 = c_gates[i]
            g2 = c_ch_gates[i]
            k = ch_key(g1, g2)
            
            if k not in natal_keys:
                # It's new!
                new_channels_data["gate"].append(g1)
                new_channels_data["ch_gate"].append(g2)
                # Handle meaning safely
                m = c_meanings[i] if i < len(c_meanings) else ("Unknown", "")
                new_channels_data["meaning"].append(m)

    # offset for birth date
    birth_offset = birth_timestamp[6] 
    
    # 6. Structure output
    return {
        "transit_date": to_iso_utc(transit_date_timestamp),
        "birth_date": clean_birth_date_to_iso(birth_features[9], birth_offset),
        "birth_place": birth_place,
        "composite_type": typ,
        "composite_authority": auth,
        "new_defined_channels": list(zip(new_channels_data["gate"], new_channels_data["ch_gate"])),
        "new_channel_meanings": new_channels_data["meaning"],
        "new_defined_centers": new_centers_list,
        "total_defined_centers": len(active_chakras),
        "raw_transit_gates": day_gate_dict
    }
