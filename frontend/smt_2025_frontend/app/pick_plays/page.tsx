"use client";
import { useState } from "react";
import Link from 'next/link'

export default function GifDisplay() {
  const [gifUrl, setGifUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = () => {
    setLoading(true);
    fetch("https://smt-2025.onrender.com/api/pick_animation").then((res) => {
        if (!res.ok) throw new Error("Failed to fetch gif");
        return res.blob();
      }).then((blob) => {
        const url = URL.createObjectURL(blob);
        setGifUrl(url);
      }).catch((err) => {
        console.error("Error loading gif:", err);
        alert("Failed to load animation. Please try again.");
      }).finally(() => {
        setLoading(false);
      });
  };

  return (
    <main className="flex flex-col px-6 py-10 max-w-6xl mx-auto gap-8">
      <Link href="/"
            className="text-green-900 bg-green-100 border border-green-400 absolute left-10 top-10 py-4 px-8 rounded-md no-underline text-foreground bg-btn-background hover:bg-btn-background-hover flex items-center group text-lg text-blue-400">
        Back to dashboard
      </Link>
      <h1 className="text-3xl font-bold text-center text-green-800">
        Random Pickoff Play Generator
      </h1>

      <div className="flex flex-col lg:flex-row gap-8">
        <div className="flex-1 flex flex-col gap-6">
          <section className="bg-white border-l-4 border-green-600 shadow-md p-6 rounded-lg w-full">
            <p className="text-gray-700 text-lg text-center font-bold">
              Explanation
            </p>
          </section>
          <section className="bg-white border-l-4 border-green-600 shadow-md p-6 rounded-lg w-full">
            <p className="text-gray-700 text-lg">
              The main model uses whether or not a play was a pickoff 
              to first as the indicator variable, so it is integral to the system that I identify pickoffs 
              correctly. This visualization serves as an eye test to verify the assumptions used to determine 
              which plays could be classified as pickoffs.
              Click to generate an animation of a play from the dataset of plays deemed as pickoffs to first.
            </p>
          </section>

          <section className="bg-white border-l-4 border-green-600 shadow-md p-6 rounded-lg w-full">
            <p className="text-gray-700 text-lg">
              Feel free to try some random samples to test my assumptions with the eye test!
            </p>
          </section>
        </div>

        <div className="flex-1 flex flex-col items-center gap-4">
          <button onClick={handleSubmit} 
          className="py-2 px-6 bg-green-600 text-white font-semibold text-lg rounded-full shadow-md hover:bg-green-700 transition duration-200">
            Generate Pickoff Play
          </button>

          <div className="bg-green-100 border border-green-400 p-4 rounded-lg shadow-inner w-full max-w-xl text-center">
            {loading ? (
              <p className="text-green-800 font-medium">Generating play...</p>
            ) : gifUrl ? (
              <img src={gifUrl} alt="Generated Pickoff Play Animation" className="rounded-md"/>
            ) : (
              <p className="text-green-800">
                Click the button to generate an animation of a pickoff to first base.
              </p>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}