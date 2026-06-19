import { NavBar } from "@/components/nav-bar";
import { PrivateConsole } from "@/components/private-console";

export default function PrivateConsolePage() {
  return (
    <>
      <NavBar />
      <main className="mx-auto w-full max-w-screen-xl px-4 py-6 md:px-6 md:py-8">
        <PrivateConsole />
      </main>
    </>
  );
}
