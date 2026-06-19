import { NavBar } from "@/components/nav-bar";
import { OperatorConsole } from "@/components/operator-console";

export default function OperatorPage() {
  return (
    <>
      <NavBar />
      <main className="mx-auto w-full max-w-screen-xl px-4 py-6 md:px-6 md:py-8">
        <OperatorConsole />
      </main>
    </>
  );
}
