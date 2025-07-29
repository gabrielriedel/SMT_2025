"use client";

import { useEffect, useState } from 'react';

export default function PitcherScoutingReport() {
  const [modelOutput, setModelOutput] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedTeam, setSelectedTeam] = useState<string | null>(null);
  const [pitchers, setPitchers] = useState<string[]>([]);
  const [selectedPitcher, setSelectedPitcher] = useState('');
  const teams = ['QEA', 'RZQ', 'YJD'];

  const handleRunModel = () => {
    setLoading(true);
    fetch("https://smt-2025.onrender.com/api/run_pitcher_model")
      .then((res) => res.json())
      .then((data) => setModelOutput(data.result))
      .catch((err) => {
        console.error("Model run failed:", err);
        alert("Failed to run model. Please try again.");
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (!selectedTeam) return;

    const fetchPitchers = async () => {
      try {
        const res = await fetch(`/api/scouting/pitcher_names?team=${encodeURIComponent(selectedTeam)}`);
        const data = await res.json();
        setPitchers(data.pitcher_names || []);
        setSelectedPitcher('');
        console.log("Team selected:", selectedTeam);
      } catch (err) {
        console.error("Error fetching pitchers:", err);
      }
    };

    fetchPitchers();
  }, [selectedTeam]);

  useEffect(() => {
    if (selectedTeam && selectedPitcher) {
      console.log("Selected pitcher:", selectedPitcher, "from team:", selectedTeam);
    }
  }, [selectedPitcher]);

  return (
    <main className="flex flex-col px-6 py-10 max-w-6xl mx-auto gap-8">
      <h1 className="text-3xl font-bold text-center text-blue-800">
        Pitcher Scouting Report
      </h1>

      {/* Dropdowns */}
      <div className="flex flex-col md:flex-row gap-6">
        <div className="flex flex-col gap-2">
          <label className="text-sm font-medium text-gray-700">Select Team</label>
          <select
            value={selectedTeam ?? ''}
            onChange={(e) => setSelectedTeam(e.target.value)}
            className="border border-gray-300 rounded-md shadow-sm p-2"
          >
            <option value="" disabled>Select a team</option>
            {teams.map((team) => (
              <option key={team} value={team}>{team}</option>
            ))}
          </select>
        </div>

        {selectedTeam && (
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium text-gray-700">Select Pitcher</label>
            <select
              value={selectedPitcher}
              onChange={(e) => setSelectedPitcher(e.target.value)}
              className="border border-gray-300 rounded-md shadow-sm p-2"
            >
              <option value="" disabled>Select a pitcher</option>
              {pitchers.map((pitcher) => (
                <option key={pitcher} value={pitcher}>{pitcher}</option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Top Section */}
      <div className="flex flex-col lg:flex-row gap-8">
        <div className="flex-1 flex gap-6 items-start">
          <img
            src="https://via.placeholder.com/150"
            alt="Pitcher"
            className="w-40 h-40 rounded-xl shadow-md object-cover"
          />
          <div className="flex flex-col gap-2">
            <p className="text-xl font-semibold text-gray-800">Name: John Doe</p>
            <p className="text-md text-gray-600">Throws: Right</p>
            <p className="text-md text-gray-600">Velocity: 94-96 MPH</p>
            <p className="text-md text-gray-600">Team: SMT Hawks</p>
          </div>
        </div>

        <div className="flex-1 flex flex-col gap-4">
          <section className="bg-white border-l-4 border-blue-600 shadow-md p-6 rounded-lg w-full">
            <p className="text-gray-700 text-lg font-bold">Pitch Mix</p>
            <p className="text-gray-600 text-sm">Fastball: 55% | Slider: 25% | Changeup: 20%</p>
          </section>
          <section className="bg-white border-l-4 border-blue-600 shadow-md p-6 rounded-lg w-full">
            <p className="text-gray-700 text-lg font-bold">Scouting Notes</p>
            <p className="text-gray-600 text-sm">
              Strong command to both sides of the plate. Swing-and-miss slider. Some effort in delivery but repeats it well.
            </p>
          </section>
        </div>
      </div>

      {/* Model Section */}
      <div className="flex flex-col gap-4 mt-6">
        <h2 className="text-2xl font-semibold text-blue-700">Run Model Simulation</h2>

        <button
          onClick={handleRunModel}
          className="py-2 px-6 bg-blue-600 text-white font-semibold text-lg rounded-full shadow-md hover:bg-blue-700 transition duration-200"
        >
          Run Model
        </button>

        <div className="bg-blue-100 border border-blue-400 p-4 rounded-lg shadow-inner w-full max-w-xl text-center">
          {loading ? (
            <p className="text-blue-800 font-medium">Running model...</p>
          ) : modelOutput ? (
            <p className="text-blue-800 font-semibold">Model Output: {modelOutput}</p>
          ) : (
            <p className="text-blue-800">Click the button to simulate an outcome based on pitcher profile.</p>
          )}
        </div>
      </div>
    </main>
  );
}


