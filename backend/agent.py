import os
import json
import urllib.request
import urllib.error

from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Check backend/.env"
    )

client = genai.Client(api_key=API_KEY)

BACKEND_URL = "http://127.0.0.1:8000"


# ============================================================
# HTTP HELPER
# ============================================================

def call_backend(method, endpoint):
    """
    Call one of our FastAPI backend endpoints.
    """

    url = BACKEND_URL + endpoint

    try:

        request = urllib.request.Request(
            url=url,
            method=method
        )

        with urllib.request.urlopen(request, timeout=10) as response:

            data = response.read().decode("utf-8")

            return json.loads(data)

    except urllib.error.HTTPError as e:

        try:
            error_body = e.read().decode("utf-8")
            return json.loads(error_body)

        except Exception:
            return {
                "success": False,
                "error": f"Backend HTTP error {e.code}"
            }

    except Exception as e:

        return {
            "success": False,
            "error": f"Backend connection error: {str(e)}"
        }


# ============================================================
# INFORMATION TOOLS
# ============================================================

def get_customer(customer_id: str):
    """
    Retrieve customer information.
    """

    return call_backend(
        "GET",
        f"/customer/{customer_id}"
    )


def get_order(order_id: str):
    """
    Retrieve order information.
    """

    return call_backend(
        "GET",
        f"/order/{order_id}"
    )


def get_inventory(product_id: str):
    """
    Check current inventory availability.
    """

    return call_backend(
        "GET",
        f"/inventory/{product_id}"
    )


def get_policy(issue_type: str):
    """
    Retrieve the company policy for a customer issue.
    """

    return call_backend(
        "GET",
        f"/policy/{issue_type}"
    )


# ============================================================
# ACTION TOOLS
# ============================================================

def create_replacement(order_id: str):
    """
    Attempt to create a replacement for an order.

    IMPORTANT:
    This performs a real state-changing action
    in the ResolveAI backend.
    """

    return call_backend(
        "POST",
        f"/replacement/{order_id}"
    )


def create_refund(order_id: str):
    """
    Process a refund for an order.

    IMPORTANT:
    This performs a real state-changing action
    in the ResolveAI backend.
    """

    return call_backend(
        "POST",
        f"/refund/{order_id}"
    )


# ============================================================
# VERIFICATION TOOL
# ============================================================

def verify_resolution(order_id: str):
    """
    Verify whether the requested resolution was actually completed.
    """

    return call_backend(
        "GET",
        f"/verify/{order_id}"
    )


# ============================================================
# RESOLVEAI AGENT
# ============================================================

def run_agent(customer_request: str):

    system_instruction = """
You are ResolveAI, an autonomous customer resolution agent.

Your job is to resolve customer issues by observing the request,
investigating the situation, making a policy-compliant decision,
executing an action, verifying the result, and adapting when
an action fails.

============================================================
AGENTIC WORKFLOW
============================================================

You MUST follow this general workflow:

1. OBSERVE
   Understand the customer's request.

2. INVESTIGATE
   Retrieve the information needed to make a safe decision.

3. DECIDE
   Select the best valid resolution based on:
   - customer information
   - order information
   - company policy
   - inventory availability

4. ACT
   Actually execute the selected resolution using an action tool.

5. VERIFY
   Verify that the action was successfully completed.

6. ADAPT
   If the action fails or cannot be completed:
   - understand WHY it failed
   - reconsider the available options
   - select another valid resolution
   - execute the alternative
   - verify again

============================================================
AVAILABLE INFORMATION TOOLS
============================================================

get_customer(customer_id)

get_order(order_id)

get_inventory(product_id)

get_policy(issue_type)

============================================================
AVAILABLE ACTION TOOLS
============================================================

create_replacement(order_id)

create_refund(order_id)

============================================================
VERIFICATION
============================================================

verify_resolution(order_id)

============================================================
IMPORTANT RULES
============================================================

RULE 1:
Never claim that an action was completed unless the action tool
actually reports success.

RULE 2:
Always check company policy before executing a resolution.

RULE 3:
If replacement is requested, check inventory before attempting
replacement.

RULE 4:
If an action fails, do NOT stop immediately.
Analyze the failure and attempt a valid alternative if policy
allows it.

RULE 5:
Always verify the final resolution.

RULE 6:
Never invent customer, order, inventory, policy, or action results.

RULE 7:
The customer's requested resolution is a preference, not an
absolute instruction. Safety and company policy take priority.

============================================================
FAILURE AND ADAPTATION EXAMPLE
============================================================

If the customer requests a replacement:

- Check order.
- Check policy.
- Check inventory.
- If replacement is allowed and stock exists:
    execute replacement.
- If replacement fails because stock is unavailable:
    check whether refund is allowed.
- If refund is allowed:
    execute refund.
- Verify the refund.
- Report the final outcome honestly.

============================================================
FINAL RESPONSE
============================================================

After completing the workflow, provide:

OBSERVATION
What the customer requested.

INVESTIGATION
What information was retrieved.

DECISION
Why the selected resolution was appropriate.

ACTION
What action was actually executed.

VERIFICATION
Whether the action succeeded.

ADAPTATION
If something failed, explain what changed and why.

FINAL OUTCOME
Clearly state how the customer was resolved.

Do not claim success unless verification confirms it.
"""


    # ========================================================
    # CREATE CHAT
    # ========================================================

    chat = client.chats.create(
        model="gemini-3.5-flash-lite",

        config={
            "system_instruction": system_instruction,

            "tools": [
                get_customer,
                get_order,
                get_inventory,
                get_policy,
                create_replacement,
                create_refund,
                verify_resolution
            ]
        }
    )


    # ========================================================
    # SEND CUSTOMER REQUEST
    # ========================================================

    response = chat.send_message(
        customer_request
    )

    return response.text


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    request = """
My laptop arrived damaged.
My order ID is ORD1001.
I want a replacement.
"""

    print()
    print("================================================")
    print("              RESOLVEAI AGENT")
    print("================================================")

    print()
    print("CUSTOMER REQUEST")
    print("------------------------------------------------")
    print(request)

    print()
    print("AGENT WORKFLOW")
    print("------------------------------------------------")
    print("Observe → Investigate → Decide → Act → Verify")
    print("                         ↓")
    print("                      Adapt")
    print()

    print("Agent is working...")
    print()

    try:

        result = run_agent(request)

        print("================================================")
        print("              FINAL OUTCOME")
        print("================================================")
        print()

        print(result)

        print()
        print("================================================")
        print("              WORKFLOW COMPLETE")
        print("================================================")

    except Exception as e:

        print()
        print("================================================")
        print("              AGENT ERROR")
        print("================================================")
        print()

        print(str(e))