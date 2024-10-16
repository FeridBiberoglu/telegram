def is_numeric(value):
    return value.replace('.', '', 1).isdigit()

def generate_dexscreener_url(filters):
    base_url = "https://dexscreener.com/new-pairs?rankBy=trendingScoreH1&order=desc&chainIds=solana"
    
    filter_map = {
        "minLiquidity": "minLiq",
        "maxLiquidity": "maxLiq",
        "minMarketCap": "minMarketCap",
        "maxMarketCap": "maxMarketCap",
        "minFullyDilutedValuation": "minFdv",
        "maxFullyDilutedValuation": "maxFdv",
        "minAge": "minAge",
        "maxAge": "maxAge",
        "minTransactions": "min24HTxns",
        "maxTransactions": "max24HTxns"
    }
    
    additional_params = []
    
    for key, value in filters.items():
        if value and isinstance(value, str) and value.strip():
            param_key = filter_map.get(key, key)
            if is_numeric(value.strip()):
                additional_params.append(f"{param_key}={value.strip()}")
            else:
                print(f"Ignoring non-numeric value for {key}: {value}")
    
    if additional_params:
        query_string = "&".join(additional_params)
        full_url = f"{base_url}&{query_string}"
    else:
        full_url = base_url
    
    return full_url
