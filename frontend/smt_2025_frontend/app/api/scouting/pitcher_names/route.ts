import { NextRequest } from "next/server";

export async function GET(request: NextRequest){

  const url = new URL(request.url);
  const team = url.searchParams.get('team');

  if (!team) {
    return new Response(JSON.stringify({ error: 'Team and pitcher are required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try{

    const apiUrl = `https://smt-2025.onrender.com/api/pitcher_names?team=${encodeURIComponent(team)}`;
    const backendResponse = await fetch(apiUrl);
    const contentType = backendResponse.headers.get('content-type') || '';
    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      return new Response(JSON.stringify({ error: errorText }), {
        status: backendResponse.status,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    if (!contentType.includes('application/json')) {
        const raw = await backendResponse.text();
        return new Response(JSON.stringify({ error: 'Expected JSON but got something else', raw }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' },
        });
      }
      const json = await backendResponse.json();
      return new Response(JSON.stringify(json), {status: 200,
        headers: { 'Content-Type': 'application/json' },});
    } catch (error: any) {
        return new Response(JSON.stringify({ error: error.message || 'Unknown error' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
        });
    }
  }

