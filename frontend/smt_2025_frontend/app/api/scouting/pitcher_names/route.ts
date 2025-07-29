// app/api/scouting/pitcher_names/route.ts

import { NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const team = searchParams.get('team');

  if (!team) {
    return new Response(JSON.stringify({ error: 'Missing team parameter' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const upstreamUrl = `https://smt-2025.onrender.com/api/pitcher_names?team=${encodeURIComponent(team)}`;
    const res = await fetch(upstreamUrl);
    const data = await res.text();

    return new Response(data, {
      status: res.status,
      headers: {
        'Content-Type': res.headers.get('content-type') || 'application/json',
      },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Failed to fetch upstream data' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
