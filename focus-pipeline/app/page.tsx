import { NavBar } from "@/components/nav-bar";
import { PipelineDashboard } from "@/components/pipeline-dashboard";

export default function HomePage() {
  return (
    <>
      <NavBar />
      <main className="mx-auto w-full max-w-screen-xl px-4 py-6 md:px-6 md:py-8">
        <PipelineDashboard />
      </main>
    </>
  );
}
