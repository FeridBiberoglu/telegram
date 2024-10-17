import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
import sys
import json
import os
from aiohttp import ClientError
import traceback
from app.config import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVED_DATA_PATH = os.path.join(SCRIPT_DIR, 'saved_data.json')

DEFAULT_URL = "https://dexscreener.com/new-pairs?rankBy=trendingScoreH1&order=desc&chainIds=solana"

def load_saved_data():
    if os.path.exists(SAVED_DATA_PATH):
        with open(SAVED_DATA_PATH, 'r') as f:
            data = json.load(f)
            return data.get('cf_clearance', ''), data.get('user_agent', '')
    return '', ''

def save_data(cf_clearance, user_agent):
    data = {'cf_clearance': cf_clearance, 'user_agent': user_agent}
    with open(SAVED_DATA_PATH, 'w') as f:
        json.dump(data, f, indent=2)

cf_clearance, user_agent = load_saved_data()

async def get_cf_clearance():
    try:
        payload = {"url": "https://dexscreener.com", "mode": "waf-session"}
        async with aiohttp.ClientSession() as session:
            async with session.post(config.SCRAPER_URL, json=payload, timeout=360) as response:
                if response.status != 200:
                    raise ClientError(f"Scraper returned status code {response.status}")

                json_content = await response.json()

                cf_clearance = next((cookie['value'] for cookie in json_content.get('cookies', []) if cookie['name'] == 'cf_clearance'), None)
                user_agent = json_content.get('headers', {}).get('user-agent')
                
                if not cf_clearance or not user_agent:
                    raise ValueError("Missing cf_clearance or user_agent in JSON response")
                
                save_data(cf_clearance, user_agent)
                return cf_clearance, user_agent
    except Exception as e:
        logger.error(f"Error in get_cf_clearance: {e}")
        raise

def update_global_cookies_and_user_agent(new_cookie, new_user_agent):
    global cf_clearance, user_agent
    cf_clearance = new_cookie
    user_agent = new_user_agent
    save_data(cf_clearance, user_agent)

async def get_dexscreener_links(session, url=None):
    global cf_clearance, user_agent

    if not url:
        url = DEFAULT_URL
    logger.info(f"Fetching links from {url}")
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'TE': 'trailers',
    }

    cookies = {'cf_clearance': cf_clearance}

    retries = 3
    backoff_factor = 2

    for attempt in range(retries):
        try:
            await asyncio.sleep(2)
            logger.info(f"Attempt {attempt + 1} to fetch links")
            async with session.get(url, headers=headers, cookies=cookies, timeout=10) as response:
                logger.info(f"Response status code: {response.status}")
                if response.status == 200:
                    content = await response.text()
                    logger.info(f"Response content length: {len(content)}")
                    soup = BeautifulSoup(content, 'html.parser')
                    logger.info(f"BeautifulSoup object created")
                    rows = soup.find_all('a', class_='ds-dex-table-row ds-dex-table-row-new')
                    logger.info(f"Found {len(rows)} rows with class 'ds-dex-table-row ds-dex-table-row-new'")
                    
                    pair_addresses = []
                    for row in rows[:30]:
                        href = row.get('href')
                        if href:
                            pair_address = href.split('/')[-1]
                            pair_addresses.append(pair_address)
                    
                    logger.info(f"Extracted {len(pair_addresses)} pair addresses")
                    return pair_addresses
                elif response.status == 403:
                    logger.info("403 error, getting new cf_clearance")
                    new_cookie, new_user_agent = await get_cf_clearance()
                    update_global_cookies_and_user_agent(new_cookie, new_user_agent)
                    headers['User-Agent'] = user_agent
                    cookies['cf_clearance'] = cf_clearance
                    logger.info(f"Updated cf_clearance: {cf_clearance[:10]}... (truncated)")
                    logger.info(f"Updated user_agent: {user_agent}")
                    continue
                else:
                    logger.error(f"Unexpected status code: {response.status}")
                    if attempt < retries - 1:
                        sleep_time = backoff_factor ** attempt
                        logger.info(f"Sleeping for {sleep_time} seconds before next attempt")
                        await asyncio.sleep(sleep_time)
                    else:
                        logger.error("All attempts failed")
                        return []
        except Exception as e:
            logger.error(f"Error in get_dexscreener_links: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            if attempt < retries - 1:
                sleep_time = backoff_factor ** attempt
                logger.info(f"Sleeping for {sleep_time} seconds before next attempt")
                await asyncio.sleep(sleep_time)
            else:
                logger.error("All attempts failed due to exceptions")
                return []

    logger.error("All attempts to get dexscreener links failed")
    return []

async def get_token_info(session, pair_addresses):
    logger.info(f"get_token_info called with {len(pair_addresses)} addresses")
    base_url = "https://api.dexscreener.com/latest/dex/pairs/solana/"
    url = f"{base_url}{','.join(pair_addresses)}"
    
    try:
        async with session.get(url, timeout=30.0) as response:
            logger.info(f"Response status code: {response.status}")
            response.raise_for_status()
            data = await response.json()
            
            if 'pairs' in data and data['pairs'] is not None:
                all_tokens = []
                for pair in data['pairs']:
                    token_info = {
                        'chainId': pair['chainId'],
                        'pairAddress': pair['pairAddress'],
                        'baseToken': {
                            'address': pair['baseToken']['address'],
                            'name': pair['baseToken']['name'],
                            'symbol': pair['baseToken']['symbol']
                        },
                        'quoteToken': pair['quoteToken'],
                        'priceUsd': pair.get('priceUsd'),
                        'liquidity': pair.get('liquidity', {}),
                        'volume': pair.get('volume', {}),
                        'imageUrl': pair.get('info', {}).get('imageUrl')  # Add this line to include the image URL
                    }
                    all_tokens.append(token_info)
                logger.info(f"Fetched {len(all_tokens)} tokens for this batch")
                return all_tokens
            else:
                logger.warning(f"No pairs found for addresses: {pair_addresses}")
                return []
    except asyncio.TimeoutError:
        logger.error(f"Timeout occurred while fetching data for batch")
    except aiohttp.ClientResponseError as e:
        logger.error(f"HTTP error occurred: {e}")
    except Exception as e:
        logger.error(f"An error occurred while fetching data: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
    
    return []

async def get_dexscreener_data(url=None):
    async with aiohttp.ClientSession() as session:
        pair_addresses = await get_dexscreener_links(session, url)
        logger.info(f"Retrieved {len(pair_addresses)} pair addresses")
        
        batch_size = 30  # API limit
        
        async def fetch_batch(batch):
            return await get_token_info(session, batch)
        
        tasks = [fetch_batch(pair_addresses[i:i+batch_size]) 
                 for i in range(0, len(pair_addresses), batch_size)]
        
        logger.info(f"Created {len(tasks)} tasks for token info fetching")
        results = await asyncio.gather(*tasks)
        
        tokens = [token for batch in results for token in batch]
        logger.info(f"Total tokens fetched: {len(tokens)}")
        return tokens

if __name__ == "__main__":
    asyncio.run(get_dexscreener_data())
