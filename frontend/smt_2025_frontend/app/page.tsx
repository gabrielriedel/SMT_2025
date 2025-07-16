import Image from "next/image";
import Link from 'next/link'

export default function Home() {
  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
        <nav className="max-w-16xl bg-green-500 text-white items-center">
          <div className="max-w-4xl mx-auto flex justify-between items-center py-4 px-6">
            <h1 className="text-lg font-bold">SMT 2025 – Thou Shalt Not Steal: An Interactive Application</h1>
          </div>
      </nav>
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
          <section className="bg-green-100 border border-green-400 p-4 rounded shadow-md w-64 ml-4">
            <h2 className="text-lg font-bold text-green-800 mb-4">Menu</h2>
            <div className="flex flex-col gap-3">
              <Link 
                href="/pick_plays"
                className="text-green-900 hover:text-white hover:bg-green-700 font-medium py-2 px-3 rounded transition-colors duration-200">
                Pickoff Plays Visualized
              </Link>
              <Link 
                href="/steal_plays"
                className="text-green-900 hover:text-white hover:bg-green-700 font-medium py-2 px-3 rounded transition-colors duration-200">
                Stealing Plays Visualized
              </Link>
              <Link 
                href="/scouting_report"
                className="text-green-900 hover:text-white hover:bg-green-700 font-medium py-2 px-3 rounded transition-colors duration-200">
                Scouting Report
              </Link>
            </div>
          </section>
      </main>

      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/file.svg"
            alt="File icon"
            width={16}
            height={16}
          />
          Learn
        </a>
      </footer>
    </div>
  );
}
