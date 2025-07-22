"use client";
import { useEffect, useState } from "react";

export default function GifDisplay() {
  const [gifUrl, setGifUrl] = useState("");

  useEffect(() => {
    fetch("https://smt-2025.onrender.com/api/play_animation")
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
      });
  }, []);

  return (
    <div>
      {gifUrl ? (
        <img src={gifUrl} alt="Generated Animation" />
      ) : (
        <p>Loading animation...</p>
      )}
    </div>
  );
}
