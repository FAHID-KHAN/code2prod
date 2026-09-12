import CoursePath from "@/components/CoursePath";
import Evidence from "@/components/Evidence";
import FinalCta from "@/components/FinalCta";
import Footer from "@/components/Footer";
import Hero from "@/components/Hero";
import MissionDemo from "@/components/MissionDemo";
import Nav from "@/components/Nav";
import Philosophy from "@/components/Philosophy";
import Trust from "@/components/Trust";

export default function Home() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <MissionDemo />
        <Philosophy />
        <CoursePath />
        <Evidence />
        <Trust />
        <FinalCta />
      </main>
      <Footer />
    </>
  );
}
