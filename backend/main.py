from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="ResolveAI",
    description="Autonomous Customer Resolution Agent",
    version="1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# WORKFLOW EVENT LOG
# ============================================================

workflow_events = []


def log_event(step, message, status="info"):
    workflow_events.append({
        "step": step,
        "message": message,
        "status": status
    })


# ============================================================
# CUSTOMER DATABASE
# ============================================================

customers = {
    "C1001": {
        "customer_id": "C1001",
        "name": "Arun Kumar",
        "email": "arun@example.com",
        "tier": "Premium"
    },

    "C1002": {
        "customer_id": "C1002",
        "name": "Priya Sharma",
        "email": "priya@example.com",
        "tier": "Standard"
    }
}


# ============================================================
# ORDER DATABASE
# ============================================================

orders = {
    "ORD1001": {
        "order_id": "ORD1001",
        "customer_id": "C1001",
        "product": "Laptop X",
        "product_id": "P1001",
        "status": "delivered",
        "issue": "damaged",
        "order_value": 65000,
        "resolution": None
    },

    "ORD1002": {
        "order_id": "ORD1002",
        "customer_id": "C1002",
        "product": "Wireless Headphones",
        "product_id": "P1002",
        "status": "delivered",
        "issue": "wrong_product",
        "order_value": 5000,
        "resolution": None
    }
}


# ============================================================
# INVENTORY
# ============================================================

inventory = {
    "P1001": {
        "product_id": "P1001",
        "product": "Laptop X",
        "available": False,
        "quantity": 0
    },

    "P1002": {
        "product_id": "P1002",
        "product": "Wireless Headphones",
        "available": True,
        "quantity": 5
    }
}


# ============================================================
# POLICIES
# ============================================================

policies = {
    "damaged": {
        "replacement_allowed": True,
        "refund_allowed": True,
        "cancellation_allowed": False,
        "description":
            "Damaged products can be replaced or refunded."
    },

    "wrong_product": {
        "replacement_allowed": True,
        "refund_allowed": True,
        "cancellation_allowed": False,
        "description":
            "Wrong products can be replaced or refunded."
    },

    "missing_item": {
        "replacement_allowed": True,
        "refund_allowed": True,
        "cancellation_allowed": False,
        "description":
            "Missing items can be replaced or refunded."
    },

    "cancellation": {
        "replacement_allowed": False,
        "refund_allowed": True,
        "cancellation_allowed": True,
        "description":
            "Eligible orders can be cancelled and refunded."
    }
}


# ============================================================
# REFUNDS
# ============================================================

refunds = {}


# ============================================================
# REPLACEMENTS
# ============================================================

replacements = {}


# ============================================================
# REQUEST MODEL
# ============================================================

class ResolveRequest(BaseModel):
    message: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "ResolveAI backend is running"
    }


# ============================================================
# WORKFLOW EVENTS
# ============================================================

@app.get("/workflow")
def get_workflow():

    return {
        "success": True,
        "events": workflow_events
    }


# ============================================================
# CUSTOMER API
# ============================================================

@app.get("/customer/{customer_id}")
def get_customer(customer_id: str):

    log_event(
        "Investigate",
        f"Checking customer {customer_id}"
    )

    customer = customers.get(customer_id)

    if not customer:

        log_event(
            "Investigate",
            f"Customer {customer_id} not found",
            "error"
        )

        return {
            "success": False,
            "error": "Customer not found"
        }

    log_event(
        "Investigate",
        f"Customer found: {customer['name']} ({customer['tier']})",
        "success"
    )

    return {
        "success": True,
        "customer": customer
    }


# ============================================================
# ORDER API
# ============================================================

@app.get("/order/{order_id}")
def get_order(order_id: str):

    log_event(
        "Investigate",
        f"Checking order {order_id}"
    )

    order = orders.get(order_id)

    if not order:

        log_event(
            "Investigate",
            f"Order {order_id} not found",
            "error"
        )

        return {
            "success": False,
            "error": "Order not found"
        }

    log_event(
        "Investigate",
        f"Order found: {order['product']} | Issue: {order['issue']}",
        "success"
    )

    return {
        "success": True,
        "order": order
    }


# ============================================================
# INVENTORY API
# ============================================================

@app.get("/inventory/{product_id}")
def get_inventory(product_id: str):

    log_event(
        "Investigate",
        f"Checking inventory for {product_id}"
    )

    product = inventory.get(product_id)

    if not product:

        log_event(
            "Investigate",
            f"Product {product_id} not found",
            "error"
        )

        return {
            "success": False,
            "error": "Product not found"
        }

    if product["quantity"] > 0:

        log_event(
            "Investigate",
            f"{product['product']} available: "
            f"{product['quantity']} units",
            "success"
        )

    else:

        log_event(
            "Investigate",
            f"{product['product']} is OUT OF STOCK",
            "warning"
        )

    return {
        "success": True,
        "inventory": product
    }


# ============================================================
# POLICY API
# ============================================================

@app.get("/policy/{issue_type}")
def get_policy(issue_type: str):

    log_event(
        "Investigate",
        f"Checking company policy for '{issue_type}'"
    )

    policy = policies.get(issue_type)

    if not policy:

        log_event(
            "Investigate",
            f"No policy found for '{issue_type}'",
            "error"
        )

        return {
            "success": False,
            "error": "Policy not found"
        }

    log_event(
        "Investigate",
        f"Policy allows replacement="
        f"{policy['replacement_allowed']}, "
        f"refund={policy['refund_allowed']}",
        "success"
    )

    return {
        "success": True,
        "issue_type": issue_type,
        "policy": policy
    }


