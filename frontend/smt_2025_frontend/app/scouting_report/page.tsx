"use client"
import { useEffect, useState } from 'react';
import Link from 'next/link'

export default function Page() {
  type Pitcher = {
          pitcher: string;
          pitcher_hand: string;
      };
  
      type PitcherData = {
        pickoffs: number;
        pick_per: number;
        pitches: number;
        pitch_per: number;
        games: number;
        games_per: number;
        ppg: number;
        ppg_per: number;
      }
  
      interface ModelInput {
      outs: number;
      runs: number;
      pitcher_hand: string;
      batter_hand: string;
      base_dist: number;
      steal_score: number;
      home_team: string;
    } 
  
      const [modelOutput, setModelOutput] = useState<string | null>(null);
      const [loading, setLoading] = useState(false);
      const [selectedTeam, setSelectedTeam] = useState<string | null>(null);
      const [pitchers, setPitchers] = useState<Pitcher[]>([]);
      const [selectedPitcher, setSelectedPitcher] = useState<Pitcher | null>(null);
      const [pitcherData, setPitcherData] = useState<PitcherData | null>(null);
      const [formData, setFormData] = useState<ModelInput>({ outs: 0, runs: 0, pitcher_hand: '', batter_hand: '', base_dist: 0, steal_score: 0, home_team: ''});
      const teams = ['QEA', 'RZQ', 'YJD'];
  
      const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
          const { name, value } = event.target;
          setFormData({
              ...formData,
              [name]: value
          });
      };
  
      const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
          event.preventDefault(); 
  
          if (!formData.outs || !formData.runs || !formData.pitcher_hand || !formData.batter_hand || !formData.base_dist || !formData.steal_score || !formData.home_team) {
              alert('All fields are required!');
              return;
          }

          const trimmedFormData = {
            outs: Number(formData.outs),
            runs: Number(formData.runs),
            pitcher_hand: Number(formData.pitcher_hand),
            batter_hand: Number(formData.batter_hand),
            base_dist: Number(formData.base_dist),
            steal_score: Number(formData.steal_score),
            home_team: Number(formData.home_team),
          };

          console.log(trimmedFormData.outs, trimmedFormData.runs, trimmedFormData.pitcher_hand, trimmedFormData.batter_hand, trimmedFormData.base_dist, trimmedFormData.steal_score, trimmedFormData.home_team)

  
          try {
            setLoading(true);
            const res = await fetch(`https://smt-2025.onrender.com/api/run_model?outs=${trimmedFormData.outs}
              &runs=${trimmedFormData.runs}
              &pitcher_hand=${trimmedFormData.pitcher_hand}
              &batter_hand=${trimmedFormData.batter_hand}
              &base_dist=${trimmedFormData.base_dist}
              &steal_score=${trimmedFormData.steal_score}
              &home_team=${trimmedFormData.home_team}`);
            const data = await res.json();
            setModelOutput(data.prediction);

            setFormData({
              outs: 0,
              runs: 0,
              pitcher_hand: '',
              batter_hand: '',
              base_dist: 0,
              steal_score: 0,
              home_team: '',
            });
          } catch (error) {
            alert(error instanceof Error ? error.message : 'Failed to run model');
          } finally {
            setLoading(false);
          }
        };
  
    useEffect(() => {
      if (!selectedTeam) return;
  
      const fetchPitchers = async () => {
        try {
          const res = await fetch(`/api/scouting/pitcher_names?team=${encodeURIComponent(selectedTeam)}`);
          const data = await res.json();
          
          setPitchers(data.pitchers || []);
          setSelectedPitcher(null);
  
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
  
    useEffect(() => {
      if (!selectedPitcher) return;
  
      const fetchPitcherData = async () => {
        try {
          const res = await fetch(
            `https://smt-2025.onrender.com/api/pitcher_data?pitcher=${encodeURIComponent(selectedPitcher.pitcher)}`
          );
          const data = await res.json();
  
          setPitcherData({
            pickoffs: data.pickoffs[0],
            pick_per: data.pickoffs[1],
            pitches: data.pitches[0],
            pitch_per: data.pitches[1],
            games: data.games[0],
            games_per: data.games[1],
            ppg: data.ppg[0],
            ppg_per: data.ppg[1],
          });
        } catch (err) {
          console.error("Failed to fetch pitcher data:", err);
        }
      };
  
      fetchPitcherData();
    }, [selectedPitcher]);
  
    return (
      <main className="flex flex-col px-6 py-10 max-w-6xl mx-auto gap-8">
        <Link href="/"
            className="text-green-900 bg-blue-100 border border-green-400 absolute left-10 top-10 py-4 px-8 rounded-md no-underline text-foreground bg-btn-background hover:bg-btn-background-hover flex items-center group text-md text-blue-400">
                Back to dashboard
        </Link>
        <h1 className="text-3xl font-bold text-center text-blue-800">
          Pitcher Scouting Report
        </h1>
        <div className="flex flex-col md:flex-row gap-6">
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium text-gray-700">Select Team</label>
            <select
              value={selectedTeam ?? ''}
              onChange={(e) => setSelectedTeam(e.target.value)}
              className="border border-gray-300 rounded-md shadow-sm p-2">
              <option value="" disabled>Select a team</option>
              {teams.map((team) => (
                <option key={team} value={team}>{team}</option>))}
            </select>
          </div>
  
          {selectedTeam && (
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium text-gray-700">Select Pitcher</label>
              <select
                  value={selectedPitcher?.pitcher ?? ''}
                  onChange={(e) => {
                      const selected = pitchers.find(p => p.pitcher === e.target.value);
                      setSelectedPitcher(selected ?? null);
                  }}
                  className="border border-gray-300 rounded-md shadow-sm p-2"
                  >
                  <option value="" disabled>Select a pitcher</option>
                  {pitchers.map((pitcher) => (
                      <option key={pitcher.pitcher} value={pitcher.pitcher}>
                      {pitcher.pitcher}
                      </option>))}
                  </select>
            </div>)}
        </div>
        <div className="flex flex-col lg:flex-row gap-8">
          <div className="flex-1 flex flex-col items-center gap-4">
            <img
              src="https://img.mlbstatic.com/mlb-photos/image/upload/w_213,d_people:generic:headshot:silo:current.png,q_auto:best,f_auto/v1/people/%7BmlbId%7D/headshot/67/current"
              alt="Pitcher"
              className="w-40 h-40 rounded-xl shadow-md object-cover"
            />
            {selectedPitcher && (
              <section className="bg-white border-l-4 border-blue-400 shadow-md p-4 rounded-lg w-full max-w-sm">
                <p className="text-xl font-semibold text-gray-800">
                  Name: {selectedPitcher.pitcher}
                </p>
                <p className="text-xl font-semibold text-gray-800">
                  Throws: {selectedPitcher.pitcher_hand}
                </p>
                {selectedTeam && (
                  <p className="text-xl font-semibold text-gray-800">
                    Team: {selectedTeam}
                  </p>
                )}
              </section>
            )}
          </div>
  
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 auto-rows-fr">
          <section className="flex flex-col justify-between h-full bg-white border-l-4 border-blue-600 shadow-md p-4 rounded-lg">
              <p className="text-gray-700 text-md font-bold">Pickoff Counts</p>
              {pitcherData && (
              <p className="text-sm text-gray-600 mt-2">
                {pitcherData.pickoffs} pickoffs — {pitcherData.pick_per.toFixed(1)} percentile
              </p>)}
              {selectedPitcher && (
              <img
                  src={`https://smt-2025.onrender.com/api/pickoff_hist?pitcher=${encodeURIComponent(selectedPitcher.pitcher)}`}
                  alt="Pickoff Histogram"
                  className="block w-full h-auto max-h-64 object-contain rounded shadow-md"/>)}
          </section>
  
          <section className="flex flex-col justify-between h-full bg-white border-l-4 border-blue-600 shadow-md p-4 rounded-lg">
              <p className="text-gray-700 text-md font-bold">Pitch Counts</p>
              {pitcherData && (
              <p className="text-sm text-gray-600 mt-2">
                {pitcherData.pitches} pitches — {pitcherData.pitch_per.toFixed(1)} percentile
              </p>)}
              {selectedPitcher && (
              <img
                  src={`https://smt-2025.onrender.com/api/pitch_hist?pitcher=${encodeURIComponent(selectedPitcher.pitcher)}`}
                  alt="Pitch Count Histogram"
                  className="block w-full h-auto max-h-64 object-contain rounded shadow-md"/>)}
          </section>
  
          <section className="flex flex-col justify-between h-full bg-white border-l-4 border-blue-600 shadow-md p-4 rounded-lg">
              <p className="text-gray-700 text-md font-bold">Games Played</p>
              {pitcherData && (
              <p className="text-sm text-gray-600 mt-2">
                {pitcherData.games} games played — {pitcherData.games_per.toFixed(1)} percentile
              </p>)}
              {selectedPitcher && (
              <img
                  src={`https://smt-2025.onrender.com/api/games_hist?pitcher=${encodeURIComponent(selectedPitcher.pitcher)}`}
                  alt="Games Played Histogram"
                  className="block w-full h-auto max-h-64 object-contain rounded shadow-md"/>)}
          </section>
  
          <section className="flex flex-col justify-between h-full bg-white border-l-4 border-blue-600 shadow-md p-4 rounded-lg">
              <p className="text-gray-700 text-md font-bold">Pickoffs Per Game</p>
              {pitcherData && (
              <p className="text-sm text-gray-600 mt-2">
                {pitcherData.ppg} pickoffs per game — {pitcherData.ppg_per.toFixed(1)} percentile
              </p>)}
              {selectedPitcher && (
              <img
                  src={`https://smt-2025.onrender.com/api/ppg_hist?pitcher=${encodeURIComponent(selectedPitcher.pitcher)}`}
                  alt="PPG Histogram"
                  className="block w-full h-auto max-h-64 object-contain rounded shadow-md"/>)}
          </section>
          </div>
          </div>
  
        <div className="flex flex-col gap-4 mt-6">
      <h2 className="text-2xl font-semibold text-blue-700">Run Model Simulation</h2>
      <form
        onSubmit={handleSubmit}
        className="animate-in grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 bg-white shadow-lg rounded-lg p-4 w-full max-w-5xl">
        <div>
          <label htmlFor="outs" className="text-sm text-blue-900 font-medium block mb-1">Number of Outs:</label>
          <select
            id="outs"
            name="outs"
            value={formData.outs}
            onChange={handleChange}
            required
            className="text-blue-900 rounded-md px-3 py-1 w-full bg-gray-50 border border-gray-300 focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50">
            <option value="">Select Outs</option>
            <option value={0}>0</option>
            <option value={1}>1</option>
            <option value={2}>2</option>
          </select>
        </div>
  
        <div>
          <label htmlFor="runs" className="text-sm text-blue-900 font-medium block mb-1">Run Differential:</label>
          <input
            type="number"
            id="runs"
            name="runs"
            value={formData.runs}
            onChange={handleChange}
            className="text-blue-900 rounded-md px-3 py-1 w-full bg-gray-50 border border-gray-300 focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50"/>
        </div>
  
        <div>
          <label htmlFor="pitcher_hand" className="text-sm text-blue-900 font-medium block mb-1">Pitcher Handedness:</label>
          <select
            id="pitcher_hand"
            name="pitcher_hand"
            value={formData.pitcher_hand}
            onChange={handleChange}
            required
            className="text-blue-900 rounded-md px-3 py-1 w-full bg-gray-50 border border-gray-300 focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50">
            <option value="">Select Handedness</option>
            <option value={0}>Right</option>
            <option value={1}>Left</option>
          </select>
        </div>
  
        <div>
          <label htmlFor="batter_hand" className="text-sm text-blue-900 font-medium block mb-1">Batter Handedness:</label>
          <select
            id="batter_hand"
            name="batter_hand"
            value={formData.batter_hand}
            onChange={handleChange}
            required
            className="text-blue-900 rounded-md px-3 py-1 w-full bg-gray-50 border border-gray-300 focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50">
            <option value="">Select Handedness</option>
            <option value={0}>Right</option>
            <option value={1}>Left</option>
          </select>
        </div>
  
        <div>
          <label htmlFor="base_dist" className="text-sm text-blue-900 font-medium block mb-1">Leadoff Distance (in feet):</label>
          <input
            type="number"
            id="base_dist"
            name="base_dist"
            value={formData.base_dist}
            onChange={handleChange}
            className="text-blue-900 rounded-md px-3 py-1 w-full bg-gray-50 border border-gray-300 focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50"/>
        </div>
  
        <div>
          <label htmlFor="steal_score" className="text-sm text-blue-900 font-medium block mb-1">Steal+ (average is 100):</label>
          <input
            type="number"
            id="steal_score"
            name="steal_score"
            value={formData.steal_score}
            onChange={handleChange}
            className="text-blue-900 rounded-md px-3 py-1 w-full bg-gray-50 border border-gray-300 focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50"/>
        </div>
  
        <div>
          <label htmlFor="home_team" className="text-sm text-blue-900 font-medium block mb-1">Home or Away:</label>
          <select
            id="home_team"
            name="home_team"
            value={formData.home_team}
            onChange={handleChange}
            required
            className="text-blue-900 rounded-md px-3 py-1 w-full bg-gray-50 border border-gray-300 focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50">
            <option value="">Select Home or Away</option>
            <option value={1}>Home</option>
            <option value={0}>Away</option>
          </select>
        </div>
  
        <div className="col-span-full mt-2">
          <button
            type="submit"
            className="w-full bg-blue-700 hover:bg-blue-800 text-white font-medium py-2 px-4 rounded-md transition">
            Run Model
          </button>
        </div>
      </form>
  
          <div className="bg-blue-100 border border-blue-400 p-4 rounded-lg shadow-inner w-full max-w-xl text-center">
            {loading ? (
              <p className="text-blue-800 font-medium">Running model...</p>) 
              : modelOutput ? (<p className="text-blue-800 font-semibold">Pickoff Probability: {modelOutput}</p>) 
              : (
              <p className="text-blue-800">Run the model to simulate the probability of a pickoff in a given scenario.</p>)}
          </div>
        </div>
      </main>
    );
}
