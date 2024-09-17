"""FastAPI application module for handling message-based inference requests."""

from fastapi import FastAPI

from coophive.seller import Seller

# FastAPI application
app = FastAPI()


@app.post("/")
async def inference_endpoint(message: dict):
    # https://github.com/CoopHive/redis-scheme-client/blob/main/src/scheme.ts#L108
    """Process a message and return the inference result."""
    seller = Seller(
        private_key="your_private_key",  # Replace with actual values or pass dynamically
        public_key="your_public_key",
        messaging_client_url="redis://localhost:6379",
        policy_name="compute_marketplace_naive_rejecter",
    )

    out_message = seller.policy.infer(message)

    return out_message
