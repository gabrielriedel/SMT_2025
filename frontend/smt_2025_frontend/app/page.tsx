import Link from 'next/link'

export default function Home() {
  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
        <nav className="max-w-16xl bg-green-500 text-white items-center">
          <div className="max-w-4xl mx-auto flex justify-between items-center py-4 px-6">
            <h1 className="text-lg font-bold">SMT 2025 – Thou Shalt Not Steal: An Interactive Application</h1>
          </div>
      </nav>
      <main className="flex flex-row gap-[32px] row-start-2 items-start justify-center flex-wrap">
        <section className="bg-green-100 border border-green-400 p-4 rounded shadow-md w-64">
          <h2 className="text-lg font-bold text-green-800 mb-4">Menu</h2>
          <div className="flex flex-col gap-3">
            <Link 
              href="/scouting_report"
              className="text-green-900 hover:text-white hover:bg-green-700 font-medium py-2 px-3 rounded transition-colors duration-200">
              Scouting Report
            </Link>
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
              href="/run_plays"
              className="text-green-900 hover:text-white hover:bg-green-700 font-medium py-2 px-3 rounded transition-colors duration-200">
              Run Scoring Plays Visualized
            </Link>
            <Link 
              href="/out_plays"
              className="text-green-900 hover:text-white hover:bg-green-700 font-medium py-2 px-3 rounded transition-colors duration-200">
              Out Recorded Plays Visualized
            </Link>
            <Link 
              href="/contact_info"
              className="text-green-900 hover:text-white hover:bg-green-700 font-medium py-2 px-3 rounded transition-colors duration-200">
              Contact Info
            </Link>
          </div>
        </section>

        <section className="bg-green-100 border border-green-400 p-4 rounded shadow-md w-150 space-y-6">
          <h2 className="text-lg font-bold text-green-800 mb-4">What is this?</h2>
          <div className="text-green-900 flex flex-col gap-3">
            This application is a scouting report aimed to unveil the 
            tendency of a pitcher to attempt a pickoff at first base.
            You are able to select one of the three main teams in our 
            dataset (QEA, RZQ, and YJD) and a pitcher who has played 
            in more than one game in our data. Then, dynamically generated
            statistics on the pickoff proclivity and game experience 
            of the pitcher will pop up along with an interactive model. 
            This model allows you to input game state information, and 
            it will respond with the probability of a pitcher picking 
            off under those conditions.
          </div>
          <div className="text-green-900 flex flex-col gap-3">
            In order to generate the graphs and model in the scouting 
            report, I made inferences about various play types in the 
            data. The other tabs provide visualizations of the plays 
            I deemed as pickoff, stealing, run scoring, and out plays. 
            Watch them to assess the validity of my assumptions!
          </div>
        </section>
      </main>
    </div>
  );
}
