"use client";
import { useState } from "react";

export default function GifDisplay() {
  const [gifUrl, setGifUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = () => {
    setLoading(true);
    fetch("https://smt-2025.onrender.com/api/steal_animation")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch gif");
        return res.blob();
      })
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        setGifUrl(url);
      })
      .catch((err) => {
        console.error("Error loading gif:", err);
        alert("Failed to load animation. Please try again.");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <main className="flex flex-col items-center px-6 py-10 max-w-3xl mx-auto gap-8">
      <h1 className="text-3xl font-bold text-center text-green-800">
        Random Pickoff Play Generator
      </h1>

      <section className="bg-white border-l-4 border-green-600 shadow-md p-6 rounded-lg w-full">
        <p className="text-gray-700 text-lg">
          This page generates a random pickoff play animation using data that
          was used to train a machine learning model. When you click the button
          below, a new play is sampled and animated, simulating how the model
          interprets real-world defensive plays based on training data.
        </p>
      </section>

      <button
        onClick={handleSubmit}
        className="py-2 px-6 bg-green-600 text-white font-semibold text-lg rounded-full shadow-md hover:bg-green-700 transition duration-200"
      >
        Generate Pickoff Play
      </button>

      <section className="w-full flex justify-center">
        <div className="bg-green-100 border border-green-400 p-4 rounded-lg shadow-inner w-full max-w-xl text-center">
          {loading ? (
            <p className="text-green-800 font-medium">Generating play...</p>
          ) : gifUrl ? (
            <img
              src={gifUrl}
              alt="Generated Pickoff Play Animation"
              className="rounded-md"
            />
          ) : (
            <p className="text-green-800">
              Click the button above to generate a pickoff play animation.
            </p>
          )}
        </div>
      </section>
    </main>
  );
}
