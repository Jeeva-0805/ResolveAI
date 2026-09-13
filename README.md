# 🤖 ResolveAI

## Autonomous Customer Resolution Agent

ResolveAI is an AI-powered customer resolution agent designed to handle customer complaints from investigation to final verified resolution.

Unlike a traditional chatbot that only recommends an action, ResolveAI can investigate the issue, make a policy-aware decision, execute a backend action, verify the result, and adapt when the original action fails.

---

## 🚀 Key Idea

ResolveAI follows a closed-loop agentic workflow:

Customer Request
        ↓
     Observe
        ↓
    Investigate
        ↓
      Decide
        ↓
       Act
        ↓
     Verify
        ↓
      Adapt
        ↓
 Final Resolution

The system is designed to make customer support more autonomous and reliable.

---

## ✨ Features

- Customer information retrieval
- Order information retrieval
- Company policy checking
- Inventory availability checking
- Automated replacement processing
- Automated refund processing
- Resolution verification
- Failure detection
- Adaptive fallback resolution
- Gemini-powered tool calling
- FastAPI backend
- Next.js frontend

---

## 🧠 Agentic Workflow

### 1. Observe

The agent understands the customer's request and identifies the required information.

### 2. Investigate

The agent retrieves:

- Customer information
- Order information
- Company policy
- Inventory information

### 3. Decide

The agent selects the most appropriate resolution based on:

- Customer request
- Order details
- Company policy
- Inventory availability

### 4. Act

The agent executes the selected backend action.

Available actions:

- Replacement
- Refund

### 5. Verify

The agent verifies whether the action was actually completed successfully.

The agent never claims success without backend verification.

### 6. Adapt

If the selected action fails, the agent analyzes the failure and attempts a valid alternative when company policy allows it.

---

# 🏗️ System Architecture

```text
                 Customer
                    │
                    ▼
          ┌──────────────────┐
          │   Next.js UI     │
          │    Frontend      │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │     FastAPI      │
          │     Backend      │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │   Gemini Agent   │
          │  Tool Calling    │
          └────────┬─────────┘
                   │
       ┌───────────┼───────────┐
       │           │           │
       ▼           ▼           ▼
   Customer      Order      Policy
      Tool        Tool        Tool
                   │
                   ▼
              Inventory
                 Tool
                   │
                   ▼
          ┌──────────────────┐
          │  Action Tools    │
          │                  │
          │ Replacement      │
          │ Refund           │
          └────────┬─────────┘
                   │
                   ▼
              Verification
                   │
                   ▼
             Final Outcome

# 🎥 Demo Video
[▶️ Watch the ResolveAI Demo Video](https://drive.google.com/file/d/1Orp27NBfcKMzf64iH3fj_QRhdp3tlS53/view?usp=sharing)

# 🔗 GitHub Repository

https://github.com/Jeeva-0805/ResolveAI