# ============================================================
# REPLACEMENT
# ============================================================

@app.post("/replacement/{order_id}")
def create_replacement(order_id: str):

    log_event(
        "Act",
        f"Attempting replacement for {order_id}"
    )

    order = orders.get(order_id)

    if not order:

        log_event(
            "Act",
            f"Order {order_id} not found",
            "error"
        )

        return {
            "success": False,
            "error": "Order not found"
        }

    product_id = order["product_id"]

    product = inventory.get(product_id)

    if not product:

        log_event(
            "Act",
            f"Product {product_id} not found",
            "error"
        )

        return {
            "success": False,
            "error": "Product not found"
        }

    if product["quantity"] <= 0:

        product["available"] = False

        log_event(
            "Act",
            "Replacement failed: product is out of stock",
            "warning"
        )

        log_event(
            "Adapt",
            "Replacement blocked. "
            "Agent must find an alternative resolution.",
            "warning"
        )

        return {
            "success": False,
            "error":
                "Replacement unavailable: product is out of stock"
        }

    product["quantity"] -= 1

    if product["quantity"] == 0:
        product["available"] = False

    replacement_id = (
        f"REP{len(replacements) + 1001}"
    )

    replacements[replacement_id] = {
        "replacement_id": replacement_id,
        "order_id": order_id,
        "product_id": product_id,
        "status": "confirmed"
    }

    order["resolution"] = "replacement"
    order["status"] = "replacement_initiated"

    log_event(
        "Act",
        f"Replacement created successfully: {replacement_id}",
        "success"
    )

    return {
        "success": True,
        "message": "Replacement successfully created",
        "replacement":
            replacements[replacement_id]
    }


# ============================================================
# REFUND
# ============================================================

@app.post("/refund/{order_id}")
def create_refund(order_id: str):

    log_event(
        "Act",
        f"Processing refund for {order_id}"
    )

    order = orders.get(order_id)

    if not order:

        log_event(
            "Act",
            f"Order {order_id} not found",
            "error"
        )

        return {
            "success": False,
            "error": "Order not found"
        }

    refund_id = (
        f"REF{len(refunds) + 1001}"
    )

    refunds[refund_id] = {
        "refund_id": refund_id,
        "order_id": order_id,
        "amount": order["order_value"],
        "status": "processed"
    }

    order["resolution"] = "refund"
    order["status"] = "refunded"

    log_event(
        "Adapt",
        "Replacement unavailable, switching to refund",
        "warning"
    )

    log_event(
        "Act",
        f"Refund successfully processed: {refund_id}",
        "success"
    )

    return {
        "success": True,
        "message": "Refund successfully processed",
        "refund": refunds[refund_id]
    }


# ============================================================
# VERIFY
# ============================================================

@app.get("/verify/{order_id}")
def verify_resolution(order_id: str):

    log_event(
        "Verify",
        f"Verifying final resolution for {order_id}"
    )

    order = orders.get(order_id)

    if not order:

        log_event(
            "Verify",
            "Verification failed: order not found",
            "error"
        )

        return {
            "success": False,
            "error": "Order not found"
        }

    resolution = order["resolution"]

    if resolution == "refund":

        for refund in refunds.values():

            if refund["order_id"] == order_id:

                log_event(
                    "Verify",
                    f"Refund {refund['refund_id']} "
                    "verified successfully",
                    "success"
                )

                return {
                    "success": True,
                    "verified": True,
                    "resolution": "refund",
                    "status": refund["status"],
                    "refund_id": refund["refund_id"],
                    "amount": refund["amount"]
                }

    if resolution == "replacement":

        for replacement in replacements.values():

            if replacement["order_id"] == order_id:

                log_event(
                    "Verify",
                    f"Replacement "
                    f"{replacement['replacement_id']} "
                    "verified successfully",
                    "success"
                )

                return {
                    "success": True,
                    "verified": True,
                    "resolution": "replacement",
                    "status": replacement["status"],
                    "replacement_id":
                        replacement["replacement_id"]
                }

    log_event(
        "Verify",
        "No completed resolution found",
        "error"
    )

    return {
        "success": True,
        "verified": False,
        "resolution": None,
        "message":
            "No completed resolution found"
    }


# ============================================================
# RESOLVE ENDPOINT
# ============================================================

@app.post("/resolve")
def resolve_customer(request: ResolveRequest):

    global workflow_events

    # Clear events from previous request
    workflow_events = []

    # OBSERVE
    log_event(
        "Observe",
        f"Customer request received: {request.message}",
        "success"
    )

    try:

        # Import only when required
        from agent import run_agent

        result = run_agent(request.message)

        # Final verification event is added here as a
        # workflow-level completion marker.
        log_event(
            "Verify",
            "Resolution workflow completed",
            "success"
        )

        return {
            "success": True,
            "response": result,
            "events": workflow_events
        }

    except Exception as e:

        log_event(
            "Verify",
            f"Agent error: {str(e)}",
            "error"
        )

        return {
            "success": False,
            "response":
                "ResolveAI encountered an error.",
            "error": str(e),
            "events": workflow_events
        }