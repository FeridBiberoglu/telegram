import asyncio
import logging
import os
from datetime import datetime, timezone
from typing import List, Optional, Any
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Body
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from address import get_dexscreener_data, DEFAULT_URL
from config import config
from fastapi.middleware.cors import CORSMiddleware
from url import generate_dexscreener_url
import random 
import httpx
import sys

from telegram_bot import send_telegram_message, run_telegram_bot

ALERT_MESSAGES = [
    "🎯 ProfitSniffer Bullseye: {count} new target(s) acquired. Aim for profits!",
    "🚀 {count} token(s) are skyrocketing into your criteria!",
    "💎 {count} coin(s) are shining like diamonds and fit your filter!",
    "🔔 Alert! {count} token(s) have triggered your notification!",
    "📈 {count} cryptocurrencie(s) are now on an upward trend, matching your needs!",
    "🕵️ {count} coin(s) are now on your radar, detective!",
    "🔍 {count} token(s) meet your detailed search criteria!"
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncIOMotorClient(config.MONGODB_URL)
db = client[config.MONGODB_DB_NAME]

users_collection = db.users
tokens_collection = db.tokens
user_token_sets_collection = db.user_token_sets

class UserFilters(BaseModel):
    telegram_id: str

class Token(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    address: str
    chain: str
    name: Optional[str]
    symbol: Optional[str]
    price_usd: Optional[float]
    liquidity_usd: Optional[float]
    volume_24h: Optional[float]
    image_url: Optional[str]
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

scheduler = AsyncIOScheduler(job_defaults={'max_instances': 1})

@app.on_event("startup")
async def startup_event():
    logger.info("Starting ProfitSniffer API. Initializing scheduler...")
    scheduler.add_job(scheduled_fetch_tokens, IntervalTrigger(minutes=1), max_instances=1)
    scheduler.start()
    
    # Start the Telegram bot
    asyncio.create_task(run_telegram_bot())

@app.get("/")
async def root():
    return {"message": "Welcome to ProfitSniffer API"}

@app.post("/users/")
async def create_user(user: UserFilters):
    try:
        if not user.telegram_id:
            raise HTTPException(status_code=400, detail="telegram_id is required")

        existing_user = await users_collection.find_one({"telegram_id": user.telegram_id})
        if existing_user:
            return {"telegram_id": existing_user["telegram_id"], "message": "User already exists"}

        default_url = DEFAULT_URL
        token_set = await user_token_sets_collection.insert_one({
            "token_ids": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        })

        user_dict = {
            "telegram_id": user.telegram_id,
            "dexscreener_url": default_url,
            "token_set_id": token_set.inserted_id,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }

        result = await users_collection.insert_one(user_dict)
        logger.info(f"New user created with telegram_id: {user.telegram_id}")
        return {
            "telegram_id": user.telegram_id,
            "message": "User created successfully"
        }

    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

class Filters(BaseModel):
    minLiquidity: Optional[str] = None
    maxLiquidity: Optional[str] = None
    minMarketCap: Optional[str] = None
    maxMarketCap: Optional[str] = None
    minFullyDilutedValuation: Optional[str] = None
    maxFullyDilutedValuation: Optional[str] = None
    minAge: Optional[str] = None
    maxAge: Optional[str] = None
    minTransactions: Optional[str] = None
    maxTransactions: Optional[str] = None

@app.put("/users/{telegram_id}/filters")
async def update_user_filters(telegram_id: str, filters: Filters):
    try:
        user = await users_collection.find_one({"telegram_id": telegram_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_url = generate_dexscreener_url(filters.dict(exclude_none=True))

        update_data = {
            "dexscreener_url": new_url,
            "updated_at": datetime.now(timezone.utc)
        }

        update_result = await users_collection.update_one(
            {"telegram_id": telegram_id},
            {"$set": update_data}
        )

        updated_user = await users_collection.find_one({"telegram_id": telegram_id})
        url = updated_user.get("dexscreener_url", DEFAULT_URL)
        
        logger.info(f"Updated filters for user {telegram_id}")
        return {"message": "Filters updated successfully", "url": url} if update_result.modified_count > 0 else {"message": "No changes were made to filters", "url": url}
    except Exception as e:
        logger.error(f"Error in update_user_filters: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/fetch_tokens/{telegram_id}")
async def fetch_tokens(telegram_id: str):
    try:
        user = await users_collection.find_one({"telegram_id": telegram_id})
        if not user:
            return {"message": "User not found", "token_count": 0}

        if "token_set_id" not in user:
            token_set = await user_token_sets_collection.insert_one({
                "token_ids": [],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            })
            await users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"token_set_id": token_set.inserted_id}}
            )
            user["token_set_id"] = token_set.inserted_id

        url = user.get("dexscreener_url")
        pairs = await get_dexscreener_data(url)

        if not pairs:
            # Clear the token set if no tokens match the current filters
            await user_token_sets_collection.update_one(
                {"_id": user["token_set_id"]},
                {"$set": {"token_ids": [], "updated_at": datetime.now(timezone.utc)}}
            )
            return {"message": "No tokens match the current filters", "token_count": 0}

        # Get the current token set
        current_token_set = await user_token_sets_collection.find_one({"_id": user["token_set_id"]})
        current_token_ids = set(current_token_set.get("token_ids", []))

        new_token_ids = []
        for pair in pairs:
            token_data = {
                "address": pair['baseToken']['address'],
                "chain": pair['chainId'],
                "name": pair['baseToken']['name'],
                "symbol": pair['baseToken']['symbol'],
                "price_usd": float(pair['priceUsd']) if pair['priceUsd'] is not None else None,
                "liquidity_usd": float(pair['liquidity']['usd']) if 'liquidity' in pair and 'usd' in pair['liquidity'] else None,
                "volume_24h": float(pair['volume']['h24']) if 'volume' in pair and 'h24' in pair['volume'] else None,
                "image_url": pair.get('imageUrl'),
                "updated_at": datetime.now(timezone.utc)
            }
            
            result = await tokens_collection.update_one(
                {"address": token_data["address"], "chain": token_data["chain"]},
                {"$set": token_data},
                upsert=True
            )
            
            if result.upserted_id:
                new_token_ids.append(str(result.upserted_id))
            else:
                token = await tokens_collection.find_one({"address": token_data["address"], "chain": token_data["chain"]})
                new_token_ids.append(str(token["_id"]))

        # Determine truly new tokens
        new_token_ids_set = set(new_token_ids)
        truly_new_tokens = new_token_ids_set - current_token_ids

        # Update the token set with all fetched tokens
        await user_token_sets_collection.update_one(
            {"_id": user["token_set_id"]},
            {
                "$set": {
                    "token_ids": list(new_token_ids_set),
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )

        added_token_count = len(truly_new_tokens)

        if added_token_count > 0:
            message = random.choice(ALERT_MESSAGES).replace("{count}", str(added_token_count))
            await send_telegram_message(telegram_id, message)

        logger.info(f"Fetched tokens for user {telegram_id}: {len(pairs)} total, {added_token_count} new")
        return {"telegram_id": telegram_id, "token_count": len(pairs), "new_tokens_added": added_token_count}
    except httpx.TimeoutException:
        logger.error(f"Timeout occurred while fetching tokens for user {telegram_id}")
        return {"message": "Service temporarily unavailable, please try again later", "token_count": 0}
    except Exception as e:
        logger.error(f"Error in fetch_tokens for user {telegram_id}: {str(e)}", exc_info=True)
        return {"message": f"Error fetching tokens: {str(e)}", "token_count": 0}

@app.get("/token_sets/{user_id}")
async def get_token_set(user_id: str):
    try:
        user = await users_collection.find_one({"telegram_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        token_set = await user_token_sets_collection.find_one({"_id": user.get("token_set_id")})
        if token_set:
            token_set["_id"] = str(token_set["_id"])
            token_ids = token_set["token_ids"]
            
            tokens = await tokens_collection.find({"_id": {"$in": [ObjectId(id) for id in token_ids]}}).to_list(None)

            tokens = [{**token, "_id": str(token["_id"])} for token in tokens]
            
            return {
                "user_id": str(user["_id"]),
                "telegram_id": user_id,
                "tokens": tokens,
                "created_at": token_set["created_at"],
                "updated_at": token_set["updated_at"]
            }
        
        return {"message": "No token set found for this user"}
    except Exception as e:
        logger.error(f"Error in get_token_set: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def cleanup_tokens():
    logger.info("Starting token cleanup process")
    try:
        # Get all token sets
        all_token_sets = await user_token_sets_collection.find().to_list(None)
        
        # Collect all token IDs from all token sets
        all_token_ids = set()
        for token_set in all_token_sets:
            all_token_ids.update(token_set.get('token_ids', []))
        
        # Convert string IDs to ObjectId
        all_token_ids = set(ObjectId(token_id) for token_id in all_token_ids)
        
        # Find tokens that are not in any token set
        tokens_to_remove = await tokens_collection.find(
            {"_id": {"$nin": list(all_token_ids)}}
        ).to_list(None)
        
        if tokens_to_remove:
            result = await tokens_collection.delete_many(
                {"_id": {"$in": [token['_id'] for token in tokens_to_remove]}}
            )
            logger.info(f"Removed {result.deleted_count} tokens that were not in any token set")
        else:
            logger.info("No tokens to remove")
    
    except Exception as e:
        logger.error(f"Error in cleanup_tokens: {str(e)}", exc_info=True)

async def scheduled_fetch_tokens():
    logger.info("Starting scheduled token fetch")
    try:
        users = await users_collection.find().to_list(length=None)
        total_users = len(users)

        users_per_minute = 300
        batch_size = 30
        num_batches = (users_per_minute + batch_size - 1) // batch_size

        for i in range(0, min(total_users, users_per_minute), batch_size):
            batch = users[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1} of {num_batches}")
            
            # Add a timeout to the fetch_tokens_safe function
            async def fetch_tokens_safe_with_timeout(telegram_id: str):
                try:
                    return await asyncio.wait_for(fetch_tokens_safe(telegram_id), timeout=50)  # 50 seconds timeout
                except asyncio.TimeoutError:
                    logger.error(f"Timeout fetching tokens for user {telegram_id}")
                    return None

            tasks = [fetch_tokens_safe_with_timeout(user['telegram_id']) for user in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for user, result in zip(batch, results):
                if isinstance(result, Exception):
                    logger.error(f"Error fetching tokens for user {user['telegram_id']}: {str(result)}")
            
            if i + batch_size < min(total_users, users_per_minute):
                await asyncio.sleep(60 / num_batches)

        await cleanup_tokens()

        logger.info("Finished scheduled token fetch and cleanup")
    except Exception as e:
        logger.error(f"Error in scheduled_fetch_tokens: {str(e)}", exc_info=True)

async def fetch_tokens_safe(telegram_id: str):
    try:
        return await fetch_tokens(telegram_id)
    except Exception as e:
        logger.error(f"Error fetching tokens for user {telegram_id}: {str(e)}")
        return None

@app.get("/tokens/{token_id}")
async def get_token(token_id: str):
    try:
        token = await tokens_collection.find_one({"_id": ObjectId(token_id)})
        if token:
            token["_id"] = str(token["_id"])
            return token
        raise HTTPException(status_code=404, detail="Token not found")
    except Exception as e:
        logger.error(f"Error in get_token: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the ProfitSniffer API...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
