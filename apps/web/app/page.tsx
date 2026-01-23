"use client";

import { useState } from "react";
import { Activity, Moon, Dumbbell, Brain, Send, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function Dashboard() {
    const [sleep, setSleep] = useState<number>(7);
    const [hr, setHr] = useState<number>(60);
    const [plan, setPlan] = useState<string>("Heavy Leg Day");
    const [recommendation, setRecommendation] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const getRecommendation = async () => {
        setLoading(true);
        setRecommendation(null);
        try {
            const response = await fetch("http://127.0.0.1:8000/coach", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    sleep: Number(sleep),
                    hr: Number(hr),
                    plan
                }),
            });
            const data = await response.json();
            setRecommendation(data.recommendation);
        } catch (error) {
            console.error("Error fetching recommendation:", error);
            setRecommendation("Failed to connect to the Biometric Auditor API. Ensure the backend is running at http://localhost:8000");
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="min-h-screen p-8 flex flex-col items-center justify-center bg-[#050510] relative overflow-hidden">
            {/* Background blobs */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/20 blur-[120px] rounded-full" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-600/20 blur-[120px] rounded-full" />

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="w-full max-w-4xl z-10"
            >
                <header className="mb-12 text-center">
                    <h1 className="text-5xl font-extrabold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent mb-2">
                        Biometric Auditor
                    </h1>
                    <p className="text-gray-400 text-lg uppercase tracking-widest font-medium">Resolution Intelligence Coach</p>
                </header>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Input Section */}
                    <section className="glass-card p-8 flex flex-col gap-6">
                        <h2 className="text-xl font-semibold flex items-center gap-2 border-b border-white/10 pb-4 mb-2">
                            <Activity className="text-blue-400" /> Current Biometrics
                        </h2>

                        <div className="space-y-4">
                            <div className="flex flex-col gap-2">
                                <label className="text-sm text-gray-400 flex items-center gap-2">
                                    <Moon size={16} /> Sleep Duration (hours)
                                </label>
                                <input
                                    type="range" min="3" max="12" step="0.5"
                                    value={sleep} onChange={(e) => setSleep(parseFloat(e.target.value))}
                                    className="w-full accent-blue-500"
                                />
                                <div className="text-right font-mono text-blue-400">{sleep}h</div>
                            </div>

                            <div className="flex flex-col gap-2">
                                <label className="text-sm text-gray-400 flex items-center gap-2">
                                    <Activity size={16} /> Resting Heart Rate (BPM)
                                </label>
                                <input
                                    type="number"
                                    value={hr} onChange={(e) => setHr(parseInt(e.target.value))}
                                    className="bg-white/5 border border-white/10 rounded-lg p-3 outline-none focus:border-blue-500 transition-colors"
                                />
                            </div>

                            <div className="flex flex-col gap-2">
                                <label className="text-sm text-gray-400 flex items-center gap-2">
                                    <Dumbbell size={16} /> Original Workout Plan
                                </label>
                                <input
                                    type="text"
                                    value={plan} onChange={(e) => setPlan(e.target.value)}
                                    placeholder="e.g., Heavy Deadlifts"
                                    className="bg-white/5 border border-white/10 rounded-lg p-3 outline-none focus:border-blue-500 transition-colors"
                                />
                            </div>
                        </div>

                        <button
                            onClick={getRecommendation}
                            disabled={loading}
                            className="mt-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all transform hover:scale-[1.02] disabled:opacity-50"
                        >
                            {loading ? <Loader2 className="animate-spin" /> : <Send size={20} />}
                            {loading ? "Analyzing..." : "Audit My Resolution"}
                        </button>
                    </section>

                    {/* Output Section */}
                    <section className="glass-card p-8 flex flex-col relative overflow-hidden">
                        <h2 className="text-xl font-semibold flex items-center gap-2 border-b border-white/10 pb-4 mb-2">
                            <Brain className="text-purple-400" /> Coach's Deep Insight
                        </h2>

                        <div className="flex-1 flex items-center justify-center border border-white/5 rounded-xl bg-black/20 mt-4 p-6">
                            <AnimatePresence mode="wait">
                                {loading ? (
                                    <motion.div
                                        key="loading"
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        exit={{ opacity: 0 }}
                                        className="flex flex-col items-center gap-4 text-gray-500"
                                    >
                                        <div className="w-12 h-12 rounded-full border-t-2 border-blue-500 animate-spin" />
                                        <p>Scanning bio-signals...</p>
                                    </motion.div>
                                ) : recommendation ? (
                                    <motion.div
                                        key="output"
                                        initial={{ opacity: 0, scale: 0.95 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        className="text-gray-200 leading-relaxed overflow-y-auto max-h-[300px] text-justify"
                                    >
                                        {recommendation}
                                    </motion.div>
                                ) : (
                                    <motion.p
                                        key="idle"
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        className="text-gray-600 italic text-center"
                                    >
                                        Enter your biometrics and click the button for a personalized workout audit based on your fatigue levels.
                                    </motion.p>
                                )}
                            </AnimatePresence>
                        </div>

                        {recommendation && (
                            <div className="absolute top-0 right-0 p-4">
                                <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_10px_#22c55e]" />
                            </div>
                        )}
                    </section>
                </div>
            </motion.div>
        </main>
    );
}
