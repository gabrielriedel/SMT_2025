import Link from 'next/link'

export default function Page() {
    return(
        <main className="flex flex-col px-6 py-10 max-w-6xl mx-auto gap-8">
            <Link href="/"
            className="text-green-900 bg-green-100 border border-green-400 absolute left-10 top-10 py-4 px-8 rounded-md no-underline text-foreground bg-btn-background hover:bg-btn-background-hover flex items-center group text-md text-blue-400">
                Back to dashboard
            </Link>
            <section className="bg-white border-l-4 border-green-600 shadow-md p-6 rounded-lg w-full">
            <p className="text-gray-700 text-lg text-center font-bold">
              Not filled out until papers are deanonymized
            </p>
          </section>
        </main>
    );
}