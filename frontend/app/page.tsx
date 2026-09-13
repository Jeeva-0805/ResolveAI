"use client";

import { useState } from "react";

type Message = {
  role: "user" | "agent";
  text: string;
};

type Stage = {
  name: string;
  icon: string;
  status: "pending" | "active" | "completed";
};

export default function Home() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const [stages, setStages] = useState<Stage[]>([
    { name: "Observe", icon: "👁", status: "pending" },
    { name: "Investigate", icon: "🔍", status: "pending" },
    { name: "Decide", icon: "🧠", status: "pending" },
    { name: "Act", icon: "⚡", status: "pending" },
    { name: "Verify", icon: "✓", status: "pending" },
    { name: "Adapt", icon: "↻", status: "pending" },
  ]);

  const [showDetails, setShowDetails] = useState(false);

  const updateStages = async () => {
    const names = [
      "Observe",
      "Investigate",
      "Decide",
      "Act",
      "Verify",
      "Adapt",
    ];

    for (let i = 0; i < names.length; i++) {
      setStages((prev) =>
        prev.map((stage, index) => ({
          ...stage,
          status:
            index < i
              ? "completed"
              : index === i
              ? "active"
              : "pending",
        }))
      );

      await new Promise((resolve) => setTimeout(resolve, 450));
    }

    setStages((prev) =>
      prev.map((stage) => ({
        ...stage,
        status: "completed",
      }))
    );
  };

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const userMessage = message.trim();

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);
    setShowDetails(true);

    setStages([
      { name: "Observe", icon: "👁", status: "active" },
      { name: "Investigate", icon: "🔍", status: "pending" },
      { name: "Decide", icon: "🧠", status: "pending" },
      { name: "Act", icon: "⚡", status: "pending" },
      { name: "Verify", icon: "✓", status: "pending" },
      { name: "Adapt", icon: "↻", status: "pending" },
    ]);

    try {
      const response = await fetch("http://127.0.0.1:8000/resolve", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
        }),
      });

      if (!response.ok) {
        throw new Error("Backend request failed");
      }

      const data = await response.json();

      await updateStages();

      setMessages((prev) => [
        ...prev,
        {
          role: "agent",
          text:
            data.response ||
            data.message ||
            "ResolveAI completed the request.",
        },
      ]);
    } catch (error) {
      setStages((prev) =>
        prev.map((stage) => ({
          ...stage,
          status: "pending",
        }))
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "agent",
          text:
            "❌ Unable to connect to ResolveAI backend.\n\nPlease make sure FastAPI is running on http://127.0.0.1:8000",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const useDemo = () => {
    setMessage(
      "My laptop arrived damaged. My order ID is ORD1001. I want a replacement."
    );
  };

  return (
    <main className="min-h-screen bg-[#030817] text-white">

      {/* =====================================================
          HEADER
      ====================================================== */}

      <header className="sticky top-0 z-50 border-b border-slate-800/80 bg-[#030817]/95 backdrop-blur">

        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-lg font-bold shadow-lg shadow-blue-600/20">
              R
            </div>

            <div>
              <h1 className="text-lg font-bold tracking-tight">
                ResolveAI
              </h1>

              <p className="text-xs text-slate-500">
                Autonomous Customer Resolution Agent
              </p>
            </div>

          </div>

          <div className="flex items-center gap-2 rounded-full border border-green-500/20 bg-green-500/5 px-4 py-2">

            <span className="h-2 w-2 animate-pulse rounded-full bg-green-400" />

            <span className="text-xs font-medium text-green-400">
              Agent Online
            </span>

          </div>

        </div>

      </header>


      {/* =====================================================
          MAIN
      ====================================================== */}

      <section className="mx-auto max-w-7xl px-6 py-8">

        {/* HERO */}

        {messages.length === 0 && (

          <div className="mx-auto max-w-4xl py-10 text-center">

            <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-3xl border border-blue-500/20 bg-blue-500/10 text-4xl shadow-2xl shadow-blue-500/10">
              🤖
            </div>

            <div className="mb-3 inline-flex rounded-full border border-blue-500/20 bg-blue-500/5 px-4 py-2 text-xs text-blue-300">
              AI-POWERED CUSTOMER RESOLUTION
            </div>

            <h2 className="mt-4 text-4xl font-bold tracking-tight md:text-6xl">
              Don't just answer.
              <br />

              <span className="text-blue-500">
                Resolve.
              </span>
            </h2>

            <p className="mx-auto mt-6 max-w-2xl text-base leading-7 text-slate-400">
              ResolveAI investigates customer issues, checks policies,
              makes decisions, executes real actions, verifies outcomes,
              and adapts when the first resolution fails.
            </p>

          </div>

        )}


        {/* =====================================================
            WORKFLOW
        ====================================================== */}

        <div className="mb-8 rounded-2xl border border-slate-800 bg-slate-900/40 p-5">

          <div className="mb-4 flex items-center justify-between">

            <div>
              <h3 className="font-semibold">
                Agent Workflow
              </h3>

              <p className="mt-1 text-xs text-slate-500">
                Observe → Investigate → Decide → Act → Verify → Adapt
              </p>
            </div>

            {loading && (
              <div className="flex items-center gap-2 text-xs text-blue-400">

                <span className="h-2 w-2 animate-pulse rounded-full bg-blue-400" />

                Agent working...

              </div>
            )}

          </div>


          <div className="grid grid-cols-2 gap-3 md:grid-cols-6">

            {stages.map((stage, index) => (

              <div
                key={stage.name}
                className={`relative rounded-xl border p-4 transition-all duration-500 ${
                  stage.status === "completed"
                    ? "border-green-500/40 bg-green-500/5"
                    : stage.status === "active"
                    ? "border-blue-500/50 bg-blue-500/10 shadow-lg shadow-blue-500/10"
                    : "border-slate-800 bg-slate-950/40"
                }`}
              >

                <div className="flex items-center justify-between">

                  <span className="text-xl">
                    {stage.icon}
                  </span>

                  {stage.status === "completed" && (
                    <span className="text-xs text-green-400">
                      ✓
                    </span>
                  )}

                  {stage.status === "active" && (
                    <span className="h-2 w-2 animate-pulse rounded-full bg-blue-400" />
                  )}

                </div>

                <p
                  className={`mt-3 text-sm font-semibold ${
                    stage.status === "completed"
                      ? "text-green-400"
                      : stage.status === "active"
                      ? "text-blue-400"
                      : "text-slate-500"
                  }`}
                >
                  {stage.name}
                </p>

                {index < stages.length - 1 && (
                  <div className="absolute -right-2 top-1/2 hidden text-slate-700 md:block">
                    →
                  </div>
                )}

              </div>

            ))}

          </div>

        </div>


        {/* =====================================================
            CONTENT GRID
        ====================================================== */}

        <div className="grid gap-6 lg:grid-cols-[1fr_360px]">

          {/* CHAT */}

          <div className="flex min-h-[500px] flex-col rounded-2xl border border-slate-800 bg-slate-900/40">

            <div className="border-b border-slate-800 px-5 py-4">

              <div className="flex items-center justify-between">

                <div>
                  <h3 className="font-semibold">
                    Customer Conversation
                  </h3>

                  <p className="mt-1 text-xs text-slate-500">
                    Describe the issue and let the agent resolve it.
                  </p>
                </div>

                <span className="rounded-lg border border-slate-700 px-3 py-1 text-xs text-slate-500">
                  LIVE
                </span>

              </div>

            </div>


            {/* CHAT MESSAGES */}

            <div className="flex-1 space-y-5 overflow-y-auto p-5">

              {messages.length === 0 && (

                <div className="flex min-h-[300px] items-center justify-center">

                  <div className="max-w-md text-center">

                    <p className="text-sm text-slate-500">
                      No customer request yet.
                    </p>

                    <button
                      onClick={useDemo}
                      className="mt-5 rounded-xl border border-blue-500/30 bg-blue-500/10 px-5 py-3 text-sm font-medium text-blue-400 transition hover:bg-blue-500/20"
                    >
                      Try Demo Request
                    </button>

                  </div>

                </div>

              )}


              {messages.map((msg, index) => (

                <div
                  key={index}
                  className={`flex ${
                    msg.role === "user"
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >

                  <div
                    className={`max-w-[85%] rounded-2xl px-5 py-4 ${
                      msg.role === "user"
                        ? "bg-blue-600 shadow-lg shadow-blue-600/10"
                        : "border border-slate-700 bg-slate-950"
                    }`}
                  >

                    <div
                      className={`mb-2 text-xs font-semibold ${
                        msg.role === "user"
                          ? "text-blue-100"
                          : "text-blue-400"
                      }`}
                    >
                      {msg.role === "user"
                        ? "YOU"
                        : "RESOLVEAI"}
                    </div>

                    <p className="whitespace-pre-wrap text-sm leading-7 text-slate-200">
                      {msg.text}
                    </p>

                  </div>

                </div>

              ))}


              {loading && (

                <div className="flex justify-start">

                  <div className="rounded-2xl border border-blue-500/20 bg-slate-950 px-5 py-4">

                    <div className="flex items-center gap-3">

                      <div className="flex gap-1">

                        <span className="h-2 w-2 animate-bounce rounded-full bg-blue-400" />

                        <span className="h-2 w-2 animate-bounce rounded-full bg-blue-400 [animation-delay:150ms]" />

                        <span className="h-2 w-2 animate-bounce rounded-full bg-blue-400 [animation-delay:300ms]" />

                      </div>

                      <span className="text-sm text-slate-400">
                        ResolveAI is investigating...
                      </span>

                    </div>

                  </div>

                </div>

              )}

            </div>


            {/* INPUT */}

            <div className="border-t border-slate-800 p-4">

              <div className="flex gap-3 rounded-xl border border-slate-700 bg-slate-950 p-2 focus-within:border-blue-500/50">

                <input
                  type="text"
                  value={message}
                  disabled={loading}
                  onChange={(e) =>
                    setMessage(e.target.value)
                  }
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      sendMessage();
                    }
                  }}
                  placeholder="Describe your customer issue..."
                  className="flex-1 bg-transparent px-3 py-3 text-sm text-white outline-none placeholder:text-slate-600"
                />

                <button
                  onClick={sendMessage}
                  disabled={
                    loading ||
                    !message.trim()
                  }
                  className="rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  {loading ? "..." : "Send"}
                </button>

              </div>

            </div>

          </div>


          {/* =====================================================
              AGENT INSIGHTS
          ====================================================== */}

          <aside className="space-y-5">

            {/* AGENT STATUS */}

            <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5">

              <div className="flex items-center gap-3">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/10 text-xl">
                  🧠
                </div>

                <div>
                  <h3 className="font-semibold">
                    ResolveAI Agent
                  </h3>

                  <p className="text-xs text-green-400">
                    Autonomous reasoning enabled
                  </p>
                </div>

              </div>

              <div className="mt-5 space-y-3">

                {[
                  ["Policy aware", "✓"],
                  ["Tool enabled", "✓"],
                  ["Action capable", "✓"],
                  ["Verification enabled", "✓"],
                  ["Adaptation enabled", "✓"],
                ].map(([label, value]) => (

                  <div
                    key={label}
                    className="flex items-center justify-between border-b border-slate-800 pb-3 text-sm"
                  >

                    <span className="text-slate-400">
                      {label}
                    </span>

                    <span className="text-green-400">
                      {value}
                    </span>

                  </div>

                ))}

              </div>

            </div>


            {/* INVESTIGATION */}

            {showDetails && (

              <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5">

                <div className="flex items-center justify-between">

                  <h3 className="font-semibold">
                    Investigation
                  </h3>

                  <span className="text-xs text-blue-400">
                    TOOL CALLS
                  </span>

                </div>

                <div className="mt-5 space-y-3">

                  {[
                    ["Customer", "Retrieved", "✓"],
                    ["Order", "ORD1001", "✓"],
                    ["Policy", "Checked", "✓"],
                    ["Inventory", "0 units", "⚠"],
                  ].map(([label, value, status]) => (

                    <div
                      key={label}
                      className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950/60 p-3"
                    >

                      <div>
                        <p className="text-xs text-slate-500">
                          {label}
                        </p>

                        <p className="mt-1 text-sm text-slate-200">
                          {value}
                        </p>
                      </div>

                      <span
                        className={
                          status === "⚠"
                            ? "text-yellow-400"
                            : "text-green-400"
                        }
                      >
                        {status}
                      </span>

                    </div>

                  ))}

                </div>

              </div>

            )}


            {/* DEMO SCENARIO */}

            <div className="rounded-2xl border border-blue-500/20 bg-blue-500/5 p-5">

              <p className="text-xs font-semibold uppercase tracking-wider text-blue-400">
                Recommended Demo
              </p>

              <p className="mt-3 text-sm leading-6 text-slate-300">
                Damaged laptop → replacement requested →
                inventory unavailable → agent adapts →
                refund → verification.
              </p>

              <button
                onClick={useDemo}
                className="mt-4 w-full rounded-lg border border-blue-500/30 bg-blue-500/10 px-4 py-2.5 text-sm font-medium text-blue-400 transition hover:bg-blue-500/20"
              >
                Load Demo Scenario
              </button>

            </div>

          </aside>

        </div>

      </section>


      {/* FOOTER */}

      <footer className="border-t border-slate-800/80 py-6">

        <p className="text-center text-xs text-slate-600">
          ResolveAI • Autonomous Customer Resolution •
          Observe. Investigate. Decide. Act. Verify. Adapt.
        </p>

      </footer>

    </main>
  );
}